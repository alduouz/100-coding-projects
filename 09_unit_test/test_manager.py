import unittest
import tempfile
import os
import json
from manager import TaskManager
from models import Task


class TestTaskManager(unittest.TestCase):
    """Unit tests for TaskManager class."""
    
    def setUp(self):
        """Set up test fixtures with temporary directory for each test."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = os.path.join(self.temp_dir.name, "test_tasks.json")
        self.manager = TaskManager(self.test_file)
    
    def tearDown(self):
        """Clean up temporary directory after each test."""
        self.temp_dir.cleanup()
    
    def test_add_task(self):
        """Test adding a task with correct description, due date, and default completed=False."""
        description = "Test task"
        due_date = "2024-12-31"
        
        task = self.manager.add(description, due_date)
        
        self.assertEqual(task.description, description)
        self.assertEqual(task.due_date, due_date)
        self.assertFalse(task.completed)
        self.assertEqual(len(self.manager.tasks), 1)
        self.assertEqual(self.manager.tasks[0], task)
    
    def test_add_task_no_due_date(self):
        """Test adding a task without due date."""
        description = "Task without due date"
        
        task = self.manager.add(description)
        
        self.assertEqual(task.description, description)
        self.assertIsNone(task.due_date)
        self.assertFalse(task.completed)
    
    def test_complete_task(self):
        """Test adding a task, marking it complete, and verifying completed=True."""
        task = self.manager.add("Task to complete")
        
        completed_task = self.manager.complete_by_index(1)
        
        self.assertTrue(completed_task.completed)
        self.assertEqual(completed_task.id, task.id)
        self.assertTrue(self.manager.tasks[0].completed)
    
    def test_delete_task(self):
        """Test adding a task, deleting it, and confirming removal from list."""
        task = self.manager.add("Task to delete")
        initial_count = len(self.manager.tasks)
        
        deleted_task = self.manager.delete_by_index(1)
        
        self.assertEqual(deleted_task.id, task.id)
        self.assertEqual(deleted_task.description, task.description)
        self.assertEqual(len(self.manager.tasks), initial_count - 1)
        self.assertNotIn(task, self.manager.tasks)
    
    def test_persistence_save_and_load(self):
        """Test adding tasks, saving them, reloading from disk, and confirming data matches."""
        # Add multiple tasks
        task1 = self.manager.add("First task", "2024-01-01")
        task2 = self.manager.add("Second task")
        self.manager.complete_by_index(1)  # Complete first task
        
        # Verify tasks are in memory
        self.assertEqual(len(self.manager.tasks), 2)
        self.assertTrue(self.manager.tasks[0].completed)
        
        # Create new manager instance to test loading
        new_manager = TaskManager(self.test_file)
        new_manager.load()
        
        # Verify loaded data matches saved data
        self.assertEqual(len(new_manager.tasks), 2)
        
        loaded_task1 = new_manager.tasks[0]
        loaded_task2 = new_manager.tasks[1]
        
        self.assertEqual(loaded_task1.id, task1.id)
        self.assertEqual(loaded_task1.description, task1.description)
        self.assertEqual(loaded_task1.due_date, task1.due_date)
        self.assertTrue(loaded_task1.completed)
        
        self.assertEqual(loaded_task2.id, task2.id)
        self.assertEqual(loaded_task2.description, task2.description)
        self.assertIsNone(loaded_task2.due_date)
        self.assertFalse(loaded_task2.completed)
    
    def test_load_nonexistent_file(self):
        """Test loading when file doesn't exist starts with empty task list."""
        nonexistent_path = os.path.join(self.temp_dir.name, "nonexistent.json")
        manager = TaskManager(nonexistent_path)
        
        manager.load()
        
        self.assertEqual(len(manager.tasks), 0)
    
    def test_load_corrupted_file(self):
        """Test loading corrupted JSON file starts with empty task list."""
        # Create corrupted JSON file
        with open(self.test_file, "w") as f:
            f.write("invalid json content")
        
        self.manager.load()
        
        self.assertEqual(len(self.manager.tasks), 0)
    
    def test_index_validation(self):
        """Test that invalid indices raise IndexError."""
        self.manager.add("Test task")
        
        # Test out of range indices
        with self.assertRaises(IndexError):
            self.manager.complete_by_index(0)  # Index too low
        
        with self.assertRaises(IndexError):
            self.manager.complete_by_index(2)  # Index too high
        
        with self.assertRaises(IndexError):
            self.manager.delete_by_index(0)  # Index too low
        
        with self.assertRaises(IndexError):
            self.manager.delete_by_index(2)  # Index too high


if __name__ == "__main__":
    unittest.main()