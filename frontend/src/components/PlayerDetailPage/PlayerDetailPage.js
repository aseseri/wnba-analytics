// frontend/src/components/PlayerDetailPage/PlayerDetailPage.js

import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography, Box, Skeleton, Button, Grid, Card, CardContent} from '@mui/material';

function PlayerDetailPage() {
  const [player, setPlayer] = useState(null);
  const [loading, setLoading] = useState(true);
  const [similarPlayers, setSimilarPlayers] = useState([]);
  const [compsLoading, setCompsLoading] = useState(true);

  const { playerId } = useParams();

  useEffect(() => {
    // Reset states when the player ID changes
    setLoading(true);
    setCompsLoading(true);
    setPlayer(null);
    setSimilarPlayers([]);

    // Fetch the main player data
    fetch(`http://localhost:8000/api/players/${playerId}`)
      .then(response => response.json())
      .then(data => {
        setPlayer(data);
        setLoading(false);

        // Logic to fetch similar players ---
        // After we get the player data, find their most recent season
        if (data.stats && data.stats.length > 0) {
          // Sort stats by season descending to get the most recent
          const mostRecentSeason = data.stats.sort((a, b) => b.season.localeCompare(a.season))[0];
          
          // Now, fetch the comps for that specific player and season
          fetch(`http://localhost:8000/api/players/${playerId}/seasons/${mostRecentSeason.season}/similar`)
            .then(compResponse => compResponse.json())
            .then(compData => {
              setSimilarPlayers(compData);
            })
            .catch(error => console.error('Error fetching similar players:', error))
            .finally(() => setCompsLoading(false)); // Stop the comps loading state
        } else {
          // If the player has no stats, we can't get comps
          setCompsLoading(false);
        }
      })
      .catch(error => {
        console.error('Error fetching player details:', error);
        setLoading(false);
        setCompsLoading(false);
      });
  }, [playerId]);

  // Skeleton Loading UI
  if (loading) {
    return (
      <Box sx={{ mt: 2 }}>
        <Typography variant="h3"><Skeleton width="60%" /></Typography>
        <Typography variant="h5" color="text.secondary"><Skeleton width="40%" /></Typography>
        <Skeleton variant="rectangular" sx={{ mt: 4, borderRadius: 1 }} width="100%" height={300} />
      </Box>
    );
  }

  if (!player) { return <Typography>Player not found.</Typography>; }

  return (
    // Use MUI's Box component for layout and spacing
    <Box sx={{ mt: 2 }}>
      <Typography variant="h3" component="h1" gutterBottom> {player.first_name} {player.last_name} </Typography>
      <Typography variant="h5" component="h2" color="text.secondary" gutterBottom> Team: {player.team} </Typography>

      <Typography variant="h4" component="h3" sx={{ mt: 4, mb: 2 }}> Season Statistics </Typography>

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

      <Typography variant="h4" component="h3" sx={{ mt: 4, mb: 2 }}>Statistical Comps</Typography>
      <Box>
        {compsLoading ? (
          // If comps are loading, show a grid of skeletons
          <Grid container spacing={2}>
            {[...Array(5)].map((_, index) => (
              <Grid item xs={12} sm={6} md={2.4} key={index}>
                <Skeleton variant="rectangular" height={100} sx={{ borderRadius: 1 }}/>
              </Grid>
            ))}
          </Grid>
        ) : (
          // Otherwise, show the similar player cards
          <Grid container spacing={2}>
            {similarPlayers.map((comp) => (
              <Grid item xs={12} sm={6} md={2.4} key={comp.player_season_id}>
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="subtitle1">{comp.player_season_id}</Typography>
                    <Typography color="text.secondary">
                      Similarity: { (comp.similarity_score * 100).toFixed(1) }%
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        )}
      </Box>

      <Box sx={{ mt: 4 }}>
          <Button component={Link} to="/" variant="outlined">Back to Roster</Button>
      </Box>
    </Box>
  );
}

export default PlayerDetailPage;