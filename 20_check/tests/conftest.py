import os
import tempfile
import pytest
from app import create_app
from app.db import init_db, reset_database_path


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Reset database path cache before each test
    reset_database_path()
    
    # Create a temporary directory for test databases
    test_dir = tempfile.mkdtemp()
    
    # Set environment variables for testing
    os.environ["DATA_DIR"] = test_dir
    os.environ["TESTING"] = "true"
    
    # Create app in testing mode
    app = create_app('testing')
    
    # Initialize database manually for tests
    with app.app_context():
        init_db()
    
    yield app
    
    # Cleanup - remove all files in test directory
    import shutil
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    
    # Clean up environment variables and reset database path
    os.environ.pop("DATA_DIR", None)
    os.environ.pop("TESTING", None)
    reset_database_path()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture
def auth(client):
    """Authentication helper for tests."""
    class AuthActions:
        def __init__(self, client):
            self._client = client
        
        def register(self, email='test@example.com', password='testpass123'):
            """Register a new user."""
            return self._client.post(
                '/register',
                data={'email': email, 'password': password}
            )
        
        def login(self, email='test@example.com', password='testpass123'):
            """Login a user."""
            return self._client.post(
                '/login',
                data={'email': email, 'password': password}
            )
        
        def logout(self):
            """Logout the current user."""
            return self._client.get('/logout')
    
    return AuthActions(client)