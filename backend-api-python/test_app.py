# backend-api-python/test_app.py

import pytest
import json
from unittest.mock import patch, MagicMock
from app import app, db

@pytest.fixture
def client():
    """Configures the app for testing and provides a test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('app.Message.query')
def test_get_messages_with_mock_db(mock_query, client):
    """Tests the GET /api/messages endpoint."""
    mock_message = MagicMock()
    mock_message.to_dict.return_value = {"id": 99, "text": "This is a mocked message."}
    mock_query.all.return_value = [mock_message]

    response = client.get('/api/messages')
    json_data = response.get_json()

    assert response.status_code == 200
    assert len(json_data) == 1
    assert json_data[0]['text'] == "This is a mocked message."
    mock_query.all.assert_called_once()

@patch('app.db.session')
def test_add_message_with_mock_db(mock_session, client):
    """Tests the POST /api/messages endpoint."""
    # The data we'll send in our POST request
    new_message_data = {"text": "A new test message"}

    # Call the endpoint
    response = client.post(
        '/api/messages',
        data=json.dumps(new_message_data),
        content_type='application/json'
    )

    # Assertions
    assert response.status_code == 201
    assert 'text' in response.get_json()
    assert response.get_json()['text'] == "A new test message"
    
    # Check that our mock database session was used
    assert mock_session.add.call_count == 1
    assert mock_session.commit.call_count == 1

def test_add_message_empty_text(client):
    """Tests that an empty message cannot be added."""
    response = client.post(
        '/api/messages',
        data=json.dumps({"text": "  "}), # Empty string
        content_type='application/json'
    )
    assert response.status_code == 400
    assert "error" in response.get_json()