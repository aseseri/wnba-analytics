// frontend/src/components/App.test.js
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from './App';
import { AuthProvider } from '../AuthContext';
import { AppThemeProvider } from '../ThemeContext';

test('renders the RosterPage for the home route', () => {
  render(
    <AppThemeProvider>
      <AuthProvider>
        <MemoryRouter initialEntries={['/']}>
          <App />
        </MemoryRouter>
      </AuthProvider>
    </AppThemeProvider>
  );
  expect(screen.getByRole('heading', { name: /WNBA Player Roster/i })).toBeInTheDocument();
});