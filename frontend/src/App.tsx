import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import LandingPage from './components/LandingPage';
import GamePage from './components/GamePage';

import './App.css'
import { WebSocketProvider } from './services/WebSocket';
import LoginPage from './components/LoginPage';

import { tryLogin, tryRegister } from "./services/Login";

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage onLogin={tryLogin} />}/>
        <Route path="/" element={<LandingPage />}/>
        <Route path="/g" element={<WebSocketProvider><GamePage /></WebSocketProvider>}/>
      </Routes>
    </BrowserRouter>
  )
};

export default App
