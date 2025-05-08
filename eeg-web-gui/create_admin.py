from app import create_app, db
from app.models import User

def create_admin_user(username, email, password):
    app = create_app()
    with app.app_context():
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            print(f"User {username} already exists!")
            return
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        
        # Add to database
        db.session.add(user)
        db.session.commit()
        print(f"Admin user {username} created successfully!")

if __name__ == "__main__":
    username = input("Enter admin username: ")
    email = input("Enter admin email: ")
    password = input("Enter admin password: ")
    create_admin_user(username, email, password) 