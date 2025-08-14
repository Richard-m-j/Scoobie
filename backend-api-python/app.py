# app.py

import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# --- Database Configuration ---
db_user = os.environ.get('POSTGRES_USER')
db_pass = os.environ.get('POSTGRES_PASSWORD')
db_name = os.environ.get('POSTGRES_DB')
db_host = os.environ.get('POSTGRES_HOST')

db_url = f"postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}"

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Database Model ---
class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        """Converts the message object to a dictionary."""
        return {"id": self.id, "text": self.text}

# --- API Endpoints ---
@app.route('/api/messages', methods=['GET'])
def get_messages():
    """Handles GET requests to fetch all messages."""
    messages = Message.query.all()
    return jsonify([msg.to_dict() for msg in messages])

@app.route('/api/messages', methods=['POST'])
def add_message():
    """Handles POST requests to add a new message."""
    if not request.json or not 'text' in request.json or not request.json['text'].strip():
        return jsonify({"error": "Message text cannot be empty"}), 400

    text = request.json['text']
    new_message = Message(text=text)
    db.session.add(new_message)
    db.session.commit()

    return jsonify(new_message.to_dict()), 201

# --- Main Execution (for local development) ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not Message.query.first():
            sample_message = Message(text="Welcome to your list!")
            db.session.add(sample_message)
            db.session.commit()
    app.run(host='0.0.0.0', port=5000)