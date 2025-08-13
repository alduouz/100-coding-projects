
# Project 7: To-Do List CLI App with JSON Storage - PRD

## 1. Overview
Create a Python command-line application that lets users manage a to-do list. Tasks should be stored in a JSON file so they persist between runs. The app will allow adding, completing, deleting, and listing tasks, and will maintain task status.

## 2. Functional Requirements
- **Add Task:**
  - Prompt for task description (required).
  - Prompt for optional due date.
  - Store task with a default "incomplete" status.
- **Mark Task as Complete:**
  - Select a task by number and mark it complete.
- **Delete Task:**
  - Select a task by number and remove it from the list.
- **List Tasks:**
  - Display tasks in a numbered list.
  - Show task status (complete/incomplete).
  - Show due dates if available.
- **Persistent Storage:**
  - Load tasks from `tasks.json` at program start.
  - Save tasks to `tasks.json` after every change.

## 3. Non-functional Requirements
- Use only Python standard library (`json` for file handling).
- Menu-driven CLI interface that runs until user chooses to exit.
- Handle invalid inputs gracefully (e.g., non-numeric task numbers).
- Code must be modular, with functions like `load_tasks()`, `save_tasks()`, `add_task()`, `complete_task()`, `delete_task()`, `list_tasks()`.
- Include comments noting where Claude assisted.

## 4. User Stories
- **As a user**, I want to add tasks so I can remember things I need to do.
- **As a user**, I want to see my tasks with their statuses so I can track my progress.
- **As a user**, I want my tasks saved so I don't lose them when I close the app.

## 5. Acceptance Criteria
- Adding a task updates `tasks.json` immediately.
- Completing or deleting a task updates `tasks.json` immediately.
- Tasks persist between runs (closing and reopening the app retains tasks).
- Listing tasks shows their number, description, status, and due date (if set).
- Invalid task selections or inputs result in clear error messages.

## 6. Constraints
- Must run in Python 3.8+.
- Must store data in a JSON file named `tasks.json` in the same directory.
- No external dependencies beyond the standard library.

## 7. Deliverables
- `todo.py` Python file containing the program.
- `tasks.json` (created during runtime).
- Screenshot of sample run showing all four operations: add, complete, delete, list.

## 8. Lessons Learned
- Working with JSON for structured data storage.
- Implementing CRUD logic in a CLI environment.
- Designing a menu-driven interface for user interaction.
