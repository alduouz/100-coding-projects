# Personal Notes App

A secure, multi-user Flask web application for creating, editing, and managing personal notes. The application features user authentication, note CRUD operations, search functionality, and responsive Bootstrap UI.

## Features

- **User Authentication**: Secure registration and login with password hashing
- **Note Management**: Create, read, update, and delete personal notes
- **Search**: Find notes by content using case-insensitive search
- **User Isolation**: Each user can only access their own notes
- **Responsive UI**: Bootstrap-based interface that works on all devices
- **Security**: Session management, CSRF protection, and secure headers

## Technology Stack

- **Backend**: Flask 2.3.3 with SQLite database
- **Frontend**: Bootstrap 5.3.3 with Jinja2 templates
- **Authentication**: Werkzeug password hashing
- **Testing**: pytest with comprehensive test coverage
- **Deployment**: Gunicorn WSGI server

## Project Structure

```
app/
├── __init__.py          # App factory and configuration
├── auth.py              # Authentication blueprint (register/login/logout)
├── notes.py             # Notes management blueprint (CRUD operations)
├── db.py                # Database connection and initialization
└── templates/
    ├── base.html        # Base template with navigation
    ├── index.html       # Notes listing with search
    ├── add.html         # Add new note form
    ├── edit.html        # Edit existing note form
    ├── login.html       # User login form
    ├── register.html    # User registration form
    ├── confirm_delete.html  # Delete confirmation
    └── errors/
        ├── 404.html     # Page not found
        └── 500.html     # Server error

config.py                # Configuration classes for different environments
wsgi.py                  # WSGI entry point for production
requirements.txt         # Python dependencies
tests/                   # Comprehensive test suite
├── conftest.py          # Test fixtures and configuration
├── test_auth.py         # Authentication tests
├── test_notes.py        # Notes management tests
├── test_db.py           # Database tests
└── test_app.py          # Application and smoke tests
```

## Setup Instructions

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd personal-notes-app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**
   ```bash
   export SECRET_KEY="your-secret-key-here"
   export DATA_DIR="./data"  # Optional, defaults to current directory
   export FLASK_ENV="development"
   ```

5. **Run the application**
   ```bash
   # Using Flask development server
   flask --app wsgi run --debug

   # Or using the WSGI file directly
   python wsgi.py
   ```

6. **Access the application**
   - Open your browser to `http://localhost:5000`
   - Register a new account or login with existing credentials

### Production Deployment

#### Railway Deployment

1. **Set environment variables in Railway dashboard**:
   - `SECRET_KEY`: Generate a secure random string
   - `DATA_DIR`: `/app/data` (or use Railway's volume mount)
   - `FLASK_ENV`: `production`
   - `HTTPS_ENABLED`: `true` (for secure cookies)

2. **Database persistence**:
   - The app uses SQLite stored in `DATA_DIR`
   - For persistence, mount a volume or use Railway's disk storage
   - Database file: `{DATA_DIR}/notes.db`

3. **Start command**: `gunicorn wsgi:app`

#### Other Platforms (Render, Heroku, etc.)

1. **Procfile** (included):
   ```
   web: gunicorn wsgi:app
   ```

2. **Environment variables**:
   ```
   SECRET_KEY=your-production-secret-key
   DATA_DIR=/app/data
   FLASK_ENV=production
   HTTPS_ENABLED=true
   ```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | Yes | `dev-secret-key-change-in-production` | Flask secret key for sessions |
| `DATA_DIR` | No | `.` | Directory for SQLite database file |
| `FLASK_ENV` | No | `default` | Environment: `development`, `production`, `testing` |
| `HTTPS_ENABLED` | No | `False` | Set to `true` to enable secure cookies |
| `PORT` | No | `8080` | Port for the application to listen on |

## Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

### Test Coverage

The test suite includes:
- **Authentication tests**: Registration, login, logout, validation
- **Notes management tests**: CRUD operations, search, user isolation
- **Database tests**: Connection, initialization, constraints
- **Application tests**: Error handling, blueprints, security
- **Smoke tests**: End-to-end user workflows

## Security Features

- **Password Security**: PBKDF2 hashing with salt
- **Session Management**: HTTPOnly, SameSite cookies
- **CSRF Protection**: Built-in Flask-WTF protection
- **SQL Injection Prevention**: Parameterized queries
- **User Isolation**: Users can only access their own data
- **Security Headers**: XSS protection, content type validation
- **Input Validation**: Form validation and length limits

## Development Notes

### Database Schema

```sql
-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

-- Notes table
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

### Configuration

The app uses a configuration class system:
- `DevelopmentConfig`: Debug enabled, verbose logging
- `ProductionConfig`: Security headers, secure cookies
- `TestingConfig`: Isolated test database, debug enabled

### Logging

- **Development**: DEBUG level with detailed formatting
- **Production**: INFO level with structured logging
- **Events logged**: User registration, login, database operations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the test suite for examples
2. Review the configuration options
3. Check application logs for debugging
4. Open an issue in the repository