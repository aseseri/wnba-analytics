// frontend/src/components/PlayerDetailPage/PlayerDetailPage.js
import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import '../App.css';

function PlayerDetailPage() {
  const [player, setPlayer] = useState(null);
  const { playerId } = useParams(); // Gets the 'playerId' from the URL

  useEffect(() => {
    // Fetch data for this specific player
    fetch(`http://localhost:8000/api/players/${playerId}`)
      .then(response => response.json())
      .then(data => setPlayer(data))
      .catch(error => console.error('Error fetching player details:', error));
  }, [playerId]); // Re-run if the playerId changes

  // Show a loading message while data is being fetched
  if (!player) {
    return <div>Loading player details...</div>;
  }

  return (
    <div>
      <h1>{player.first_name} {player.last_name}</h1>
      <p><strong>Team:</strong> {player.team}</p>

      <h3>Season Statistics</h3>
      <table className="stats-table">
        <thead>
          <tr>
            <th>Season</th>
            <th>Team</th>
            <th>G</th>
            <th>GS</th>
            <th>PTS</th>
            <th>REB</th>
            <th>AST</th>
            <th>STL</th>
            <th>BLK</th>
            <th>FG%</th>
            <th>3P%</th>
            <th>PER</th>
          </tr>
        </thead>
        <tbody>
          {player.stats.map(stat => (
            <tr key={stat.id}>
              <td>{stat.season}</td>
              <td>{player.team}</td>
              <td>{stat.games_played}</td>
              <td>{stat.games_started}</td>
              <td>{stat.points_per_game}</td>
              <td>{stat.rebounds_per_game}</td>
              <td>{stat.assists_per_game}</td>
              <td>{stat.steals_per_game}</td>
              <td>{stat.blocks_per_game}</td>
              <td>{stat.field_goal_percentage}</td>
              <td>{stat.three_point_percentage}</td>
              <td>{stat.player_efficiency_rating}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <br />
      <Link to="/">Back to Roster</Link>
    </div>
  );
}

export default PlayerDetailPage;