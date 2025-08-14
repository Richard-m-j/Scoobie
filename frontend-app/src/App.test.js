// src/App.test.js
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from './App';

// We mock the global fetch function to control API responses in our tests
beforeEach(() => {
  global.fetch = jest.fn();
});

afterEach(() => {
  jest.resetAllMocks();
});

test('renders and displays initial messages', async () => {
  // Mock a successful fetch call for the initial load
  fetch.mockResolvedValueOnce({
    ok: true,
    json: async () => [{ id: 1, text: 'First item from API' }],
  });

  render(<App />);

  // Check if the main heading is present
  expect(screen.getByText('My List')).toBeInTheDocument();

  // Wait for the message to appear after the async fetch call and assert it's there
  const firstItem = await screen.findByText('First item from API');
  expect(firstItem).toBeInTheDocument();
  
  // Ensure fetch was called once on initial load
  expect(fetch).toHaveBeenCalledTimes(1);
  expect(fetch).toHaveBeenCalledWith('/api/messages');
});

test('allows a user to add a new item to the list', async () => {
  // Mock the initial fetch to return an empty list
  fetch.mockResolvedValueOnce({
    ok: true,
    json: async () => [],
  });

  render(<App />);
  
  // Mock the successful POST request when the form is submitted
  fetch.mockResolvedValueOnce({
    ok: true,
    json: async () => ({ id: 2, text: 'My new shiny item' }),
  });
  
  // Mock the fetch call that refreshes the list *after* submission
  fetch.mockResolvedValueOnce({
    ok: true,
    json: async () => [{ id: 2, text: 'My new shiny item' }],
  });

  // Find the input field and the submit button
  const inputField = screen.getByPlaceholderText("What's on your mind?");
  const addButton = screen.getByRole('button', { name: /Add Item/i });

  // Simulate user typing into the input field
  fireEvent.change(inputField, { target: { value: 'My new shiny item' } });
  expect(inputField.value).toBe('My new shiny item');

  // Simulate user clicking the add button
  fireEvent.click(addButton);

  // Wait for the new item to appear in the document
  const newItem = await screen.findByText('My new shiny item');
  expect(newItem).toBeInTheDocument();
  
  // Verify the input field was cleared after submission
  expect(inputField.value).toBe('');
  
  // Check that fetch was called 3 times: initial load, POST, and refresh
  expect(fetch).toHaveBeenCalledTimes(3);
});

test('shows an error message when fetching messages fails', async () => {
  // Mock a failed fetch call
  fetch.mockRejectedValueOnce(new Error('API is down'));

  render(<App />);

  // Wait for the error message to be displayed and assert it exists
  const errorMessage = await screen.findByText('Failed to fetch messages.');
  expect(errorMessage).toBeInTheDocument();
});