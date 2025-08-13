import unittest
import tempfile
import os
import json
from unittest.mock import Mock
from contact_book import ContactBook


class TestContactBook(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.mock_input = Mock()
        self.mock_print = Mock()
        self.contact_book = ContactBook(
            filename=self.temp_file.name,
            input_func=self.mock_input,
            print_func=self.mock_print
        )

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_validate_name(self):
        self.assertTrue(self.contact_book.validate_name("John Doe"))
        self.assertTrue(self.contact_book.validate_name(" John "))
        self.assertFalse(self.contact_book.validate_name(""))
        self.assertFalse(self.contact_book.validate_name("   "))

    def test_validate_phone(self):
        self.assertTrue(self.contact_book.validate_phone("1234567890"))
        self.assertTrue(self.contact_book.validate_phone("123-456-7890"))
        self.assertTrue(self.contact_book.validate_phone("(123) 456-7890"))
        self.assertFalse(self.contact_book.validate_phone(""))
        self.assertFalse(self.contact_book.validate_phone("abc"))

    def test_validate_email(self):
        self.assertTrue(self.contact_book.validate_email("test@example.com"))
        self.assertTrue(self.contact_book.validate_email(""))
        self.assertTrue(self.contact_book.validate_email("   "))
        self.assertFalse(self.contact_book.validate_email("invalid-email"))

    def test_clean_phone(self):
        self.assertEqual(self.contact_book.clean_phone("123-456-7890"), "1234567890")
        self.assertEqual(self.contact_book.clean_phone("(123) 456-7890"), "1234567890")
        self.assertEqual(self.contact_book.clean_phone("123 456 7890"), "1234567890")
        self.assertEqual(self.contact_book.clean_phone("1234567890"), "1234567890")

    def test_load_contacts_empty_file(self):
        contact_book = ContactBook(filename=self.temp_file.name)
        self.assertEqual(contact_book.contacts, [])

    def test_load_contacts_with_data(self):
        test_contacts = [
            {"name": "John Doe", "phone": "1234567890", "email": "john@example.com"}
        ]
        with open(self.temp_file.name, 'w') as f:
            json.dump(test_contacts, f)
        
        contact_book = ContactBook(filename=self.temp_file.name)
        self.assertEqual(contact_book.contacts, test_contacts)

    def test_save_contacts(self):
        test_contacts = [
            {"name": "John Doe", "phone": "1234567890", "email": "john@example.com"}
        ]
        self.contact_book.contacts = test_contacts
        self.contact_book.save_contacts()
        
        with open(self.temp_file.name, 'r') as f:
            saved_contacts = json.load(f)
        
        self.assertEqual(saved_contacts, test_contacts)

    def test_add_contact_valid(self):
        self.mock_input.side_effect = ["John Doe", "1234567890", "john@example.com"]
        
        self.contact_book.add_contact()
        
        self.assertEqual(len(self.contact_book.contacts), 1)
        contact = self.contact_book.contacts[0]
        self.assertEqual(contact["name"], "John Doe")
        self.assertEqual(contact["phone"], "1234567890")
        self.assertEqual(contact["email"], "john@example.com")

    def test_add_contact_invalid_name_then_valid(self):
        self.mock_input.side_effect = ["", "  ", "John Doe", "1234567890", ""]
        
        self.contact_book.add_contact()
        
        self.assertEqual(len(self.contact_book.contacts), 1)
        self.assertEqual(self.contact_book.contacts[0]["name"], "John Doe")

    def test_add_contact_invalid_phone_then_valid(self):
        self.mock_input.side_effect = ["John Doe", "abc", "123-456-7890", ""]
        
        self.contact_book.add_contact()
        
        self.assertEqual(self.contact_book.contacts[0]["phone"], "1234567890")

    def test_view_all_contacts_empty(self):
        self.contact_book.view_all_contacts()
        self.mock_print.assert_any_call("\nNo contacts found.")

    def test_view_all_contacts_with_data(self):
        self.contact_book.contacts = [
            {"name": "John Doe", "phone": "1234567890", "email": "john@example.com"},
            {"name": "Alice Smith", "phone": "0987654321", "email": "alice@example.com"}
        ]
        
        self.contact_book.view_all_contacts()
        
        self.mock_print.assert_any_call("\n--- All Contacts ---")

    def test_search_contact_found(self):
        self.contact_book.contacts = [
            {"name": "John Doe", "phone": "1234567890", "email": "john@example.com"},
            {"name": "Alice Smith", "phone": "0987654321", "email": "alice@example.com"}
        ]
        self.mock_input.return_value = "john"
        
        self.contact_book.search_contact()
        
        self.mock_print.assert_any_call("\n--- Search Results for 'john' ---")

    def test_search_contact_not_found(self):
        self.contact_book.contacts = [
            {"name": "John Doe", "phone": "1234567890", "email": "john@example.com"}
        ]
        self.mock_input.return_value = "bob"
        
        self.contact_book.search_contact()
        
        self.mock_print.assert_any_call("No contacts found matching 'bob'.")

    def test_search_contact_empty_list(self):
        self.mock_input.return_value = "john"
        
        self.contact_book.search_contact()
        
        self.mock_print.assert_any_call("\nNo contacts found.")

    def test_update_contact_found(self):
        self.contact_book.contacts = [
            {"name": "John Doe", "phone": "1234567890", "email": "john@example.com"}
        ]
        self.mock_input.side_effect = ["John Doe", "Jane Doe", "0987654321", "jane@example.com"]
        
        self.contact_book.update_contact()
        
        contact = self.contact_book.contacts[0]
        self.assertEqual(contact["name"], "Jane Doe")
        self.assertEqual(contact["phone"], "0987654321")
        self.assertEqual(contact["email"], "jane@example.com")

    def test_update_contact_not_found(self):
        self.contact_book.contacts = [
            {"name": "John Doe", "phone": "1234567890", "email": "john@example.com"}
        ]
        self.mock_input.return_value = "Bob Smith"
        
        self.contact_book.update_contact()
        
        self.mock_print.assert_any_call("Contact 'Bob Smith' not found.")

    def test_update_contact_keep_values(self):
        original_contact = {"name": "John Doe", "phone": "1234567890", "email": "john@example.com"}
        self.contact_book.contacts = [original_contact.copy()]
        self.mock_input.side_effect = ["John Doe", "", "", ""]
        
        self.contact_book.update_contact()
        
        contact = self.contact_book.contacts[0]
        self.assertEqual(contact["name"], "John Doe")
        self.assertEqual(contact["phone"], "1234567890")
        self.assertEqual(contact["email"], "john@example.com")

    def test_delete_contact_confirmed(self):
        self.contact_book.contacts = [
            {"name": "John Doe", "phone": "1234567890", "email": "john@example.com"}
        ]
        self.mock_input.side_effect = ["John Doe", "y"]
        
        self.contact_book.delete_contact()
        
        self.assertEqual(len(self.contact_book.contacts), 0)
        self.mock_print.assert_any_call("Contact 'John Doe' deleted successfully!")

    def test_delete_contact_cancelled(self):
        self.contact_book.contacts = [
            {"name": "John Doe", "phone": "1234567890", "email": "john@example.com"}
        ]
        self.mock_input.side_effect = ["John Doe", "n"]
        
        self.contact_book.delete_contact()
        
        self.assertEqual(len(self.contact_book.contacts), 1)
        self.mock_print.assert_any_call("Delete cancelled.")

    def test_delete_contact_not_found(self):
        self.contact_book.contacts = [
            {"name": "John Doe", "phone": "1234567890", "email": "john@example.com"}
        ]
        self.mock_input.return_value = "Bob Smith"
        
        self.contact_book.delete_contact()
        
        self.mock_print.assert_any_call("Contact 'Bob Smith' not found.")

    def test_run_add_contact_then_exit(self):
        self.mock_input.side_effect = ["1", "John Doe", "1234567890", "john@example.com", "6"]
        
        self.contact_book.run()
        
        self.assertEqual(len(self.contact_book.contacts), 1)
        self.mock_print.assert_any_call("Contacts saved. Goodbye!")

    def test_run_invalid_choice(self):
        self.mock_input.side_effect = ["9", "6"]
        
        self.contact_book.run()
        
        self.mock_print.assert_any_call("Invalid choice. Please enter a number between 1-6.")


if __name__ == '__main__':
    unittest.main()