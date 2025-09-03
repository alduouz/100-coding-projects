import pytest
import sqlite3
from app.db import get_conn, init_db, execute_query


def test_database_connection(app):
    """Test that database connection works."""
    with app.app_context():
        conn = get_conn()
        assert conn is not None
        conn.close()


def test_database_initialization(app):
    """Test that database tables are created."""
    with app.app_context():
        conn = get_conn()
        cursor = conn.cursor()
        
        # Check users table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        assert cursor.fetchone() is not None
        
        # Check notes table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='notes'")
        assert cursor.fetchone() is not None
        
        # Check foreign key constraints are enabled
        cursor.execute("PRAGMA foreign_keys")
        result = cursor.fetchone()
        assert result[0] == 1
        
        conn.close()


def test_execute_query_insert(app):
    """Test execute_query with insert operation."""
    with app.app_context():
        # Insert a test user
        result = execute_query(
            'INSERT INTO users (email, password_hash) VALUES (?, ?)',
            ('test@example.com', 'hashed_password')
        )
        assert result == 1  # One row affected
        
        # Verify user was inserted
        user = execute_query(
            'SELECT * FROM users WHERE email = ?',
            ('test@example.com',),
            fetch_one=True
        )
        assert user is not None
        assert user['email'] == 'test@example.com'


def test_execute_query_fetch_all(app):
    """Test execute_query with fetch_all option."""
    with app.app_context():
        # Insert multiple test users
        execute_query('INSERT INTO users (email, password_hash) VALUES (?, ?)', ('user1@example.com', 'hash1'))
        execute_query('INSERT INTO users (email, password_hash) VALUES (?, ?)', ('user2@example.com', 'hash2'))
        
        # Fetch all users
        users = execute_query('SELECT * FROM users', fetch_all=True)
        assert len(users) >= 2
        
        emails = [user['email'] for user in users]
        assert 'user1@example.com' in emails
        assert 'user2@example.com' in emails


def test_foreign_key_constraint(app):
    """Test that foreign key constraints work."""
    with app.app_context():
        # Insert a user first
        execute_query('INSERT INTO users (email, password_hash) VALUES (?, ?)', ('test@example.com', 'hash'))
        user = execute_query('SELECT * FROM users WHERE email = ?', ('test@example.com',), fetch_one=True)
        user_id = user['id']
        
        # Insert note with valid user_id
        execute_query(
            'INSERT INTO notes (content, user_id) VALUES (?, ?)',
            ('Test note', user_id)
        )
        
        # Try to insert note with invalid user_id (should fail)
        with pytest.raises(sqlite3.IntegrityError):
            execute_query(
                'INSERT INTO notes (content, user_id) VALUES (?, ?)',
                ('Invalid note', 999)
            )