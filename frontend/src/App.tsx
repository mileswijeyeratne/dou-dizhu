import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import LandingPage from './components/LandingPage';
import GamePage from './components/GamePage';

import './App.css'

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />}/>
        <Route path="/g" element={<GamePage />}/>
      </Routes>
    </BrowserRouter>
  )
};

export default App
