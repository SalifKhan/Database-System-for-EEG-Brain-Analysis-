import os

# Base directory of the application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Secret key for session management
SECRET_KEY = 'your-secret-key-replace-this-in-production'

# Database configuration
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/eeg_brain_signal_analysis'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True  # Enable SQL query logging

# File upload settings
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER) 