"""
This file is kept for backwards compatibility.
Use run.py at the project root instead.
"""
from app import app
from models import db

def init_db():
    """Initialize the database with tables and sample data."""
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)