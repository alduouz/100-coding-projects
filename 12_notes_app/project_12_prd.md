# Project 12: Personal Notes App (Flask + HTML Templates) — PRD

## 1. Overview
This project builds a simple Flask web application that allows users to add personal notes and view them in a list. The goal is to introduce HTML templating, forms, and basic GET/POST request handling.

## 2. Functional Requirements
- Routes:
  - `/` : Displays a list of all notes.
  - `/add` : Displays a form for adding a new note and handles form submission.
- Notes are stored **in memory** (e.g., a Python list or dictionary).
- Use Jinja2 HTML templates stored in a `templates/` folder.
- The `/add` route must handle both GET (display form) and POST (process form) requests.
- Include comments in the code attributing assistance from Claude.
- Submission must include:
  - `.py` file(s)
  - `templates/` folder with HTML files
  - Screenshot showing the app working in a browser

## 3. Non-Functional Requirements
- Code must be clean, readable, and follow PEP8 style guidelines.
- App must start without errors using Flask's built-in server.
- Pages should have basic styling for readability.

## 4. User Stories
**As a** user,  
**I want** to add text notes via a form and view them in a list,  
**So that** I can quickly jot down and see my personal notes.

## 5. Acceptance Criteria
- Visiting `/` shows all added notes.
- Visiting `/add` shows a form to input a note.
- Submitting the form adds the note to memory and redirects to `/`.
- App runs without syntax or runtime errors.
- Screenshot proof provided.

## 6. Notes
- No database is required yet; persistence is not necessary.
- Keep HTML simple but well-structured.
