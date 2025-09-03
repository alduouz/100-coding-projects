import logging
import os
from flask import Flask, render_template
from config import config
from .db import init_db


def create_app(config_name=None):
    """Application factory pattern."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Configure logging
    if not app.debug and not app.testing:
        # Production logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(name)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
        app.logger.info('Personal Notes application startup')
    else:
        # Development logging
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
    
    # Initialize database (only in non-testing mode)
    if not app.testing:
        with app.app_context():
            init_db()
    
    # Register blueprints
    from .auth import auth_bp
    from .notes import notes_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}, 200
    
    # Remove the root route since notes.index handles '/'
    
    return app