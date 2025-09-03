from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, abort, session, flash
from functools import wraps
from .db import get_conn


notes_bp = Blueprint('notes', __name__)


def login_required(f):
    """Decorator to require login for protected routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def get_note_by_id(note_id):
    """Retrieve a single note by ID. Returns None if not found."""
    try:
        note_id = int(note_id)
    except (ValueError, TypeError):
        return None
    
    conn = get_conn()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM notes WHERE id = ? AND user_id = ?', (note_id, session.get('user_id')))
    note = cursor.fetchone()
    
    conn.close()
    return note


@notes_bp.route('/')
@login_required
def index():
    """Display notes with optional search filtering."""
    search_query = request.args.get('q', '').strip()
    
    conn = get_conn()
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


@notes_bp.route('/add', methods=['GET', 'POST'])
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
        
        conn = get_conn()
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO notes (content, date, user_id) VALUES (?, ?, ?)',
            (note_content, datetime.now(), session['user_id'])
        )
        
        conn.commit()
        conn.close()
        
        flash('Note added successfully!', 'success')
        return redirect(url_for('notes.index'))
    
    return render_template('add.html')


@notes_bp.route('/edit/<int:note_id>', methods=['GET', 'POST'])
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
        
        conn = get_conn()
        cursor = conn.cursor()
        
        cursor.execute(
            'UPDATE notes SET content = ?, date = ? WHERE id = ? AND user_id = ?',
            (note_content, datetime.now(), note_id, session['user_id'])
        )
        
        conn.commit()
        conn.close()
        
        flash('Note updated successfully!', 'success')
        return redirect(url_for('notes.index'))
    
    return render_template('edit.html', note=note)


@notes_bp.route('/delete/<int:note_id>', methods=['GET', 'POST'])
@login_required
def delete_note(note_id):
    """Handle note deletion - GET shows confirmation, POST deletes from database."""
    note = get_note_by_id(note_id)
    if not note:
        abort(404)
    
    if request.method == 'POST':
        conn = get_conn()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM notes WHERE id = ? AND user_id = ?', (note_id, session['user_id']))
        
        conn.commit()
        conn.close()
        
        flash('Note deleted successfully!', 'success')
        return redirect(url_for('notes.index'))
    
    return render_template('confirm_delete.html', note=note)