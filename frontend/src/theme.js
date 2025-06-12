// frontend/src/theme.js
import { createTheme } from '@mui/material/styles';

export const lightTheme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2', // A nice blue
    },
    background: {
      default: '#f4f6f8', // A very light grey
      paper: '#ffffff',
    },
  },
});

export const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#90caf9', // A lighter blue for dark mode
    },
    background: {
      default: '#121212', // Standard dark theme background
      paper: '#1e1e1e',
    },
  },
});