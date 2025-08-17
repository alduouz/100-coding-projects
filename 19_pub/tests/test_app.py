import pytest
from app import create_app


def test_create_app():
    """Test that the app factory creates an app instance."""
    app = create_app('testing')
    assert app is not None
    assert app.config['TESTING'] is True


def test_app_blueprints(app):
    """Test that blueprints are registered."""
    blueprint_names = [bp.name for bp in app.blueprints.values()]
    assert 'auth' in blueprint_names
    assert 'notes' in blueprint_names


def test_error_handlers(client):
    """Test that error handlers work."""
    # Test 404 error handler
    response = client.get('/nonexistent-page')
    assert response.status_code == 404
    assert b'Page Not Found' in response.data


def test_root_redirect(client):
    """Test that root redirects appropriately."""
    # Should redirect to login when not authenticated
    response = client.get('/')
    assert response.status_code == 302
    assert '/login' in response.location


def test_root_redirect_authenticated(client, auth):
    """Test that root shows notes when authenticated."""
    auth.register()
    auth.login()
    
    response = client.get('/')
    assert response.status_code == 200
    assert b'My Notes' in response.data


def test_smoke_test_full_workflow(client, auth):
    """Smoke test: complete user workflow."""
    # Register
    response = auth.register()
    assert response.status_code == 302
    
    # Login
    response = auth.login()
    assert response.status_code == 302
    
    # View notes page
    response = client.get('/')
    assert response.status_code == 200
    
    # Add a note
    response = client.post('/add', data={'content': 'My first note'})
    assert response.status_code == 302
    
    # View notes with new note
    response = client.get('/')
    assert response.status_code == 200
    assert b'My first note' in response.data
    
    # Search for note
    response = client.get('/?q=first')
    assert response.status_code == 200
    assert b'My first note' in response.data
    
    # Logout
    response = auth.logout()
    assert response.status_code == 302
    
    # Verify redirect to login after logout
    response = client.get('/')
    assert response.status_code == 302
    assert '/login' in response.location