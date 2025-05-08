from app import create_app, db
import pymysql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

def update_db():
    with app.app_context():
        try:
            # Create a connection
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                database='eeg_brain_signal_analysis'
            )
            cursor = conn.cursor()

            # Add researcher_id to users table
            try:
                cursor.execute("""
                    ALTER TABLE users 
                    ADD COLUMN researcher_id INT,
                    ADD CONSTRAINT fk_user_researcher 
                    FOREIGN KEY (researcher_id) 
                    REFERENCES Researcher(researcher_id)
                """)
                print("Added researcher_id to users table")
            except pymysql.err.OperationalError as e:
                if "Duplicate column name" in str(e):
                    print("researcher_id column already exists")
                else:
                    raise e

            # Create admin user if not exists
            cursor.execute("""
                INSERT IGNORE INTO users (username, email, password_hash, is_active)
                VALUES ('admin', 'admin@example.com', 
                       'pbkdf2:sha256:600000$7qyqVa3W$c1590f31f0fa32dd94d487af5980ada9c602d2a980b471889327d59e5b4fec4a',
                       1)
            """)

            # Commit the changes
            conn.commit()
            print("Database schema updated successfully!")

        except Exception as e:
            print(f"Error updating database: {str(e)}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

if __name__ == '__main__':
    update_db() 