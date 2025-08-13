// src/App.js
import React, { useState } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const fetchMessage = async () => {
    try {
      // This fetch call will be proxied to our backend.
      const response = await fetch('/api/messages');
      
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      // Our backend returns a list, so we'll take the text from the first item.
      setMessage(data[0].text); 
      setError(''); // Clear any previous errors
    } catch (err) {
      setMessage('');
      setError('Failed to fetch messages. Is the backend running?');
      console.error(err);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>React Frontend</h1>
        <button onClick={fetchMessage}>Get Message from Backend</button>
        {message && <p className="message">{message}</p>}
        {error && <p className="error">{error}</p>}
      </header>
    </div>
  );
}

export default App;