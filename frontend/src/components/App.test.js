// frontend/src/components/App.test.js
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from './App';

test('renders the RosterPage for the home route', () => {
  render(
    <MemoryRouter initialEntries={['/']}>
      <App />
    </MemoryRouter>
  );
  // We expect the main heading from the RosterPage to be present
  expect(screen.getByRole('heading', { name: /WNBA Player Roster/i })).toBeInTheDocument();
});
