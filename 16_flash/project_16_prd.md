# Project 16: Flash Messaging and Form Validation — PRD

## 1. Overview
Polish the Personal Notes App by adding user-visible feedback via Flask flash messages and robust server-side validation for all forms (notes + auth).

## 2. Functional Requirements
- **Flash Messaging**
  - Use `flash(message, category)` for success/error/info across key actions:
    - Notes: add, edit, delete
    - Auth: register, login, logout
  - Render flashed messages globally in the layout using `get_flashed_messages(with_categories=True)`.
  - Provide at least `success`, `error`, and `info` categories with distinct styles.

- **Validation (server-side)**
  - Notes: reject empty content and (recommended) enforce max length (e.g., 2000 chars). Show clear error messages.
  - Register: require email + password; handle duplicate email with a friendly error; enforce minimal password length (e.g., 6 chars).
  - Login: show error for invalid credentials.
  - If validation fails: show an error and keep the user on a helpful page (re-render or redirect with a flash message).

- **Submission must include**
  - Updated `.py` file with `flash()` calls and validation checks for add/edit/delete/register/login.
  - Updated `base.html` (or equivalent layout) that displays flashed messages.
  - Screenshots demonstrating: (1) success on add/edit/delete, (2) a validation error, and (3) an auth error (e.g., duplicate email or invalid login).

## 3. Non-Functional Requirements
- Set `SECRET_KEY` for sessions/flash (use env var with a dev fallback).
- Parameterize all SQL queries; never interpolate user input.
- Consistent UX copy and visual styling for messages.

## 4. User Stories
**As a** user,  
**I want** clear success/error messages and forms that guard against mistakes,  
**So that** I know what happened and how to fix issues immediately.

## 5. Acceptance Criteria
- Flash banners appear after add, edit, delete, register, login, and logout events.
- Submitting an empty note results in an error message and no DB write.
- Duplicate email registration shows a friendly error and does not create a new user.
- Invalid login shows an error; valid login shows success and loads the user’s notes.
- Visual differentiation of message categories (e.g., green for success, red for error).

## 6. Implementation Notes
- **Base layout**: add a flash block (example):
  ```jinja2
  {% with messages = get_flashed_messages(with_categories=True) %}
    {% if messages %}
      <div>
        {% for category, msg in messages %}
          <div class="flash {{ category }}">{{ msg }}</div>
        {% endfor %}
      </div>
    {% endif %}
  {% endwith %}
  ```
- **CSS (example)**: `.flash.success`, `.flash.error`, `.flash.info` with distinct colors.
- **Validation**: prefer redirect-after-POST paired with flash; for inline errors, re-render the template with an `error` variable.
- **Security**: never store plaintext passwords; keep using `generate_password_hash`/`check_password_hash`.
