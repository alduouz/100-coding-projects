import sqlite3
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, abort, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

DATA_DIR = os.environ.get("DATA_DIR", ".")
os.makedirs(DATA_DIR, exist_ok=True)
DATABASE_NAME = os.path.join(DATA_DIR, "notes.db")

def init_database():
    """Initialize SQLite database and create tables if they don't exist."""
    conn = sqlite3.connect(DATABASE_NAME)
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
    
    conn.commit()
    conn.close()

def get_database_connection():
    """Get database connection with Row factory for dict-like access."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    """Decorator to require login for protected routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_user_by_email(email):
    """Retrieve a user by email. Returns None if not found."""
    conn = get_database_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    
    conn.close()
    return user

def get_note_by_id(note_id):
    """Retrieve a single note by ID. Returns None if not found."""
    try:
        note_id = int(note_id)
    except (ValueError, TypeError):
        return None
    
    conn = get_database_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM notes WHERE id = ? AND user_id = ?', (note_id, session.get('user_id')))
    note = cursor.fetchone()
    
    conn.close()
    return note

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Email and password are required.', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('register.html')
        
        if get_user_by_email(email):
            flash('Email already registered. Please use a different email or log in.', 'error')
            return render_template('register.html')
        
        password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        
        conn = get_database_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'INSERT INTO users (email, password_hash) VALUES (?, ?)',
                (email, password_hash)
            )
            conn.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already registered. Please use a different email or log in.', 'error')
        finally:
            conn.close()
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Email and password are required.', 'error')
            return render_template('login.html')
        
        user = get_user_by_email(email)
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            flash('Login successful! Welcome back.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password. Please try again.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Handle user logout."""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    """Display notes with optional search filtering."""
    search_query = request.args.get('q', '').strip()
    
    conn = get_database_connection()
    cursor = conn.cursor()
    
    if search_query:
        search_pattern = f'%{search_query.lower()}%'
        cursor.execute(
            'SELECT * FROM notes WHERE user_id = ? AND LOWER(content) LIKE ? ORDER BY date DESC',
            (session['user_id'], search_pattern)
        )
    else:
        cursor.execute('SELECT * FROM notes WHERE user_id = ? ORDER BY date DESC', (session['user_id'],))
    
    notes = cursor.fetchall()
    conn.close()
    
    return render_template('index.html', notes=notes, search_query=search_query)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_note():
    """Handle note creation - GET shows form, POST inserts to database."""
    if request.method == 'POST':
        note_content = request.form.get('content', '').strip()
        
        if not note_content:
            flash('Note content cannot be empty.', 'error')
            return render_template('add.html')
        
        if len(note_content) > 2000:
            flash('Note content cannot exceed 2000 characters.', 'error')
            return render_template('add.html')
        
        conn = get_database_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO notes (content, date, user_id) VALUES (?, ?, ?)',
            (note_content, datetime.now(), session['user_id'])
        )
        
        conn.commit()
        conn.close()
        
        flash('Note added successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    """Handle note editing - GET shows form with current content, POST updates database."""
    note = get_note_by_id(note_id)
    if not note:
        abort(404)
    
    if request.method == 'POST':
        note_content = request.form.get('content', '').strip()
        
        if not note_content:
            flash('Note content cannot be empty.', 'error')
            return render_template('edit.html', note=note)
        
        if len(note_content) > 2000:
            flash('Note content cannot exceed 2000 characters.', 'error')
            return render_template('edit.html', note=note)
        
        conn = get_database_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            'UPDATE notes SET content = ?, date = ? WHERE id = ? AND user_id = ?',
            (note_content, datetime.now(), note_id, session['user_id'])
        )
        
        conn.commit()
        conn.close()
        
        flash('Note updated successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('edit.html', note=note)

@app.route('/delete/<int:note_id>', methods=['GET', 'POST'])
@login_required
def delete_note(note_id):
    """Handle note deletion - GET shows confirmation, POST deletes from database."""
    note = get_note_by_id(note_id)
    if not note:
        abort(404)
    
    if request.method == 'POST':
        conn = get_database_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM notes WHERE id = ? AND user_id = ?', (note_id, session['user_id']))
        
        conn.commit()
        conn.close()
        
        flash('Note deleted successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('confirm_delete.html', note=note)

if __name__ == '__main__':
    init_database()
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, port=int(os.environ.get('PORT', 5004)))