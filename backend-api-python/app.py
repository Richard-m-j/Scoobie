# app.py

import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# --- Database Configuration ---
# Use an environment variable for the database URL, with a fallback for local development.
# This makes it easy to connect to the database in Kubernetes later.
db_url = os.environ.get("DB_URL", "postgresql://user:password@localhost:5432/mydatabase")
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)


# --- Database Model ---
# This class represents the 'messages' table in our database.
class Message(db.Model):
    __tablename__ = 'messages' # Optional: Specify table name
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)

    def __init__(self, text):
        self.text = text


# --- API Endpoint ---
# This defines a GET endpoint at /api/messages.
@app.route('/api/messages')
def get_messages():
    """Returns all messages from the database as JSON."""
    messages = Message.query.all()
    # Convert the list of message objects to a list of dictionaries
    results = [
        {
            "id": msg.id,
            "text": msg.text
        } for msg in messages]
    
    # Return the JSON response
    return jsonify(results)


# --- Main Execution ---
# This block runs only when the script is executed directly (e.g., `python app.py`).
if __name__ == '__main__':
    # Create database tables and add a sample message if it's a fresh database
    with app.app_context():
        db.create_all() # Create tables if they don't exist
        # Check if there are any messages already
        if not Message.query.first():
            # If no messages, add a sample one
            sample_message = Message("Hello from the Python Backend! 👋")
            db.session.add(sample_message)
            db.session.commit()
            print("Database initialized and sample message added.")

    # Run the Flask development server
    app.run(host='0.0.0.0', port=5000)