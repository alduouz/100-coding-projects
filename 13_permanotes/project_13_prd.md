# Project 13: Add Persistent Notes (SQLite) — PRD

## 1. Overview
Upgrade the Personal Notes App by adding SQLite database support to persist notes even after the server restarts.

## 2. Functional Requirements
- Create a SQLite database file (e.g., `notes.db`) with a table `notes` having at least:
  - `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
  - `content` (TEXT)
  - `date` (TIMESTAMP or TEXT)
- `/` route:
  - Fetch and display all notes from the database in descending order of date (latest first).
- `/add` route:
  - On GET: Show the add note form.
  - On POST: Insert the new note into the database with the current date/time, then redirect to `/`.
- Database and table should be created automatically if they don't exist.
- Submission must include:
  - `.py` file(s)
  - `.db` file (with at least one example note)
  - Updated `requirements.txt` if any new dependencies are added
  - Screenshot showing the app with notes after a restart

## 3. Non-Functional Requirements
- Code must be clean, readable, and follow PEP8 style guidelines.
- All database operations should be parameterized to avoid SQL injection.
- App must start without errors and function consistently across restarts.

## 4. User Stories
**As a** user,  
**I want** my notes to be saved in a database,  
**So that** they are available even if the app restarts or my computer is turned off.

## 5. Acceptance Criteria
- Visiting `/` shows all notes stored in the database.
- Adding a note via `/add` inserts it into the database.
- Data persists after stopping and restarting the server.
- The `.db` file contains the inserted notes.

## 6. Notes
- You may use the built-in `sqlite3` library or SQLAlchemy ORM.
- Keep HTML templates from Project 12; only back-end storage changes.
