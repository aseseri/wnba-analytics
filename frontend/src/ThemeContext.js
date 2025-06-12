// frontend/src/ThemeContext.js
import React, { useState, useMemo, createContext } from 'react';
import { ThemeProvider as MuiThemeProvider, CssBaseline } from '@mui/material';
import { lightTheme, darkTheme } from './theme';

export const ThemeContext = createContext({
  toggleTheme: () => {},
});

export const AppThemeProvider = ({ children }) => {
  const [mode, setMode] = useState('dark'); // Default to dark mode

  const theme = useMemo(() => (mode === 'light' ? lightTheme : darkTheme), [mode]);

  const toggleTheme = () => {
    setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'));
  };

  return (
    <ThemeContext.Provider value={{ toggleTheme }}>
      <MuiThemeProvider theme={theme}>
        <CssBaseline /> {/* This resets default browser styles */}
        {children}
      </MuiThemeProvider>
    </ThemeContext.Provider>
  );
};