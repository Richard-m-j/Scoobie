# backend-api-python/test_app.py

import pytest
from app import app, db, Message

# This fixture sets up a temporary, in-memory SQLite database for each test
@pytest.fixture
def client():
    # Configure the app for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Use an in-memory DB
    
    # Create a test client using the Flask application configured for testing
    with app.test_client() as client:
        # Establish an application context
        with app.app_context():
            db.create_all() # Create all database tables
            
            # Add a sample message to the in-memory database
            sample_message = Message("Test Message")
            db.session.add(sample_message)
            db.session.commit()

        yield client # this is where the testing happens

    # Teardown: The in-memory database is automatically destroyed after the test
    
def test_get_messages_endpoint(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/messages' endpoint is requested (GET)
    THEN check that the response is valid and contains the sample message
    """
    response = client.get('/api/messages')
    json_data = response.get_json()

    # Check the response status and content type
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    
    # Check that the response data is a list with one item
    assert isinstance(json_data, list)
    assert len(json_data) == 1
    
    # Check the content of the message
    assert json_data[0]['text'] == "Test Message"