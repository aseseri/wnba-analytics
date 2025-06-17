// frontend/src/components/LoginPage/LoginPage.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../AuthContext';
import { Box, Button, TextField, Typography, Paper } from '@mui/material';

function LoginPage() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const auth = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault();
        setError('');
        try {
            await auth.login(username, password);
            navigate('/'); // Redirect to homepage on successful login
        } catch (err) {
            setError('Invalid username or password.');
        }
    };

    return (
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="70vh">
            <Paper elevation={6} sx={{ padding: 4, width: '100%', maxWidth: 400 }}>
                <Typography variant="h4" component="h1" gutterBottom>Admin Login</Typography>
                <Box component="form" onSubmit={handleSubmit}>
                    <TextField fullWidth margin="normal" label="Username" value={username} onChange={e => setUsername(e.target.value)} required />
                    <TextField fullWidth margin="normal" label="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} required />
                    {error && <Typography color="error">{error}</Typography>}
                    <Button type="submit" fullWidth variant="contained" sx={{ mt: 2 }}>Login</Button>
                </Box>
            </Paper>
        </Box>
    );
}
export default LoginPage;