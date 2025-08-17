import pytest
from app.notes import get_note_by_id
from app.db import execute_query


def test_index_redirect_when_not_logged_in(client):
    """Test that index redirects to login when not authenticated."""
    response = client.get('/')
    assert response.status_code == 302
    assert '/login' in response.location


def test_index_page_when_logged_in(client, auth):
    """Test that index page loads when authenticated."""
    auth.register()
    auth.login()
    
    response = client.get('/')
    assert response.status_code == 200
    assert b'My Notes' in response.data


def test_add_note_page(client, auth):
    """Test that add note page loads."""
    auth.register()
    auth.login()
    
    response = client.get('/add')
    assert response.status_code == 200
    assert b'Add a New Note' in response.data


def test_add_note_valid(client, auth):
    """Test adding a valid note."""
    auth.register()
    auth.login()
    
    response = client.post('/add', data={
        'content': 'This is a test note'
    })
    assert response.status_code == 302  # Redirect to index
    
    # Check note was created
    with client.application.app_context():
        notes = execute_query('SELECT * FROM notes WHERE content = ?', ('This is a test note',), fetch_all=True)
        assert len(notes) == 1
        assert notes[0]['content'] == 'This is a test note'


def test_add_note_empty_content(client, auth):
    """Test adding note with empty content."""
    auth.register()
    auth.login()
    
    response = client.post('/add', data={
        'content': ''
    })
    assert response.status_code == 200
    assert b'Note content cannot be empty' in response.data


def test_add_note_too_long(client, auth):
    """Test adding note with content too long."""
    auth.register()
    auth.login()
    
    long_content = 'x' * 2001
    response = client.post('/add', data={
        'content': long_content
    })
    assert response.status_code == 200
    assert b'Note content cannot exceed 2000 characters' in response.data


def test_edit_note_page(client, auth):
    """Test that edit note page loads."""
    auth.register()
    auth.login()
    
    # Add a note first
    client.post('/add', data={'content': 'Original content'})
    
    # Get the note ID
    with client.application.app_context():
        note = execute_query('SELECT * FROM notes WHERE content = ?', ('Original content',), fetch_one=True)
        note_id = note['id']
    
    response = client.get(f'/edit/{note_id}')
    assert response.status_code == 200
    assert b'Original content' in response.data


def test_edit_note_valid(client, auth):
    """Test editing a note with valid content."""
    auth.register()
    auth.login()
    
    # Add a note first
    client.post('/add', data={'content': 'Original content'})
    
    # Get the note ID
    with client.application.app_context():
        note = execute_query('SELECT * FROM notes WHERE content = ?', ('Original content',), fetch_one=True)
        note_id = note['id']
    
    # Edit the note
    response = client.post(f'/edit/{note_id}', data={
        'content': 'Updated content'
    })
    assert response.status_code == 302  # Redirect to index
    
    # Check note was updated
    with client.application.app_context():
        updated_note = execute_query('SELECT * FROM notes WHERE id = ?', (note_id,), fetch_one=True)
        assert updated_note['content'] == 'Updated content'


def test_edit_note_empty_content(client, auth):
    """Test editing note with empty content."""
    auth.register()
    auth.login()
    
    # Add a note first
    client.post('/add', data={'content': 'Original content'})
    
    # Get the note ID
    with client.application.app_context():
        note = execute_query('SELECT * FROM notes WHERE content = ?', ('Original content',), fetch_one=True)
        note_id = note['id']
    
    # Try to edit with empty content
    response = client.post(f'/edit/{note_id}', data={
        'content': ''
    })
    assert response.status_code == 200
    assert b'Note content cannot be empty' in response.data


def test_edit_nonexistent_note(client, auth):
    """Test editing a note that doesn't exist."""
    auth.register()
    auth.login()
    
    response = client.get('/edit/999')
    assert response.status_code == 404


def test_delete_note_page(client, auth):
    """Test that delete confirmation page loads."""
    auth.register()
    auth.login()
    
    # Add a note first
    client.post('/add', data={'content': 'To be deleted'})
    
    # Get the note ID
    with client.application.app_context():
        note = execute_query('SELECT * FROM notes WHERE content = ?', ('To be deleted',), fetch_one=True)
        note_id = note['id']
    
    response = client.get(f'/delete/{note_id}')
    assert response.status_code == 200
    assert b'To be deleted' in response.data
    assert b'Are you sure' in response.data


def test_delete_note_confirm(client, auth):
    """Test confirming note deletion."""
    auth.register()
    auth.login()
    
    # Add a note first
    client.post('/add', data={'content': 'To be deleted'})
    
    # Get the note ID
    with client.application.app_context():
        note = execute_query('SELECT * FROM notes WHERE content = ?', ('To be deleted',), fetch_one=True)
        note_id = note['id']
    
    # Delete the note
    response = client.post(f'/delete/{note_id}')
    assert response.status_code == 302  # Redirect to index
    
    # Check note was deleted
    with client.application.app_context():
        deleted_note = execute_query('SELECT * FROM notes WHERE id = ?', (note_id,), fetch_one=True)
        assert deleted_note is None


def test_delete_nonexistent_note(client, auth):
    """Test deleting a note that doesn't exist."""
    auth.register()
    auth.login()
    
    response = client.get('/delete/999')
    assert response.status_code == 404


def test_search_notes(client, auth):
    """Test searching for notes."""
    auth.register()
    auth.login()
    
    # Add some notes
    client.post('/add', data={'content': 'Python programming notes'})
    client.post('/add', data={'content': 'JavaScript tutorial'})
    client.post('/add', data={'content': 'Database design patterns'})
    
    # Search for 'python'
    response = client.get('/?q=python')
    assert response.status_code == 200
    assert b'Python programming notes' in response.data
    assert b'JavaScript tutorial' not in response.data
    assert b'Database design patterns' not in response.data


def test_user_isolation(client, auth):
    """Test that users can only see their own notes."""
    # Register and login first user
    auth.register('user1@example.com', 'password123')
    auth.login('user1@example.com', 'password123')
    client.post('/add', data={'content': 'User 1 note'})
    auth.logout()
    
    # Register and login second user
    auth.register('user2@example.com', 'password123')
    auth.login('user2@example.com', 'password123')
    client.post('/add', data={'content': 'User 2 note'})
    
    # Check that user 2 only sees their own note
    response = client.get('/')
    assert b'User 2 note' in response.data
    assert b'User 1 note' not in response.data


def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'healthy'