# backend-api-python/test_app.py

import pytest
from unittest.mock import patch, MagicMock
from app import app

@pytest.fixture
def client():
    """Configures the app for testing and provides a test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        # The test client pushes an application context
        yield client

def test_get_messages_with_mock_db(client):
    """
    GIVEN a Flask application
    WHEN the '/api/messages' endpoint is called within a mocked DB context
    THEN check that the response is valid and contains the mocked data
    """
    # Use patch as a context manager INSIDE the test function.
    # This runs after the client fixture has activated the app context.
    with patch('app.Message.query') as mock_query:
        # 1. Create a fake "Message" object
        mock_message = MagicMock()
        mock_message.id = 99
        mock_message.text = "This is a mocked message."

        # 2. Configure the mock to return our fake message
        mock_query.all.return_value = [mock_message]

        # 3. Call the API endpoint. The patch is active here.
        response = client.get('/api/messages')
        json_data = response.get_json()

        # 4. Assert the response is correct
        assert response.status_code == 200
        assert len(json_data) == 1
        assert json_data[0]['text'] == "This is a mocked message."

        # Verify that the mocked method was called
        mock_query.all.assert_called_once()