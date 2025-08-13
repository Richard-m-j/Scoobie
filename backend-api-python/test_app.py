# backend-api-python/test_app.py

import pytest
from unittest.mock import patch, MagicMock
from app import app

# This fixture configures the Flask app for testing without a database
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# The @patch decorator intercepts the database call
@patch('app.Message.query')
def test_get_messages_with_mock_db(mock_query, client):
    """
    GIVEN a Flask application and a mocked database
    WHEN the '/api/messages' endpoint is requested (GET)
    THEN check that the response is valid and contains the mocked data
    """
    # 1. Create a fake "Message" object to be returned by the mock
    mock_message = MagicMock()
    mock_message.id = 99
    mock_message.text = "This is a mocked message."

    # 2. Configure the mock to return a list containing our fake message
    #    when the .all() method is called.
    mock_query.all.return_value = [mock_message]

    # 3. Call the API endpoint. The app code will run, but the call to
    #    "Message.query.all()" will be intercepted and return our fake data.
    response = client.get('/api/messages')
    json_data = response.get_json()

    # 4. Assert that the response is correct based on the mocked data
    assert response.status_code == 200
    assert isinstance(json_data, list)
    assert len(json_data) == 1
    assert json_data[0]['id'] == 99
    assert json_data[0]['text'] == "This is a mocked message."

    # Verify that the mocked database method was actually called
    mock_query.all.assert_called_once()