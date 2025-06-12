// frontend/src/components/PlayerDetailPage/PlayerDetailPage.js

import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography, Box, Skeleton, Button } from '@mui/material';

function PlayerDetailPage() {
  const [player, setPlayer] = useState(null);
  const [loading, setLoading] = useState(true);
  const { playerId } = useParams();

  useEffect(() => {
    setLoading(true); // Start loading
    fetch(`http://localhost:8000/api/players/${playerId}`)
      .then(response => response.json())
      .then(data => {
        setPlayer(data);
        setLoading(false); // Finish loading
      })
      .catch(error => {
        console.error('Error fetching player details:', error);
        setLoading(false); // Finish loading even if there's an error
      });
  }, [playerId]);

  // Skeleton Loading UI
  if (loading) {
    return (
      <Box sx={{ padding: 3, maxWidth: 900, margin: 'auto' }}>
        <Typography variant="h3"><Skeleton width="60%" /></Typography>
        <Typography variant="h5"><Skeleton width="40%" /></Typography>
        <Skeleton variant="rectangular" width="100%" height={300} sx={{ mt: 4 }} />
      </Box>
    );
  }

  if (!player) {
    return <Typography>Player not found.</Typography>;
  }

  return (
    // Use MUI's Box component for layout and spacing
    <Box sx={{ padding: 3, maxWidth: 900, margin: 'auto' }}>
      <Typography variant="h3" component="h1" gutterBottom>
        {player.first_name} {player.last_name}
      </Typography>
      <Typography variant="h5" component="h2" color="text.secondary" gutterBottom>
        Team: {player.team}
      </Typography>

      <Typography variant="h4" component="h3" sx={{ mt: 4, mb: 2 }}>
        Season Statistics
      </Typography>

      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label="simple table">
          <TableHead>
            <TableRow sx={{ '& th': { fontWeight: 'bold' } }}>
              <TableCell>Season</TableCell>
              <TableCell align="right">G</TableCell>
              <TableCell align="right">GS</TableCell>
              <TableCell align="right">PTS</TableCell>
              <TableCell align="right">REB</TableCell>
              <TableCell align="right">AST</TableCell>
              <TableCell align="right">STL</TableCell>
              <TableCell align="right">BLK</TableCell>
              <TableCell align="right">FG%</TableCell>
              <TableCell align="right">3P%</TableCell>
              <TableCell align="right">PER</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {player.stats.map((stat) => (
              <TableRow key={stat.id} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                <TableCell component="th" scope="row">{stat.season}</TableCell>
                <TableCell align="right">{stat.games_played}</TableCell>
                <TableCell align="right">{stat.games_started}</TableCell>
                <TableCell align="right">{stat.points_per_game}</TableCell>
                <TableCell align="right">{stat.rebounds_per_game}</TableCell>
                <TableCell align="right">{stat.assists_per_game}</TableCell>
                <TableCell align="right">{stat.steals_per_game}</TableCell>
                <TableCell align="right">{stat.blocks_per_game}</TableCell>
                <TableCell align="right">{stat.field_goal_percentage}</TableCell>
                <TableCell align="right">{stat.three_point_percentage}</TableCell>
                <TableCell align="right">{stat.player_efficiency_rating}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Box sx={{ mt: 4 }}>
          <Button component={Link} to="/" variant="outlined">Back to Roster</Button>
      </Box>
    </Box>
  );
}

export default PlayerDetailPage;