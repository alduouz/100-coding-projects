# Project 20: Feature Review & Claude Refactoring Session — PRD

## 1) Overview
Conduct a structured code review and refactor of your Flask Notes App using an AI assistant (e.g., Claude). The goal is to improve maintainability, structure, and code quality without changing core features (auth, CRUD, search, Bootstrap, deployment).

## 2) Objectives
- Identify design/architecture issues (tight coupling, duplicated logic, long functions, magic values).
- Improve project structure (blueprints or modular files), configuration management, error handling, logging, and tests.
- Document the app (README) and provide a clear local + production setup.

## 3) Scope (What to Review)
- **Application structure** (single-file vs. modular)
- **Routes & views** (clarity, duplication, validation)
- **Database layer** (connection handling, queries, constraints)
- **Templates** (layout reuse, context variables, Bootstrap)
- **Security** (session config, cookie flags, password hashing already done)
- **Config & env management**
- **Error handling** (4xx/5xx pages)
- **Logging & observability** (basic logs)
- **Tests** (unit + a simple integration smoke test)

## 4) Deliverables
1. **Before/After Summary** (1–2 pages): key issues found + refactor decisions and outcomes.
2. **Refactored Codebase** organized like:
   ```
   app/
     __init__.py          # create_app factory, config, blueprints registration
     db.py                # get_conn(), init_db(), query helpers
     auth.py              # register/login/logout routes (Blueprint)
     notes.py             # index/add/edit/delete routes (Blueprint)
     models.py (optional) # data access helpers
     templates/
       base.html, index.html, add.html, edit.html, login.html, register.html, confirm_delete.html
     static/ (optional)
   config.py              # Config classes (Dev/Prod/Test), SECRET_KEY and DATA_DIR via env
   wsgi.py                # from app import create_app; app = create_app()
   requirements.txt
   Procfile
   README.md
   tests/
     test_auth.py
     test_notes.py
     conftest.py         # pytest fixtures for app + temp DB
   ```
3. **README.md** with:
   - Setup (local + Railway)
   - Env vars (`SECRET_KEY`, `DATA_DIR`) and why they matter
   - How to run tests
   - Deployment notes (gunicorn, volume mount)
4. **Tests**:
   - Unit tests for auth (register/login), notes (add/edit/delete/search), and minimal DB.
   - A smoke test that starts the app in test mode and verifies a simple flow.

## 5) Functional Constraints
- Preserve existing features (auth, notes CRUD, search, flash messages, Bootstrap UI).
- Keep SQLite for now (persistence through DATA_DIR) unless you explicitly choose to migrate to Postgres.
- Do not change behavior or routes unless the change is documented and justified.

## 6) Acceptance Criteria
- Project runs locally (`flask run` or `python -m flask --app app` via create_app) and in production (`gunicorn wsgi:app`).
- Blueprints registered for `auth` and `notes` modules.
- `create_app()` factory configures app with env-driven `SECRET_KEY` and `DATA_DIR`.
- Database initialization executed on first request or app factory; foreign keys enabled.
- Parameterized SQL everywhere; no string interpolation of user input.
- Flash messaging & validation preserved across all forms.
- Custom 404/500 error handlers present; `/health` route responds 200 in prod.
- Basic logging to stdout (INFO) and errors captured in logs.
- Tests pass locally (`pytest -q`) with an isolated temp DB (not the production file).
- README includes clear instructions and rationale for refactors.
- A short **Before/After** document summarizes improvements.

## 7) Suggested Refactors (Menu)
- **App factory:** move from single-file to `create_app()` pattern in `app/__init__.py`.
- **Blueprints:** split `auth` and `notes` into separate modules; register in `create_app()`.
- **DB helpers:** a `db.py` to centralize `get_conn()`, `init_db()`, and PRAGMA settings.
- **Config classes:** `config.py` with `DevelopmentConfig`, `ProductionConfig`, `TestingConfig` (reads env vars).
- **Security polish:** set `SESSION_COOKIE_HTTPONLY=True`, `SESSION_COOKIE_SAMESITE="Lax"`, and `SESSION_COOKIE_SECURE` in prod.
- **Error pages:** `errorhandler(404)` and `errorhandler(500)` templates.
- **Logging:** `logging.basicConfig(level=logging.INFO)` and log connect/init events.
- **Tests:** pytest fixtures to spin up a temp SQLite DB (in-memory or NamedTemporaryFile), plus route tests.

## 8) Example AI Prompts (copy/paste to Claude)
- *“Here’s my Flask notes app repo (pasted below). Identify structural issues and suggest a modular blueprint-based layout.”*
- *“Generate a minimal create_app factory with blueprints for auth and notes, using env variables for SECRET_KEY and DATA_DIR.”*
- *“Refactor my database layer into db.py with get_conn(), init_db(), and PRAGMA foreign_keys=ON. Replace direct connections in routes.”*
- *“Propose a pytest setup with fixtures to create a temp DB and write tests for register/login and add/edit/delete/search.”*
- *“Write a concise README describing local setup, env vars, volume mount in Railway, and start commands.”*
- *“Draft a Before/After summary capturing changes and benefits (maintainability, safety, clarity).”*

## 9) Testing Notes (pytest sketch)
```python
# tests/conftest.py
import os, tempfile, pytest
from app import create_app, db

@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    os.environ["DATA_DIR"] = os.path.dirname(db_path)
    app = create_app({"TESTING": True, "SECRET_KEY": "test-secret"})
    with app.test_client() as client:
        with app.app_context():
            db.init_db()
        yield client
    os.close(db_fd)
    os.remove(db_path)
```

## 10) Definition of Done
- ✅ Codebase organized with app factory + blueprints
- ✅ Tests pass locally
- ✅ README and Before/After doc committed
- ✅ Deployed version unchanged in behavior, but code is cleaner, modular, and easier to extend
