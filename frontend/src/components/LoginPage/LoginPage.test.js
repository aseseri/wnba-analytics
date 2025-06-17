// frontend/src/components/LoginPage/LoginPage.test.js
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { AuthContext } from '../../AuthContext';
import LoginPage from './LoginPage';

// We create a mock login function using Jest's built-in mocking
const mockLogin = jest.fn();
const mockNavigate = jest.fn();

// Mock the useNavigate hook from react-router-dom
jest.mock('react-router-dom', () => ({
    ...jest.requireActual('react-router-dom'),
    useNavigate: () => mockNavigate,
}));

const renderWithAuthProvider = (component) => {
  return render(
    <AuthContext.Provider value={{ login: mockLogin, token: null }}>
      <MemoryRouter>
        {component}
      </MemoryRouter>
    </AuthContext.Provider>
  );
};

test('calls login function and navigates on successful submission', async () => {
  // Configure our mock login function to simulate a successful login
  mockLogin.mockResolvedValue(true);

  renderWithAuthProvider(<LoginPage />);

  fireEvent.change(screen.getByLabelText(/Username/i), { target: { value: 'admin' } });
  fireEvent.change(screen.getByLabelText(/Password/i), { target: { value: 'password123' } });
  fireEvent.click(screen.getByRole('button', { name: /Login/i }));

  // Wait for the login function to be called and check arguments
  await waitFor(() => {
    expect(mockLogin).toHaveBeenCalledWith('admin', 'password123');
  });

  // Check that it redirected to the homepage
  expect(mockNavigate).toHaveBeenCalledWith('/');
});