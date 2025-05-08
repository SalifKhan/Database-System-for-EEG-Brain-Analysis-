from app import create_app, db

app = create_app()

with app.app_context():
    # Get the database engine
    engine = db.engine
    
    # Execute the ALTER TABLE command
    with engine.connect() as connection:
        connection.execute("ALTER TABLE Subject AUTO_INCREMENT = 6")
        connection.commit()
    
    print("Auto-increment sequence has been reset successfully!") 