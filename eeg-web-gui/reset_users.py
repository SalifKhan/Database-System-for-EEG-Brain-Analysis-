from app import create_app, db
from app.models import User

def reset_users_table():
    app = create_app()
    with app.app_context():
        # Drop and recreate the users table
        User.__table__.drop(db.engine, checkfirst=True)
        User.__table__.create(db.engine)
        
        # Create a test user
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpass')
        db.session.add(user)
        db.session.commit()
        print("Users table reset and test user created successfully!")

if __name__ == "__main__":
    reset_users_table() 