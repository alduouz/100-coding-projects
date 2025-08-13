import unittest
import tempfile
import os
from io import StringIO
from unittest.mock import Mock
from manager import TaskManager
from todo import TodoCLI


class TestTodoCLI(unittest.TestCase):
    """Unit tests for TodoCLI class using dependency injection for I/O."""
    
    def setUp(self):
        """Set up test fixtures with temporary directory and mocked I/O."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = os.path.join(self.temp_dir.name, "test_tasks.json")
        self.task_manager = TaskManager(self.test_file)
        
        # Mock I/O functions
        self.mock_input = Mock()
        self.mock_print = Mock()
        
        # Create CLI with mocked I/O
        self.cli = TodoCLI(
            task_manager=self.task_manager,
            input_func=self.mock_input,
            print_func=self.mock_print
        )
    
    def tearDown(self):
        """Clean up temporary directory after each test."""
        self.temp_dir.cleanup()
    
    def test_add_list_exit_flow(self):
        """Test basic flow: Add → List → Exit with simulated user input."""
        # Setup input sequence: Add task, List tasks, Exit
        self.mock_input.side_effect = [
            "1",  # Choose "Add Task"
            "Test task from CLI",  # Task description
            "",  # No due date (press Enter to skip)
            "2",  # Choose "List Tasks"
            "5"   # Choose "Exit"
        ]
        
        # Run the CLI
        self.cli.run()
        
        # Verify task was added
        tasks = self.task_manager.list_all()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].description, "Test task from CLI")
        self.assertFalse(tasks[0].completed)
        self.assertIsNone(tasks[0].due_date)
        
        # Verify expected output was printed
        print_calls = [call[0][0] for call in self.mock_print.call_args_list]
        
        # Check key messages appear in output
        self.assertIn("Welcome to Todo List (OOP)!", print_calls)
        self.assertIn("Task 'Test task from CLI' added!", print_calls)
        
        # Check for the tasks header (it appears with newline prefix)
        tasks_header_found = any("--- Your Tasks ---" in call for call in print_calls)
        self.assertTrue(tasks_header_found, "--- Your Tasks --- should appear in output")
        
        self.assertIn("Goodbye!", print_calls)
        
        # Verify task appears in list output
        task_listing_found = False
        for call in print_calls:
            if "1. [✗] Test task from CLI" in call:
                task_listing_found = True
                break
        self.assertTrue(task_listing_found, "Task should appear in listing with correct format")
    
    def test_add_task_with_due_date(self):
        """Test adding a task with due date."""
        self.mock_input.side_effect = [
            "1",  # Choose "Add Task"
            "Task with due date",  # Task description
            "2024-12-25",  # Due date
            "5"   # Choose "Exit"
        ]
        
        self.cli.run()
        
        tasks = self.task_manager.list_all()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].description, "Task with due date")
        self.assertEqual(tasks[0].due_date, "2024-12-25")
    
    def test_complete_task_flow(self):
        """Test completing a task through CLI."""
        # Pre-add a task
        self.task_manager.add("Task to complete")
        
        self.mock_input.side_effect = [
            "3",  # Choose "Mark Task Complete"
            "1",  # Select first task
            "2",  # Choose "List Tasks"
            "5"   # Choose "Exit"
        ]
        
        self.cli.run()
        
        # Verify task is completed
        tasks = self.task_manager.list_all()
        self.assertEqual(len(tasks), 1)
        self.assertTrue(tasks[0].completed)
        
        # Verify completion message was shown
        print_calls = [call[0][0] for call in self.mock_print.call_args_list]
        self.assertIn("Task 'Task to complete' marked as complete!", print_calls)
        
        # Verify completed task shows with checkmark in listing
        completed_task_found = False
        for call in print_calls:
            if "1. [✓] Task to complete" in call:
                completed_task_found = True
                break
        self.assertTrue(completed_task_found, "Completed task should show with checkmark")
    
    def test_delete_task_flow(self):
        """Test deleting a task through CLI."""
        # Pre-add a task
        self.task_manager.add("Task to delete")
        
        self.mock_input.side_effect = [
            "4",  # Choose "Delete Task"
            "1",  # Select first task
            "2",  # Choose "List Tasks"
            "5"   # Choose "Exit"
        ]
        
        self.cli.run()
        
        # Verify task is deleted
        tasks = self.task_manager.list_all()
        self.assertEqual(len(tasks), 0)
        
        # Verify deletion message was shown
        print_calls = [call[0][0] for call in self.mock_print.call_args_list]
        self.assertIn("Task 'Task to delete' deleted!", print_calls)
        
        # Verify "No tasks found" message appears when listing
        self.assertIn("\nNo tasks found.", print_calls)
    
    def test_empty_task_list_operations(self):
        """Test operations when no tasks exist."""
        self.mock_input.side_effect = [
            "3",  # Try to complete task (should show no tasks)
            "4",  # Try to delete task (should show no tasks)
            "5"   # Choose "Exit"
        ]
        
        self.cli.run()
        
        # Verify appropriate messages are shown
        print_calls = [call[0][0] for call in self.mock_print.call_args_list]
        no_tasks_count = sum(1 for call in print_calls if "No tasks available." in call)
        self.assertEqual(no_tasks_count, 2, "Should show 'No tasks available' for both operations")
    
    def test_invalid_menu_choice_handling(self):
        """Test handling of invalid menu choices."""
        self.mock_input.side_effect = [
            "invalid",  # Invalid choice
            "0",        # Invalid choice
            "6",        # Invalid choice
            "2",        # Valid choice - List Tasks
            "5"         # Exit
        ]
        
        self.cli.run()
        
        # Verify error messages are shown for invalid choices
        print_calls = [call[0][0] for call in self.mock_print.call_args_list]
        invalid_choice_count = sum(1 for call in print_calls if "Invalid choice. Please enter 1-5." in call)
        self.assertEqual(invalid_choice_count, 3, "Should show error message for each invalid choice")
    
    def test_keyboard_interrupt_handling(self):
        """Test graceful handling of KeyboardInterrupt (Ctrl+C)."""
        self.mock_input.side_effect = KeyboardInterrupt()
        
        # Should not raise exception
        self.cli.run()
        
        # Verify goodbye message is shown
        print_calls = [call[0][0] for call in self.mock_print.call_args_list]
        
        # Check for goodbye message (it may appear with or without newline prefix)
        goodbye_found = any("Goodbye!" in call for call in print_calls)
        self.assertTrue(goodbye_found, "Goodbye message should appear in output")


if __name__ == "__main__":
    unittest.main()