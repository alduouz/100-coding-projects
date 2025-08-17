# Flask App Deployment Template

import os
from flask import Flask

app = Flask(__name__)

# Production-ready configuration
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# Database configuration with error handling
DATA_DIR = os.environ.get("DATA_DIR", ".")
try:
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"✅ Data directory {DATA_DIR} ready")
except Exception as e:
    print(f"❌ Data directory error: {e}")
    DATA_DIR = "."  # Fallback

DATABASE_PATH = os.path.join(DATA_DIR, "app.db")

def init_database():
    """Initialize database - MUST be called at module level for production."""
    # Your database setup code here
    print(f"Database initialized at: {DATABASE_PATH}")

# CRITICAL: Initialize database when module is imported (for gunicorn)
init_database()

@app.route('/')
def home():
    return "App is running!"

if __name__ == '__main__':
    # Development server
    debug_mode = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(
        debug=debug_mode, 
        host='0.0.0.0', 
        port=int(os.environ.get('PORT', 8000))
    )