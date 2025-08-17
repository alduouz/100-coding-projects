# Project 19: Deploy Notes App to Render or Railway — PRD

## 1. Overview
Deploy the Flask Notes App publicly on a PaaS (Render or Railway). The app must be accessible via a public URL and remain functional with auth, CRUD, search, and Bootstrap UI.

## 2. Functional Requirements
- Host the Flask app on **Render** or **Railway** (or similar) with a **public URL**.
- The app must run behind a production WSGI server (**gunicorn**).
- Keep existing features working (register/login/logout; add/edit/delete/search notes; flash messages; Bootstrap).
- **Data persistence**:
  - Option A (fast): SQLite with **persistent disk/volume** attached to your service.
  - Option B (recommended long‑term): Migrate to a managed DB (e.g., PostgreSQL on Railway or MySQL on PlanetScale).

## 3. Deliverables
- Public URL (e.g., https://your-notes-app.onrender.com/).
- Repository with deployment files:
  - `requirements.txt` (must include `Flask` and `gunicorn`).
  - `Procfile` (e.g., `web: gunicorn app:app`).
  - (If Render) `render.yaml` optional but helpful for infra as code.
  - (If Railway) service settings documented (env vars, deploy command).
- Screenshot(s) of the live site (home page + login + notes list).

## 4. Non-Functional Requirements
- The app must boot within 90 seconds on cold starts.
- Uses environment variables for any secrets (e.g., `SECRET_KEY`).
- Production behavior (no debug mode in production).

## 5. User Stories
**As a** user,  
**I want** to access my Notes App via a public URL,  
**So that** I can use it on any device without running it locally.

## 6. Acceptance Criteria
- A public URL is reachable and serves the Notes App pages.
- Login/register works; notes can be created/edited/deleted/searched.
- Data remains after an app restart:
  - If using SQLite: verified persistent disk/volume is mounted and mapped to `notes.db` location.
  - If using managed DB: notes are stored and persist across restarts/redeploys.
- App runs with `gunicorn` (visible in logs or via Procfile).
- `SECRET_KEY` is set from environment, not hardcoded.

## 7. Implementation Notes

### Minimal files
- **requirements.txt**
  ```txt
  Flask==2.3.3
  gunicorn==21.2.0
  ```

- **Procfile**
  ```procfile
  web: gunicorn app:app
  ```

- **Environment variable**
  - `SECRET_KEY` = a strong random value set in the PaaS dashboard.

### Render (example)
1. Push repo to GitHub.
2. Create **Web Service** → connect repo.
3. Build command: *(leave default)*
4. Start command: `gunicorn app:app`
5. **Persistent disk**: add a disk (e.g., `/opt/render/project/src/data`, size 1GB) and store DB at that path.
   - Update code to place `notes.db` in that folder:
     ```python
     DATA_DIR = os.environ.get("DATA_DIR", "data")
     os.makedirs(DATA_DIR, exist_ok=True)
     DATABASE_NAME = os.path.join(DATA_DIR, "notes.db")
     ```
6. Set env vars: `SECRET_KEY=...`

### Railway (example)
1. New **Service** from GitHub.
2. Start command: `gunicorn app:app`
3. Add **Volume** and mount (e.g., `/data`) then point DB file there (same pattern as above).
4. Set env vars: `SECRET_KEY=...`

### Optional: Managed DB
- Create a Postgres/MySQL instance; add env vars (`DATABASE_URL`).
- Replace SQLite code with a small DB layer (SQLAlchemy recommended).

## 8. Smoke Test Checklist
- Visit `/register`, create a user → success.
- Login → redirected to index, see empty notes.
- Add a note, refresh → note appears.
- Redeploy/restart service → note still present (persistence verified).
- Search for a keyword → filtered results shown.
- Edit + delete work as expected.
