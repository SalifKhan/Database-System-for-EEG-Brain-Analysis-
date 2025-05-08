from app import create_app, db
from app.models import User
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_auth():
    app = create_app()
    with app.app_context():
        try:
            # First, let's check if the users table exists and has any users
            logger.info("Checking existing users...")
            users = User.query.all()
            logger.info(f"Found {len(users)} existing users")
            
            # Create a test user
            test_username = "testuser"
            test_password = "testpass"
            
            # Delete test user if exists
            existing_user = User.query.filter_by(username=test_username).first()
            if existing_user:
                db.session.delete(existing_user)
                db.session.commit()
                logger.info(f"Deleted existing test user: {test_username}")
            
            # Create new test user
            user = User(username=test_username, email="test@example.com")
            user.set_password(test_password)
            db.session.add(user)
            db.session.commit()
            logger.info(f"Created new test user: {test_username}")
            
            # Try to retrieve and authenticate the user
            retrieved_user = User.query.filter_by(username=test_username).first()
            if retrieved_user:
                logger.info("Test user found in database")
                logger.info(f"Stored password hash: {retrieved_user.password_hash}")
                
                # Test password verification
                is_valid = retrieved_user.check_password(test_password)
                logger.info(f"Password verification result: {is_valid}")
                
                if is_valid:
                    logger.info("Password verification successful!")
                else:
                    logger.error("Password verification failed!")
            else:
                logger.error("Could not retrieve test user from database!")
                
        except Exception as e:
            logger.error(f"Error during testing: {str(e)}")
            raise

if __name__ == "__main__":
    test_auth() 