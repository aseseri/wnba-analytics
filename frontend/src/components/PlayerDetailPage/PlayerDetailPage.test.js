// frontend/src/components/PlayerDetailPage/PlayerDetailPage.test.js
import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import PlayerDetailPage from './PlayerDetailPage';

// We mock the global fetch function before all tests
beforeAll(() => {
  global.fetch = jest.fn();
});

test('fetches player data and displays it correctly', async () => {
  // 1. Define the fake player data that our mock fetch will return
  const mockPlayer = {
    id: 1,
    first_name: 'Arike',
    last_name: 'Ogunbowale',
    team: 'Dallas Wings',
    stats: [
      { id: 101, season: '2024', points_per_game: 25, /* ...other stats */ }
    ]
  };

  // 2. Configure the mock fetch to return our fake data as a JSON response
  fetch.mockResolvedValueOnce({
    ok: true,
    json: async () => mockPlayer,
  });
  // Also mock the similarity call, returning an empty array for simplicity
  fetch.mockResolvedValueOnce({
    ok: true,
    json: async () => [],
  });

  // 3. Render the component. We must wrap it in MemoryRouter to handle routing hooks.
  // We set the initial URL to '/players/1' to match the mock data's ID.
  render(
    <MemoryRouter initialEntries={['/players/1']}>
      <Routes>
        <Route path="/players/:playerId" element={<PlayerDetailPage />} />
      </Routes>
    </MemoryRouter>
  );

  // 4. Assert that the data is displayed.
  // We use `findByText` because the data fetching is asynchronous.
  // `findByText` will wait for the element to appear.
  expect(await screen.findByText(/Arike Ogunbowale/i)).toBeInTheDocument();
  expect(screen.getByText(/Dallas Wings/i)).toBeInTheDocument();
  expect(screen.getByText('2024')).toBeInTheDocument(); // Check for the season in the table
  expect(screen.getByText('25')).toBeInTheDocument();
});