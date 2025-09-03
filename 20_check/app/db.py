import sqlite3
import os
import logging
from pathlib import Path


logger = logging.getLogger(__name__)


# Cache the database path for consistency during testing
_database_path = None

def get_database_path():
    """Get the database file path from configuration."""
    global _database_path
    
    # Return cached path if available
    if _database_path is not None:
        return _database_path
    
    data_dir = os.environ.get("DATA_DIR", ".")
    
    try:
        os.makedirs(data_dir, exist_ok=True)
        # Test write permissions only in non-test environments
        if not os.environ.get("TESTING"):
            test_file = os.path.join(data_dir, "test_write.tmp")
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            logger.info(f"Data directory {data_dir} is writable")
    except Exception as e:
        logger.error(f"Data directory error: {e}")
        # Fallback to current directory if data dir fails
        data_dir = "."
        logger.info(f"Using fallback directory: {data_dir}")
    
    # Use unique database name for tests
    db_name = "notes.db"
    if os.environ.get("TESTING"):
        import uuid
        db_name = f"test_notes_{uuid.uuid4().hex[:8]}.db"
    
    _database_path = os.path.join(data_dir, db_name)
    return _database_path


def reset_database_path():
    """Reset the cached database path (for testing)."""
    global _database_path
    _database_path = None


def get_conn():
    """Get database connection with Row factory for dict-like access."""
    database_path = get_database_path()
    conn = sqlite3.connect(database_path)
    conn.row_factory = sqlite3.Row
    # Enable foreign key constraints
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def init_db():
    """Initialize SQLite database and create tables if they don't exist."""
    database_path = get_database_path()
    logger.info(f"Initializing database at: {database_path}")
    
    conn = get_conn()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Check if user_id column exists in notes table, add if missing
    cursor.execute("PRAGMA table_info(notes)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'user_id' not in columns:
        cursor.execute('ALTER TABLE notes ADD COLUMN user_id INTEGER')
        logger.info("Added user_id column to notes table")
    
    conn.commit()
    conn.close()
    logger.info("Database initialization completed")


def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    """Execute a database query with proper connection handling."""
    conn = get_conn()
    cursor = conn.cursor()
    
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
        else:
            result = cursor.rowcount
        
        conn.commit()
        return result
    finally:
        conn.close()