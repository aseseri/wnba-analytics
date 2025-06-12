// frontend/src/components/App.js
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Layout from './Layout';
import RosterPage from './RosterPage/RosterPage';
import PlayerDetailPage from './PlayerDetailPage/PlayerDetailPage';
import './App.css';

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<RosterPage />} />
        <Route path="/players/:playerId" element={<PlayerDetailPage />} />
      </Routes>
    </Layout>
  );
}

export default App;
