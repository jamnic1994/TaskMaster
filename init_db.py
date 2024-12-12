from app import db, app

# Ensure the app context is set up before creating the tables
with app.app_context():
    db.create_all()
    print("Database tables created successfully (if they didn't already exist).")