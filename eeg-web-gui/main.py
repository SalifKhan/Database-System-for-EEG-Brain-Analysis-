# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/eeg_brain_signal_analysis'
    
    db.init_app(app)
    
    from app.routes import main, subjects, signals, projects
    app.register_blueprint(main.bp)
    app.register_blueprint(subjects.bp)
    app.register_blueprint(signals.bp)
    app.register_blueprint(projects.bp)
    
    with app.app_context():
        db.create_all()
    
    return app

from app import create_app, db

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)