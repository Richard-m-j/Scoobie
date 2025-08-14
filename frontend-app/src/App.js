// src/App.js
import React, { useState, useEffect, useCallback } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [error, setError] = useState('');

  const fetchMessages = useCallback(async () => {
    try {
      const response = await fetch('/api/messages');
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const data = await response.json();
      setMessages(data);
    } catch (err) {
      setError('Failed to fetch messages.');
      console.error(err);
    }
  }, []);

  useEffect(() => {
    fetchMessages();
  }, [fetchMessages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!newMessage.trim()) return;

    try {
      const response = await fetch('/api/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: newMessage }),
      });

      if (!response.ok) {
        throw new Error('Failed to post message.');
      }
      
      setNewMessage(''); // Clear input field
      fetchMessages(); // Refresh the list of messages
    } catch (err) {
      setError('Failed to add message.');
      console.error(err);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>My List</h1>
        <form onSubmit={handleSubmit} className="message-form">
          <input
            type="text"
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            placeholder="What's on your mind?"
          />
          <button type="submit">Add Item</button>
        </form>

        {error && <p className="error">{error}</p>}

        <ul className="message-list">
          {messages.map((msg) => (
            <li key={msg.id}>{msg.text}</li>
          ))}
        </ul>
      </header>
    </div>
  );
}

export default App;