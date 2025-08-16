# Project 17: Search Function for Notes — PRD

## 1. Overview
Enhance the Personal Notes App by adding a search feature that allows users to filter their notes based on a keyword.

## 2. Functional Requirements
- Add a search bar to the notes index page (`index.html`).
- When a keyword is entered and submitted, filter notes that contain the keyword in their content.
- Case-insensitive search (use `LOWER(content)` or `LIKE`).
- Prevent SQL injection by using parameterized queries.
- Show a "No results found" message if no notes match the query.
- Routes:
  - Option A: Extend `/` to accept a query parameter (`?q=keyword`).
  - Option B: Create a new `/search` route to handle search queries.

- Submission must include:
  - Updated `.py` file with search route/query handling.
  - Updated `index.html` with a search form.
  - Screenshot showing successful search results.

## 3. Non-Functional Requirements
- Maintain clean, readable, PEP8-compliant code.
- Ensure consistent UX with the rest of the application (styling, navigation).
- Handle empty search queries gracefully (show all notes or prompt user).

## 4. User Stories
**As a** user,  
**I want** to search through my notes using keywords,  
**So that** I can quickly find specific information without scrolling manually.

## 5. Acceptance Criteria
- A search input is visible on the index page.
- Submitting a search filters notes by keyword and displays only matching notes.
- Searching with a keyword that has no matches displays "No results found".
- SQL queries use parameterized inputs to prevent injection attacks.

## 6. Notes
- Recommended implementation is to enhance the `/` route with a `q` query parameter (simpler than adding a separate `/search` route).
- Use `request.args.get("q")` in Flask to capture query input.
- Example SQL:
  ```sql
  SELECT * FROM notes WHERE user_id = ? AND LOWER(content) LIKE ? ORDER BY date DESC
  ```
  with `%keyword%` as the parameter.
