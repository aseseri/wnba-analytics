// frontend/src/components/App.js
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import RosterPage from './RosterPage/RosterPage';
import PlayerDetailPage from './PlayerDetailPage/PlayerDetailPage';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <Routes>
          <Route path="/" element={<RosterPage />} />
          <Route path="/players/:playerId" element={<PlayerDetailPage />} />
        </Routes>
      </header>
    </div>
  );
}

export default App;
