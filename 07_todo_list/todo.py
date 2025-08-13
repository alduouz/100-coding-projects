#!/usr/bin/env python3
import json
import os
from datetime import datetime
from typing import List, Dict, Optional

TASKS_FILE = "tasks.json"

def load_tasks() -> List[Dict]:
    if not os.path.exists(TASKS_FILE):
        return []
    
    try:
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_tasks(tasks: List[Dict]) -> None:
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

def add_task(tasks: List[Dict]) -> None:
    description = input("Enter task description: ").strip()
    if not description:
        print("Task description cannot be empty!")
        return
    
    due_date_input = input("Enter due date (YYYY-MM-DD) or press Enter to skip: ").strip()
    due_date = None
    
    if due_date_input:
        try:
            datetime.strptime(due_date_input, "%Y-%m-%d")
            due_date = due_date_input
        except ValueError:
            print("Invalid date format. Task added without due date.")
    
    task = {
        "id": len(tasks) + 1,
        "description": description,
        "completed": False,
        "due_date": due_date,
        "created_at": datetime.now().isoformat()
    }
    
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task '{description}' added successfully!")

def list_tasks(tasks: List[Dict]) -> None:
    if not tasks:
        print("No tasks found.")
        return
    
    print("\n--- Your Tasks ---")
    for i, task in enumerate(tasks, 1):
        status = "✓" if task["completed"] else "✗"
        due_info = f" (Due: {task['due_date']})" if task.get("due_date") else ""
        print(f"{i}. [{status}] {task['description']}{due_info}")
    print()

def complete_task(tasks: List[Dict]) -> None:
    if not tasks:
        print("No tasks available.")
        return
    
    list_tasks(tasks)
    
    try:
        task_num = int(input("Enter task number to mark as complete: "))
        if 1 <= task_num <= len(tasks):
            if tasks[task_num - 1]["completed"]:
                print("Task is already completed!")
            else:
                tasks[task_num - 1]["completed"] = True
                save_tasks(tasks)
                print(f"Task '{tasks[task_num - 1]['description']}' marked as complete!")
        else:
            print("Invalid task number!")
    except ValueError:
        print("Please enter a valid number!")

def delete_task(tasks: List[Dict]) -> None:
    if not tasks:
        print("No tasks available.")
        return
    
    list_tasks(tasks)
    
    try:
        task_num = int(input("Enter task number to delete: "))
        if 1 <= task_num <= len(tasks):
            deleted_task = tasks.pop(task_num - 1)
            
            for i, task in enumerate(tasks):
                task["id"] = i + 1
            
            save_tasks(tasks)
            print(f"Task '{deleted_task['description']}' deleted successfully!")
        else:
            print("Invalid task number!")
    except ValueError:
        print("Please enter a valid number!")

def show_menu() -> None:
    print("\n--- To-Do List Manager ---")
    print("1. Add Task")
    print("2. List Tasks")
    print("3. Mark Task Complete")
    print("4. Delete Task")
    print("5. Exit")
    print("-" * 25)

def main():
    print("Welcome to To-Do List Manager!")
    tasks = load_tasks()
    
    while True:
        show_menu()
        
        try:
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == "1":
                add_task(tasks)
            elif choice == "2":
                list_tasks(tasks)
            elif choice == "3":
                complete_task(tasks)
            elif choice == "4":
                delete_task(tasks)
            elif choice == "5":
                print("Thank you for using To-Do List Manager!")
                break
            else:
                print("Invalid choice! Please enter 1-5.")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()