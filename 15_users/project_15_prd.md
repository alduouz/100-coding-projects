# Project 15: User Registration and Login (Flask Auth) — PRD

## 1. Overview
Upgrade the Personal Notes App by adding user authentication (registration and login) so each user can manage their own notes.

## 2. Functional Requirements
- Add a `users` table with:
  - `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
  - `email` (TEXT UNIQUE, NOT NULL)
  - `password_hash` (TEXT, NOT NULL)

- Update the `notes` table to include:
  - `user_id` (INTEGER, FOREIGN KEY referencing users.id)

- Routes:
  - `/register`
    - GET: Show registration form
    - POST: Save new user with hashed password
  - `/login`
    - GET: Show login form
    - POST: Validate email/password, start session
  - `/logout`
    - Clear session and redirect to login

- Notes management:
  - Only show notes belonging to the logged-in user.
  - All CRUD routes (`/`, `/add`, `/edit/<id>`, `/delete/<id>`) must check for a logged-in user.

- Use `werkzeug.security` functions (`generate_password_hash`, `check_password_hash`) for secure password storage and validation.

- Submission must include:
  - Updated `.py` file with user authentication and session management
  - Updated templates (`register.html`, `login.html`, updated navbar with login/logout links)

## 3. Non-Functional Requirements
- Code must follow PEP8 style.
- Passwords must never be stored in plain text.
- Handle duplicate email registrations gracefully.
- Protect routes from unauthorized access (redirect to `/login` if not logged in).

## 4. User Stories
**As a** user,  
**I want** to register an account and log in,  
**So that** I can securely manage my own private notes separate from other users.

## 5. Acceptance Criteria
- Registering a new account saves the user with hashed password in DB.
- Logging in with valid credentials starts a session and shows only that user’s notes.
- Logging out ends the session and requires login to access notes.
- Attempting to access `/`, `/add`, `/edit`, or `/delete` without login redirects to `/login`.
- Screenshots show different users with different sets of notes.

## 6. Notes
- Use Flask’s built-in session system (no need for Flask-Login unless you prefer).
- Start with SQLite migration: add a `users` table and a `user_id` column to `notes`.
- Keep design consistent with prior projects.
