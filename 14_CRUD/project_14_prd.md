# Project 14: Add Delete & Edit (CRUD) — PRD

## 1. Overview
Expand the Personal Notes App by allowing users to edit and delete notes. This completes the CRUD cycle (Create, Read, Update, Delete).

## 2. Functional Requirements
- **Edit functionality:**
  - Add an "Edit" button next to each note on the index page.
  - `/edit/<id>` route:
    - On GET: Display a form pre-filled with the note's current content.
    - On POST: Update the note's content in the database and redirect to `/`.

- **Delete functionality:**
  - Add a "Delete" button next to each note on the index page.
  - `/delete/<id>` route:
    - On GET: Show a confirmation page or inline confirmation.
    - On POST: Delete the note from the database and redirect to `/`.

- All database interactions must use parameterized queries to prevent SQL injection.

- Submission must include:
  - Updated `.py` file with routes for edit and delete.
  - Updated `index.html` with buttons/links for edit and delete.
  - New template(s) for edit and delete confirmation (e.g., `edit.html`, `confirm_delete.html`).
  - Screenshot showing edit and delete actions working.

## 3. Non-Functional Requirements
- Code should remain clean, readable, and follow PEP8.
- App must handle invalid IDs gracefully (e.g., non-existent notes should return 404 or a friendly error message).
- Deletion must require explicit user action (no accidental deletes).

## 4. User Stories
**As a** user,  
**I want** to edit or delete my notes,  
**So that** I can keep my list of notes up to date and accurate.

## 5. Acceptance Criteria
- Clicking "Edit" on a note shows a form with that note's content pre-filled.
- Submitting the edit form updates the note in the DB and redirects to `/`.
- Clicking "Delete" on a note prompts for confirmation, and upon confirmation, removes the note from the DB.
- After deleting, the note no longer appears in the list.
- Screenshots demonstrate both features working.

## 6. Notes
- Keep the same design style from previous projects for consistency.
- Use hidden form fields or URL parameters to pass the note ID.
