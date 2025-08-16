import sqlite3
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)

DATABASE_NAME = 'notes.db'

def init_database():
    """Initialize SQLite database and create notes table if it doesn't exist."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def get_database_connection():
    """Get database connection with Row factory for dict-like access."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def get_note_by_id(note_id):
    """Retrieve a single note by ID. Returns None if not found."""
    try:
        note_id = int(note_id)
    except (ValueError, TypeError):
        return None
    
    conn = get_database_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM notes WHERE id = ?', (note_id,))
    note = cursor.fetchone()
    
    conn.close()
    return note

@app.route('/')
def index():
    """Display all notes from database in descending order of date."""
    conn = get_database_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM notes ORDER BY date DESC')
    notes = cursor.fetchall()
    
    conn.close()
    return render_template('index.html', notes=notes)

@app.route('/add', methods=['GET', 'POST'])
def add_note():
    """Handle note creation - GET shows form, POST inserts to database."""
    if request.method == 'POST':
        note_content = request.form.get('content')
        if note_content and note_content.strip():
            conn = get_database_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                'INSERT INTO notes (content, date) VALUES (?, ?)',
                (note_content.strip(), datetime.now())
            )
            
            conn.commit()
            conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
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
                'UPDATE notes SET content = ?, date = ? WHERE id = ?',
                (note_content.strip(), datetime.now(), note_id)
            )
            
            conn.commit()
            conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('edit.html', note=note)

@app.route('/delete/<int:note_id>', methods=['GET', 'POST'])
def delete_note(note_id):
    """Handle note deletion - GET shows confirmation, POST deletes from database."""
    note = get_note_by_id(note_id)
    if not note:
        abort(404)
    
    if request.method == 'POST':
        conn = get_database_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
        
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('confirm_delete.html', note=note)

if __name__ == '__main__':
    init_database()
    app.run(debug=True, port=5003)