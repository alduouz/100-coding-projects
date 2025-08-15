import sqlite3
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

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

if __name__ == '__main__':
    init_database()
    app.run(debug=True, port=5003)