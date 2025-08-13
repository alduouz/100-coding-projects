import json
import os
import re
from typing import List, Dict, Optional, Callable


class ContactBook:
    def __init__(self, filename: str = "contacts.json", input_func: Callable = input, print_func: Callable = print):
        self.filename = filename
        self.contacts: List[Dict[str, str]] = []
        self.input_func = input_func
        self.print_func = print_func
        self.load_contacts()

    def load_contacts(self) -> None:
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    self.contacts = json.load(file)
            except (json.JSONDecodeError, FileNotFoundError):
                self.contacts = []
        else:
            self.contacts = []

    def save_contacts(self) -> None:
        with open(self.filename, 'w') as file:
            json.dump(self.contacts, file, indent=2)

    def validate_name(self, name: str) -> bool:
        return bool(name.strip())

    def validate_phone(self, phone: str) -> bool:
        cleaned_phone = re.sub(r'[^\d]', '', phone)
        return bool(cleaned_phone) and cleaned_phone.isdigit()

    def validate_email(self, email: str) -> bool:
        if not email.strip():
            return True
        return '@' in email

    def clean_phone(self, phone: str) -> str:
        return re.sub(r'[^\d]', '', phone)

    def add_contact(self) -> None:
        self.print_func("\n--- Add New Contact ---")
        
        while True:
            name = self.input_func("Enter name: ").strip()
            if self.validate_name(name):
                break
            self.print_func("Name cannot be empty. Please try again.")

        while True:
            phone = self.input_func("Enter phone number: ").strip()
            if self.validate_phone(phone):
                phone = self.clean_phone(phone)
                break
            self.print_func("Phone number must contain only digits. Please try again.")

        email = self.input_func("Enter email (optional): ").strip()
        if email and not self.validate_email(email):
            self.print_func("Invalid email format. Email not added.")
            email = ""

        contact = {
            "name": name,
            "phone": phone,
            "email": email
        }

        self.contacts.append(contact)
        self.save_contacts()
        self.print_func(f"Contact '{name}' added successfully!")

    def view_all_contacts(self) -> None:
        if not self.contacts:
            self.print_func("\nNo contacts found.")
            return

        self.print_func("\n--- All Contacts ---")
        self.print_func(f"{'Name':<20} {'Phone':<15} {'Email':<30}")
        self.print_func("-" * 65)
        
        sorted_contacts = sorted(self.contacts, key=lambda x: x['name'].lower())
        for contact in sorted_contacts:
            email = contact.get('email', '')
            self.print_func(f"{contact['name']:<20} {contact['phone']:<15} {email:<30}")

    def search_contact(self) -> None:
        if not self.contacts:
            self.print_func("\nNo contacts found.")
            return

        search_term = self.input_func("\nEnter name to search: ").strip().lower()
        if not search_term:
            self.print_func("Search term cannot be empty.")
            return

        found_contacts = [
            contact for contact in self.contacts
            if search_term in contact['name'].lower()
        ]

        if not found_contacts:
            self.print_func(f"No contacts found matching '{search_term}'.")
            return

        self.print_func(f"\n--- Search Results for '{search_term}' ---")
        self.print_func(f"{'Name':<20} {'Phone':<15} {'Email':<30}")
        self.print_func("-" * 65)
        
        for contact in found_contacts:
            email = contact.get('email', '')
            self.print_func(f"{contact['name']:<20} {contact['phone']:<15} {email:<30}")

    def update_contact(self) -> None:
        if not self.contacts:
            self.print_func("\nNo contacts found.")
            return

        name_to_update = self.input_func("\nEnter name of contact to update: ").strip()
        
        contact_index = None
        for i, contact in enumerate(self.contacts):
            if contact['name'].lower() == name_to_update.lower():
                contact_index = i
                break

        if contact_index is None:
            self.print_func(f"Contact '{name_to_update}' not found.")
            return

        contact = self.contacts[contact_index]
        self.print_func(f"\nUpdating contact: {contact['name']}")
        self.print_func("Press Enter to keep current value, or enter new value:")

        new_name = self.input_func(f"Name ({contact['name']}): ").strip()
        if new_name and self.validate_name(new_name):
            contact['name'] = new_name
        elif new_name:
            self.print_func("Invalid name. Keeping current value.")

        new_phone = self.input_func(f"Phone ({contact['phone']}): ").strip()
        if new_phone and self.validate_phone(new_phone):
            contact['phone'] = self.clean_phone(new_phone)
        elif new_phone:
            self.print_func("Invalid phone. Keeping current value.")

        new_email = self.input_func(f"Email ({contact.get('email', '')}): ").strip()
        if new_email:
            if self.validate_email(new_email):
                contact['email'] = new_email
            else:
                self.print_func("Invalid email. Keeping current value.")

        self.save_contacts()
        self.print_func(f"Contact '{contact['name']}' updated successfully!")

    def delete_contact(self) -> None:
        if not self.contacts:
            self.print_func("\nNo contacts found.")
            return

        name_to_delete = self.input_func("\nEnter name of contact to delete: ").strip()
        
        contact_index = None
        for i, contact in enumerate(self.contacts):
            if contact['name'].lower() == name_to_delete.lower():
                contact_index = i
                break

        if contact_index is None:
            self.print_func(f"Contact '{name_to_delete}' not found.")
            return

        contact = self.contacts[contact_index]
        confirm = self.input_func(f"Are you sure you want to delete '{contact['name']}'? (y/N): ").strip().lower()
        
        if confirm == 'y' or confirm == 'yes':
            self.contacts.pop(contact_index)
            self.save_contacts()
            self.print_func(f"Contact '{contact['name']}' deleted successfully!")
        else:
            self.print_func("Delete cancelled.")

    def display_menu(self) -> None:
        self.print_func("\n=== Contact Book ===")
        self.print_func("1. Add Contact")
        self.print_func("2. View All Contacts")
        self.print_func("3. Search Contact")
        self.print_func("4. Update Contact")
        self.print_func("5. Delete Contact")
        self.print_func("6. Exit")
        self.print_func("=" * 20)

    def run(self) -> None:
        while True:
            self.display_menu()
            choice = self.input_func("Enter your choice (1-6): ").strip()

            if choice == '1':
                self.add_contact()
            elif choice == '2':
                self.view_all_contacts()
            elif choice == '3':
                self.search_contact()
            elif choice == '4':
                self.update_contact()
            elif choice == '5':
                self.delete_contact()
            elif choice == '6':
                self.save_contacts()
                self.print_func("Contacts saved. Goodbye!")
                break
            else:
                self.print_func("Invalid choice. Please enter a number between 1-6.")


def main():
    contact_book = ContactBook()
    contact_book.run()


if __name__ == "__main__":
    main()