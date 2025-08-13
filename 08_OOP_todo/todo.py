#!/usr/bin/env python3
from typing import Callable, Optional
from datetime import datetime
import sys
from manager import TaskManager


class TodoCLI:
    """Command-line interface for the OOP Todo List application."""
    
    def __init__(self, task_manager: TaskManager, 
                 input_func: Callable[[str], str] = input,
                 print_func: Callable[[str], None] = print):
        """Initialize CLI with dependency injection for testing.
        
        Args:
            task_manager: TaskManager instance for task operations
            input_func: Function for getting user input (injectable for testing)
            print_func: Function for printing output (injectable for testing)
        """
        self.task_manager = task_manager
        self.input_func = input_func
        self.print_func = print_func
    
    def display_menu(self) -> None:
        """Display the main menu options."""
        self.print_func("\n--- To-Do List (OOP) ---")
        self.print_func("1. Add Task")
        self.print_func("2. List Tasks")
        self.print_func("3. Mark Task Complete")
        self.print_func("4. Delete Task")
        self.print_func("5. Exit")
    
    def get_menu_choice(self) -> str:
        """Get and validate menu choice from user."""
        while True:
            try:
                choice = self.input_func("Enter choice: ").strip()
                if choice in ["1", "2", "3", "4", "5"]:
                    return choice
                else:
                    self.print_func("Invalid choice. Please enter 1-5.")
            except (EOFError, KeyboardInterrupt):
                return "5"  # Exit gracefully
    
    def get_task_description(self) -> str:
        """Get non-empty task description from user."""
        while True:
            try:
                description = self.input_func("Description: ").strip()
                if description:
                    return description
                else:
                    self.print_func("Description cannot be empty. Please try again.")
            except (EOFError, KeyboardInterrupt):
                raise KeyboardInterrupt("User cancelled input")
    
    def get_due_date(self) -> Optional[str]:
        """Get optional due date from user with validation."""
        while True:
            try:
                due_date = self.input_func("Due date (YYYY-MM-DD, Enter to skip): ").strip()
                if not due_date:
                    return None
                
                # Validate date format
                try:
                    datetime.strptime(due_date, "%Y-%m-%d")
                    return due_date
                except ValueError:
                    self.print_func("Invalid date format. Please use YYYY-MM-DD or press Enter to skip.")
            except (EOFError, KeyboardInterrupt):
                return None
    
    def get_task_index(self, operation: str) -> int:
        """Get and validate task index from user.
        
        Args:
            operation: Description of operation for error messages
            
        Returns:
            Valid 1-based task index
            
        Raises:
            ValueError: If user cancels input
        """
        tasks = self.task_manager.list_all()
        if not tasks:
            self.print_func("No tasks available.")
            raise ValueError("No tasks available")
        
        while True:
            try:
                index_str = self.input_func(f"Enter task number to {operation}: ").strip()
                index = int(index_str)
                if 1 <= index <= len(tasks):
                    return index
                else:
                    self.print_func(f"Invalid task number. Please enter 1-{len(tasks)}.")
            except ValueError:
                self.print_func("Please enter a valid number.")
            except (EOFError, KeyboardInterrupt):
                raise ValueError("User cancelled input")
    
    def add_task(self) -> None:
        """Handle adding a new task."""
        try:
            description = self.get_task_description()
            due_date = self.get_due_date()
            
            task = self.task_manager.add(description, due_date)
            self.print_func(f"Task '{task.description}' added!")
        except KeyboardInterrupt:
            self.print_func("Task creation cancelled.")
    
    def list_tasks(self) -> None:
        """Handle listing all tasks."""
        tasks = self.task_manager.list_all()
        if not tasks:
            self.print_func("\nNo tasks found.")
            return
        
        self.print_func("\n--- Your Tasks ---")
        for i, task in enumerate(tasks, 1):
            self.print_func(f"{i}. {task}")
    
    def complete_task(self) -> None:
        """Handle marking a task as complete."""
        try:
            index = self.get_task_index("complete")
            task = self.task_manager.complete_by_index(index)
            self.print_func(f"Task '{task.description}' marked as complete!")
        except (ValueError, IndexError) as e:
            if "No tasks available" not in str(e):
                self.print_func("Operation cancelled.")
    
    def delete_task(self) -> None:
        """Handle deleting a task."""
        try:
            index = self.get_task_index("delete")
            task = self.task_manager.delete_by_index(index)
            self.print_func(f"Task '{task.description}' deleted!")
        except (ValueError, IndexError) as e:
            if "No tasks available" not in str(e):
                self.print_func("Operation cancelled.")
    
    def run(self) -> None:
        """Main application loop."""
        self.print_func("Welcome to Todo List (OOP)!")
        
        # Load existing tasks
        self.task_manager.load()
        
        while True:
            try:
                self.display_menu()
                choice = self.get_menu_choice()
                
                if choice == "1":
                    self.add_task()
                elif choice == "2":
                    self.list_tasks()
                elif choice == "3":
                    self.complete_task()
                elif choice == "4":
                    self.delete_task()
                elif choice == "5":
                    self.print_func("Goodbye!")
                    break
            except KeyboardInterrupt:
                self.print_func("\nGoodbye!")
                break
            except Exception as e:
                self.print_func(f"An error occurred: {e}")


def main():
    """Main entry point for the application."""
    task_manager = TaskManager("tasks.json")
    cli = TodoCLI(task_manager)
    cli.run()


if __name__ == "__main__":
    main()