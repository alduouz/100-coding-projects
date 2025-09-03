import pytest
from flask import session
from app.auth import get_user_by_email


def test_register_page(client):
    """Test that register page loads."""
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data


def test_register_valid_user(client):
    """Test registering a valid user."""
    response = client.post('/register', data={
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    assert response.status_code == 302  # Redirect to login
    
    # Check user was created
    with client.application.app_context():
        user = get_user_by_email('test@example.com')
        assert user is not None
        assert user['email'] == 'test@example.com'


def test_register_invalid_email(client):
    """Test registering with invalid email."""
    response = client.post('/register', data={
        'email': '',
        'password': 'testpass123'
    })
    assert response.status_code == 200
    assert b'Email and password are required' in response.data


def test_register_short_password(client):
    """Test registering with short password."""
    response = client.post('/register', data={
        'email': 'test@example.com',
        'password': '123'
    })
    assert response.status_code == 200
    assert b'Password must be at least 6 characters' in response.data


def test_register_duplicate_email(client, auth):
    """Test registering with duplicate email."""
    # Register first user
    auth.register()
    
    # Try to register again with same email
    response = client.post('/register', data={
        'email': 'test@example.com',
        'password': 'anotherpass123'
    })
    assert response.status_code == 200
    assert b'Email already registered' in response.data


def test_login_page(client):
    """Test that login page loads."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data


def test_login_valid_user(client, auth):
    """Test logging in with valid credentials."""
    # Register a user first
    auth.register()
    
    # Login
    response = auth.login()
    assert response.status_code == 302  # Redirect to notes
    
    # Check session
    with client.session_transaction() as sess:
        assert 'user_id' in sess
        assert sess['user_email'] == 'test@example.com'


def test_login_invalid_email(client):
    """Test logging in with invalid email."""
    response = client.post('/login', data={
        'email': 'nonexistent@example.com',
        'password': 'testpass123'
    })
    assert response.status_code == 200
    assert b'Invalid email or password' in response.data


def test_login_invalid_password(client, auth):
    """Test logging in with invalid password."""
    # Register a user first
    auth.register()
    
    # Try to login with wrong password
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 200
    assert b'Invalid email or password' in response.data


def test_login_missing_fields(client):
    """Test logging in with missing fields."""
    response = client.post('/login', data={
        'email': '',
        'password': ''
    })
    assert response.status_code == 200
    assert b'Email and password are required' in response.data


def test_logout(client, auth):
    """Test logging out."""
    # Register and login
    auth.register()
    auth.login()
    
    # Logout
    response = auth.logout()
    assert response.status_code == 302  # Redirect to login
    
    # Check session is cleared
    with client.session_transaction() as sess:
        assert 'user_id' not in sess


def test_login_required_decorator(client):
    """Test that login_required decorator works."""
    # Try to access protected route without login
    response = client.get('/')
    assert response.status_code == 302  # Redirect to login
    assert '/login' in response.location