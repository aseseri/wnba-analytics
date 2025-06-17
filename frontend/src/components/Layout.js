// frontend/src/components/Layout.js
import React, { useContext } from 'react';
import { Box, AppBar, Toolbar, Typography, IconButton, Container, Button } from '@mui/material';
import { Brightness4, Brightness7 } from '@mui/icons-material';
import { useTheme } from '@mui/material/styles';
import { ThemeContext } from '../ThemeContext';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';

const Layout = ({ children }) => {
  const theme = useTheme();
  const colorMode = useContext(ThemeContext);
  const auth = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    auth.logout();
    navigate('/');
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar position="fixed">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
              WNBA Analytics
            </Link>
          </Typography>
          <IconButton sx={{ ml: 1 }} onClick={colorMode.toggleTheme} color="inherit">
            {theme.palette.mode === 'dark' ? <Brightness7 /> : <Brightness4 />}
          </IconButton>
          {auth.token ? (
            <Button color="inherit" onClick={handleLogout}>Logout</Button>
          ) : (
            <Button color="inherit" component={Link} to="/login">Login</Button>
          )}
        </Toolbar>
      </AppBar>
      <Box component="main" sx={{ flexGrow: 1, p: 3, width: '100%' }}>
        <Toolbar /> {/* This is a spacer to push content below the AppBar */}
        <Container maxWidth="lg">
          {children}
        </Container>
      </Box>
    </Box>
  );
};

export default Layout;