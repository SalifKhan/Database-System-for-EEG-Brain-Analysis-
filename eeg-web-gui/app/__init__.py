from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import pymysql
from datetime import datetime

pymysql.install_as_MySQLdb()

# Initialize extensions
db = SQLAlchemy()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    
    # Initialize Flask extensions
    db.init_app(app)
    csrf.init_app(app)
    
    # Register datetime filter
    @app.template_filter('datetime')
    def format_datetime(value):
        if value is None:
            return ""
        return value.strftime('%Y-%m-%d %H:%M:%S')
    
    # Register date filter
    @app.template_filter('date')
    def format_date(value):
        if value is None:
            return ""
        return value.strftime('%Y-%m-%d')
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from app.routes import main, signals, subjects, projects, researchers
    app.register_blueprint(main.bp)
    app.register_blueprint(signals.bp)
    app.register_blueprint(subjects.bp)
    app.register_blueprint(projects.bp)
    app.register_blueprint(researchers.bp)
    
    return app 