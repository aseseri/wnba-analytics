// frontend/src/App.js

import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [players, setPlayers] = useState([]);
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [team, setTeam] = useState('');

  // State to track which player is being edited
  const [editingPlayer, setEditingPlayer] = useState(null);

  const fetchPlayers = () => {
    fetch('http://localhost:8000/api/players')
      .then(response => response.json())
      .then(data => {
        setPlayers(data);
      })
      .catch(error => console.error('Error fetching players:', error));
  };

  useEffect(() => {
    fetchPlayers();
  }, []);

  // This function handles both creating AND updating
  const handleFormSubmit = (event) => {
    event.preventDefault();

    // If we are editing, call the update logic
    if (editingPlayer) {
      const updatedPlayer = {
        first_name: firstName,
        last_name: lastName,
        team: team,
      };

      fetch(`http://localhost:8000/api/players/${editingPlayer.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updatedPlayer),
      })
        .then(response => response.json())
        .then(() => {
          fetchPlayers(); // Refresh the list
          cancelEdit();   // Reset the form
        })
        .catch(error => console.error('Error updating player:', error));

    } else { // Otherwise, call the create logic
      const newPlayer = {
        first_name: firstName,
        last_name: lastName,
        team: team,
      };

      fetch('http://localhost:8000/api/players', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newPlayer),
      })
        .then(response => response.json())
        .then(() => {
          fetchPlayers();
          cancelEdit(); // Use cancelEdit to clear the form
        })
        .catch(error => console.error('Error creating player:', error));
    }
  };

  // This function pre-fills the form for editing
  const handleEditClick = (player) => {
    setEditingPlayer(player);
    setFirstName(player.first_name);
    setLastName(player.last_name);
    setTeam(player.team);
  };

  // A function to reset the form state
  const cancelEdit = () => {
    setEditingPlayer(null);
    setFirstName('');
    setLastName('');
    setTeam('');
  };

  const handleDelete = (playerId) => {
    fetch(`http://localhost:8000/api/players/${playerId}`, { method: 'DELETE' })
      .then(response => { if (response.ok) fetchPlayers(); })
      .catch(error => console.error('Error deleting player:', error));
  };

  return (
    <div className="App">
      <header className="App-header">
        {/* Dynamic form title */}
        <h1>{editingPlayer ? 'Edit Player' : 'Add a Player'}</h1>

        {/* The onSubmit now calls our new handler */}
        <form onSubmit={handleFormSubmit} className="player-form">
          <input type="text" placeholder="First Name" value={firstName} onChange={e => setFirstName(e.target.value)} required />
          <input type="text" placeholder="Last Name" value={lastName} onChange={e => setLastName(e.target.value)} required />
          <input type="text" placeholder="Team" value={team} onChange={e => setTeam(e.target.value)} required />

          {/* Dynamic button text and a "Cancel" button */}
          <div className="form-buttons">
            <button type="submit">{editingPlayer ? 'Update Player' : 'Add Player'}</button>
            {editingPlayer && <button type="button" onClick={cancelEdit}>Cancel</button>}
          </div>
        </form>

        <div className="player-list">
          {players.map(player => (
            <div key={player.id} className="player-card">
              <h2>{player.first_name} {player.last_name}</h2>
              <p>Team: {player.team}</p>
              {/* Edit button */}
              <div className="card-buttons">
                <button onClick={() => handleEditClick(player)} className="edit-btn">Edit</button>
                <button onClick={() => handleDelete(player.id)} className="delete-btn">Delete</button>
              </div>
            </div>
          ))}
        </div>
      </header>
    </div>
  );
}

export default App;