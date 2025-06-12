// frontend/src/components/RosterPage/RosterPage.js
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom'; // Import Link
import { Box, Button, TextField, Typography, Grid, Card, CardContent, CardActions } from '@mui/material';

function RosterPage() {
  const [players, setPlayers] = useState([]);
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [team, setTeam] = useState('');
  const [editingPlayer, setEditingPlayer] = useState(null);   // State to track which player is being edited


  const fetchPlayers = () => {
    fetch('http://localhost:8000/api/players')
      .then(response => response.json())
      .then(data => {
        setPlayers(data);
      })
      .catch(error => console.error('Error fetching players:', error));
  };
  useEffect(() => { fetchPlayers(); }, []);
  
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
    <Box sx={{ mt: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        {editingPlayer ? 'Edit Player' : 'WNBA Player Roster'}
      </Typography>

      <Box component="form" onSubmit={handleFormSubmit} sx={{ mb: 4, p: 2, border: '1px solid grey', borderRadius: 2 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={4}>
            <TextField fullWidth label="First Name" value={firstName} onChange={e => setFirstName(e.target.value)} required />
          </Grid>
          <Grid item xs={12} sm={4}>
            <TextField fullWidth label="Last Name" value={lastName} onChange={e => setLastName(e.target.value)} required />
          </Grid>
          <Grid item xs={12} sm={4}>
            <TextField fullWidth label="Team" value={team} onChange={e => setTeam(e.target.value)} required />
          </Grid>
          <Grid item xs={12}>
            <Button type="submit" variant="contained">{editingPlayer ? 'Update Player' : 'Add Player'}</Button>
            {editingPlayer && <Button onClick={cancelEdit} sx={{ ml: 1 }}>Cancel</Button>}
          </Grid>
        </Grid>
      </Box>

      <Grid container spacing={3}>
        {players.map(player => (
          <Grid item key={player.id} xs={12} sm={6} md={4}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
              <CardContent>
                <Typography variant="h5" component={Link} to={`/players/${player.id}`} sx={{ textDecoration: 'none', color: 'inherit' }}>
                  {player.first_name} {player.last_name}
                </Typography>
                <Typography color="text.secondary">
                  {player.team}
                </Typography>
              </CardContent>
              <CardActions>
                <Button size="small" onClick={() => handleEditClick(player)}>Edit</Button>
                <Button size="small" color="error" onClick={() => handleDelete(player.id)}>Delete</Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}

export default RosterPage;
