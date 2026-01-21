import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import LandingPage from './components/LandingPage';
import GamePage from './components/GamePage';

import './App.css'
import { WebSocketProvider } from './services/WebSocket';
import LoginPage from './components/LoginPage';

import { tryLogin, tryRegister } from "./services/Login";
import RegisterPage from './components/RegisterPage';
import { AuthProvider } from './services/AuthContext';

const App: React.FC = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/register" element={<RegisterPage onRegister={tryRegister} />}/>
          <Route path="/login" element={<LoginPage onLogin={tryLogin} />}/>
          <Route path="/" element={<LandingPage />}/>
          <Route path="/g" element={<WebSocketProvider><GamePage /></WebSocketProvider>}/>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
};

export default App;
