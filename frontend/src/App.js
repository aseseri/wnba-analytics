// frontend/src/App.js

import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [players, setPlayers] = useState([]);

  // State for the form inputs
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [team, setTeam] = useState('');

  const fetchPlayers = () => {
    fetch('http://localhost:8000/api/players')
      .then(response => response.json())
      .then(data => {
        console.log('Fetched players:', data);
        setPlayers(data);
      })
      .catch(error => console.error('Error fetching players:', error));
  };

  useEffect(() => {
    fetchPlayers();
  }, []);

  // Function to handle form submission
  const handleSubmit = (event) => {
    event.preventDefault(); // Prevents the default browser form submission

    const newPlayer = {
      first_name: firstName,
      last_name: lastName,
      team: team,
    };

    // Send the POST request to the backend
    fetch('http://localhost:8000/api/players', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newPlayer),
    })
      .then(response => response.json())
      .then(data => {
        console.log('Successfully created player:', data);
        // After successfully creating a player, fetch the updated list
        fetchPlayers();
        // Clear the form fields
        setFirstName('');
        setLastName('');
        setTeam('');
      })
      .catch(error => console.error('Error creating player:', error));
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>WNBA Player Roster</h1>

        {/* The form for adding a player */}
        <form onSubmit={handleSubmit} className="player-form">
          <input
            type="text"
            placeholder="First Name"
            value={firstName}
            onChange={e => setFirstName(e.target.value)}
            required
          />
          <input
            type="text"
            placeholder="Last Name"
            value={lastName}
            onChange={e => setLastName(e.target.value)}
            required
          />
          <input
            type="text"
            placeholder="Team"
            value={team}
            onChange={e => setTeam(e.target.value)}
            required
          />
          <button type="submit">Add Player</button>
        </form>

        <div className="player-list">
          {players.map(player => (
            <div key={player.id} className="player-card">
              <h2>{player.first_name} {player.last_name}</h2>
              <p>Team: {player.team}</p>
            </div>
          ))}
        </div>
      </header>
    </div>
  );
}

export default App;