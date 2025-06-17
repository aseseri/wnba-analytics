// frontend/src/components/App.js
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Layout from './Layout';
import RosterPage from './RosterPage/RosterPage';
import PlayerDetailPage from './PlayerDetailPage/PlayerDetailPage';
import LoginPage from './LoginPage/LoginPage';
import './App.css';

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<RosterPage />} />
        <Route path="/players/:playerId" element={<PlayerDetailPage />} />
        <Route path="/login" element={<LoginPage />} />
      </Routes>
    </Layout>
  );
}

export default App;
