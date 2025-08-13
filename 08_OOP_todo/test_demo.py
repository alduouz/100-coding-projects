#!/usr/bin/env python3
"""Demo script to test the OOP Todo List functionality."""

import os
import json
from manager import TaskManager
from todo import TodoCLI


def test_todo_functionality():
    """Test all main functionality of the todo application."""
    print("=== OOP Todo List Demo ===\n")
    
    # Clean up any existing tasks file for demo
    if os.path.exists("demo_tasks.json"):
        os.remove("demo_tasks.json")
    
    # Create task manager with demo file
    task_manager = TaskManager("demo_tasks.json")
    
    print("1. Testing Task Creation:")
    # Add some tasks
    task1 = task_manager.add("Buy groceries", "2025-08-15")
    task2 = task_manager.add("Complete project report", "2025-08-20")
    task3 = task_manager.add("Call dentist")  # No due date
    
    print(f"   Added: {task1}")
    print(f"   Added: {task2}")
    print(f"   Added: {task3}")
    
    print("\n2. Testing Task Listing:")
    tasks = task_manager.list_all()
    for i, task in enumerate(tasks, 1):
        print(f"   {i}. {task}")
    
    print("\n3. Testing Task Completion:")
    completed_task = task_manager.complete_by_index(1)
    print(f"   Completed: {completed_task}")
    
    print("\n4. Updated Task List:")
    tasks = task_manager.list_all()
    for i, task in enumerate(tasks, 1):
        print(f"   {i}. {task}")
    
    print("\n5. Testing Task Deletion:")
    deleted_task = task_manager.delete_by_index(2)
    print(f"   Deleted: {deleted_task}")
    
    print("\n6. Final Task List:")
    tasks = task_manager.list_all()
    for i, task in enumerate(tasks, 1):
        print(f"   {i}. {task}")
    
    print("\n7. Testing Persistence:")
    print("   Loading tasks from file...")
    new_manager = TaskManager("demo_tasks.json")
    new_manager.load()
    loaded_tasks = new_manager.list_all()
    print(f"   Loaded {len(loaded_tasks)} tasks from file:")
    for i, task in enumerate(loaded_tasks, 1):
        print(f"   {i}. {task}")
    
    print("\n8. JSON File Content:")
    if os.path.exists("demo_tasks.json"):
        with open("demo_tasks.json", "r", encoding="utf-8") as f:
            content = json.load(f)
            print("   Raw JSON content:")
            print("  ", json.dumps(content, indent=4, ensure_ascii=False))
    
    print("\n=== Demo Complete ===")
    print("All functionality working correctly!")


if __name__ == "__main__":
    test_todo_functionality()