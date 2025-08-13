# app.py

import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# --- Database Configuration ---
# Read individual components from environment variables
db_user = os.environ.get('POSTGRES_USER')
db_pass = os.environ.get('POSTGRES_PASSWORD')
db_name = os.environ.get('POSTGRES_DB')
db_host = os.environ.get('POSTGRES_HOST', 'postgres-service') # Default to the service name

# Construct the database URL from the parts
db_url = f"postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}"

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)


# --- Database Model ---
class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)

    def __init__(self, text):
        self.text = text


# --- API Endpoint ---
@app.route('/api/messages')
def get_messages():
    messages = Message.query.all()
    results = [
        {"id": msg.id, "text": msg.text} for msg in messages
    ]
    return jsonify(results)


# --- Main Execution ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not Message.query.first():
            sample_message = Message("Hello from the Python Backend! 👋")
            db.session.add(sample_message)
            db.session.commit()
            print("Database initialized and sample message added.")

    app.run(host='0.0.0.0', port=5000)