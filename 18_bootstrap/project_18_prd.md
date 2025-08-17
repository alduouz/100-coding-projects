# Project 18: Responsive Styling (Bootstrap) — PRD

## 1. Overview
Upgrade the Personal Notes App’s UI using Bootstrap so it looks professional and works well on mobile. Keep all existing functionality (auth, CRUD, search).

## 2. Functional Requirements
- Integrate **Bootstrap 5** via CDN in the base layout.
- Convert current pages to use Bootstrap components and utilities:
  - Navbar with brand + auth links (Login/Logout/Register), search form in navbar or header.
  - Container/grid layout for responsive spacing.
  - Buttons (`btn`, `btn-primary`, `btn-danger`, `btn-secondary`, `btn-success`).
  - Forms (`form-control`, `form-label`) for add/edit/register/login/search.
  - Notes list using **Cards** (`.card`, `.card-body`, optional `.card-subtitle` for date).
  - Flash messages as dismissible **Alerts** (`.alert`, `.alert-success`, `.alert-danger`, `.alert-info`).
- Maintain existing routes and logic; this project is **UI-only**.
- Submission must include:
  - Updated templates (at least `base.html`, `index.html`, `add.html`, `edit.html`, `login.html`, `register.html`, `confirm_delete.html`).
  - Screenshot(s) showing responsive behavior on a narrow viewport (mobile).

## 3. Non-Functional Requirements
- Responsive at common breakpoints (≥ 360px width).
- Consistent visual hierarchy (headings, spacing, button styles).
- Keep custom CSS minimal; prefer Bootstrap utilities and components.
- No blocking of core keyboard navigation and accessibility (labels, alt text for icons if used).

## 4. User Stories
**As a** user on my phone,  
**I want** the app to look clean and readable with clear actions,  
**So that** I can add, edit, delete, and search notes easily on mobile.

## 5. Acceptance Criteria
- The app uses Bootstrap 5 via CDN and renders with Bootstrap styles.
- Forms and buttons use Bootstrap classes (`form-control`, `btn`, etc.).
- Notes are presented in Bootstrap cards with readable spacing on mobile.
- Flash messages appear as Bootstrap alerts.
- Navbar collapses on small screens (hamburger menu) or a simplified mobile header is used.
- Screenshots show mobile-friendly rendering without horizontal scrolling.

## 6. Implementation Notes
- Add Bootstrap CDN in `base.html`:
  ```html
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
  ```
- Convert your flash block to alerts:
  ```jinja2
  {% with messages = get_flashed_messages(with_categories=True) %}
    {% if messages %}
      {% for category, msg in messages %}
        <div class="alert alert-{{ 'danger' if category == 'error' else category }} alert-dismissible fade show" role="alert">
          {{ msg }}
          <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
      {% endfor %}
    {% endif %}
  {% endwith %}
  ```
- Example card markup for a note:
  ```html
  <div class="card mb-3">
    <div class="card-body">
      <p class="card-text">{{ note.content }}</p>
      <p class="card-subtitle text-muted small text-end">{{ note.date }}</p>
      <div class="d-flex gap-2">
        <a href="{{ url_for('edit_note', note_id=note.id) }}" class="btn btn-success btn-sm">Edit</a>
        <a href="{{ url_for('delete_note', note_id=note.id) }}" class="btn btn-danger btn-sm">Delete</a>
      </div>
    </div>
  </div>
  ```
- Use spacing utilities (`mt-`, `mb-`, `p-`, `gap-`, `container`, `row`, `col`) instead of custom CSS.
