
# Project 5: Contact Book with File Storage

## 1. Objective
Build a command-line contact book application with persistent storage using a file. The app will support basic CRUD operations, input validation, and menu-based navigation.

## 2. Core Features
1. **Add Contact** — User can add a new contact with name, phone number, and optional email.
2. **View All Contacts** — Display all stored contacts in a readable table format.
3. **Search Contact** — Search by name (partial match allowed).
4. **Update Contact** — Modify an existing contact's details.
5. **Delete Contact** — Remove a contact by name.
6. **Exit** — Save all changes before exiting.

## 3. Data Structure
Each contact will be stored as a dictionary:
```python
{
    "name": "John Doe",
    "phone": "1234567890",
    "email": "john@example.com"
}
```
Contacts will be stored in a list, which will be serialized to a file (JSON or CSV).

## 4. File Handling
- On start:
  - If the file exists, load contacts into memory.
  - If not, create an empty file.
- On exit:
  - Save the contacts back to the file.

## 5. Input Validation
- **Name**: Must not be empty.
- **Phone**: Must be numeric (allow spaces/dashes but strip them internally).
- **Email**: Optional, must contain `@` if provided.

## 6. Incremental Lessons from Previous Projects
- Continue using `input_func` and `print_func` for dependency injection to support testing.
- Add file persistence for the first time.
- Implement CRUD pattern and search functionality.

## 7. Testing Requirements
- Use mock input/output to test all functions without manual interaction.
- Use temporary files or `io.StringIO` for file operations in tests.
- Test all CRUD operations and file save/load logic.

## 8. Stretch Goals
- Sort contacts alphabetically before displaying.
- Support multiple file formats (JSON, CSV).
- Add export option to `.txt` file.
