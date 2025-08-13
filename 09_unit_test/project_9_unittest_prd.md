
# Project 9: Unit Testing with unittest - PRD

## 1. Overview
Implement automated tests for the Project 8 OOP To-Do List application using Python's built-in `unittest` framework. The goal is to validate the core functionalities of both the `TaskManager` and the CLI interface, ensuring correctness, persistence, and user interaction.

## 2. Functional Requirements
### 2.1 TaskManager Tests
- **Add Task Test:**
  - Verify a task is added with the correct description, due date, and `completed=False` by default.
- **Complete Task Test:**
  - Add a task, mark it complete, and verify `completed=True`.
- **Delete Task Test:**
  - Add a task, delete it, and confirm it is removed from the list and returned by the delete method.
- **Persistence Test:**
  - Add tasks, save them, reload from disk, and confirm the loaded tasks match the saved data.

### 2.2 CLI Tests
- Simulate user input/output using injected `input_func` and `print_func`.
- **Basic Flow Test:**
  - Simulate: Add → List → Exit.
  - Verify output contains the added task and correct status symbols.
- Ensure no actual user interaction is needed during testing.

## 3. Non-functional Requirements
- Use only standard Python libraries: `unittest`, `tempfile`, `os`, `json`, `io`.
- Tests must not modify or depend on any real project files.
- Use `tempfile.TemporaryDirectory()` for storage isolation.
- Each test should be self-contained and independent.

## 4. User Stories
- **As a developer**, I want automated tests so that I can quickly verify my application's correctness after changes.
- **As a developer**, I want tests that do not require manual intervention so they can be run in CI/CD pipelines.

## 5. Acceptance Criteria
- Running `python -m unittest` in the project directory runs all tests and they all pass.
- Tests cover:
  - Adding, completing, and deleting tasks in `TaskManager`.
  - Persistence (save/load).
  - CLI interaction with injected I/O functions.
- No persistent files are left after test execution.

## 6. Constraints
- Python 3.8+.
- Only standard library modules allowed.
- Test files should be in a `tests/` directory or have `test_` prefix.

## 7. Deliverables
- `test_manager.py` containing TaskManager tests.
- `test_cli.py` containing CLI interaction tests.
- Optional `__init__.py` in tests folder for package structure.

## 8. Lessons Learned
- Using `unittest` to write structured test cases.
- Leveraging temporary directories and dependency injection for safe testing.
- Simulating CLI user interactions in an automated environment.
