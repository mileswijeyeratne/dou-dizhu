import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import LandingPage from './components/LandingPage';
import GamePage from './components/GamePage';

import './App.css'
import { WebSocketProvider } from './services/WebSocket';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />}/>
        <Route path="/g" element={<WebSocketProvider><GamePage /></WebSocketProvider>}/>
      </Routes>
    </BrowserRouter>
  )
};

export default App
