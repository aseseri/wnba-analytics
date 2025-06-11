// frontend/src/App.js

import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  // State to hold the list of players from the API
  const [players, setPlayers] = useState([]);

  // This function will fetch the players from the backend
  const fetchPlayers = () => {
    fetch('http://localhost:8000/api/players')
      .then(response => response.json())
      .then(data => {
        console.log('Fetched players:', data); // For debugging
        setPlayers(data);
      })
      .catch(error => console.error('Error fetching players:', error));
  };

  // useEffect runs once after the component mounts
  useEffect(() => {
    fetchPlayers();
  }, []); // The empty array ensures this runs only once

  return (
    <div className="App">
      <header className="App-header">
        <h1>WNBA Player Roster</h1>
        <div className="player-list">
          {/* We will map over the players array to display each one */}
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