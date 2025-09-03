import sqlite3
import logging
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .db import get_conn


logger = logging.getLogger(__name__)


auth_bp = Blueprint('auth', __name__)


def get_user_by_email(email):
    """Retrieve a user by email. Returns None if not found."""
    conn = get_conn()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    
    conn.close()
    return user


@auth_bp.route('/register', methods=['GET', 'POST'])
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
        
        conn = get_conn()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'INSERT INTO users (email, password_hash) VALUES (?, ?)',
                (email, password_hash)
            )
            conn.commit()
            logger.info(f'New user registered: {email}')
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except sqlite3.IntegrityError:
            flash('Email already registered. Please use a different email or log in.', 'error')
        finally:
            conn.close()
    
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
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
            logger.info(f'User logged in: {email}')
            flash('Login successful! Welcome back.', 'success')
            return redirect(url_for('notes.index'))
        else:
            flash('Invalid email or password. Please try again.', 'error')
    
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    """Handle user logout."""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))