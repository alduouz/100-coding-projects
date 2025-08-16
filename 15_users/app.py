import sqlite3
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, abort, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

DATABASE_NAME = 'notes.db'

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
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Email and password are required.')
            return render_template('register.html')
        
        if get_user_by_email(email):
            flash('Email already registered.')
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
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already registered.')
        finally:
            conn.close()
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Email and password are required.')
            return render_template('login.html')
        
        user = get_user_by_email(email)
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Handle user logout."""
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    """Display all notes from database in descending order of date."""
    conn = get_database_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM notes WHERE user_id = ? ORDER BY date DESC', (session['user_id'],))
    notes = cursor.fetchall()
    
    conn.close()
    return render_template('index.html', notes=notes)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_note():
    """Handle note creation - GET shows form, POST inserts to database."""
    if request.method == 'POST':
        note_content = request.form.get('content')
        if note_content and note_content.strip():
            conn = get_database_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                'INSERT INTO notes (content, date, user_id) VALUES (?, ?, ?)',
                (note_content.strip(), datetime.now(), session['user_id'])
            )
            
            conn.commit()
            conn.close()
        
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
        note_content = request.form.get('content')
        if note_content and note_content.strip():
            conn = get_database_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                'UPDATE notes SET content = ?, date = ? WHERE id = ? AND user_id = ?',
                (note_content.strip(), datetime.now(), note_id, session['user_id'])
            )
            
            conn.commit()
            conn.close()
        
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
        
        return redirect(url_for('index'))
    
    return render_template('confirm_delete.html', note=note)

if __name__ == '__main__':
    init_database()
    app.run(debug=True, port=5004)