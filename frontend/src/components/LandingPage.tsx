import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import FormCard from "./FormCard";
import { useAuth } from "../services/AuthContext";

import "./LandingPage.css";

const LandingPage: React.FC = () => {
    const [playerName, setPlayerName] = useState<string>("");
    const [roomId, setRoomId] = useState<string>("");
    const [errorMsg, setErrorMsg] = useState<string>("");
    const navigate = useNavigate();
    const { isLoggedIn, email, logout } = useAuth();

    useEffect( () => {
        const storedName = localStorage.getItem("playerName");
        if (storedName) {
            setPlayerName(storedName);
        }
    }, [])

    const handleJoinGame = (e: React.FormEvent) => {
        e.preventDefault();
        
        if (playerName === "") {
            setErrorMsg("Please enter a name");
            return;
        }

        localStorage.setItem("playerName", playerName);
        localStorage.setItem("roomId", roomId);

        navigate("/g")
    };

    return (
        <div className="landing-page">
            <div className="auth-status">
                {isLoggedIn ? (
                    <div className="logged-in">
                        <span>✓ Logged in as <strong>{email}</strong></span>
                        <button onClick={logout} className="logout-btn">Logout</button>
                    </div>
                ) : (
                    <div className="not-logged-in">
                        <span>Not logged in (playing anonymously)</span>
                        <button onClick={() => navigate("/login")} className="login-btn">Login</button>
                    </div>
                )}
            </div>

            <FormCard title="Join Game">
                <form onSubmit={handleJoinGame}>
                    <input 
                        type="text"
                        id="playerName"
                        value={playerName}
                        onChange={(e) => setPlayerName(e.target.value)}
                        placeholder="Enter name..."
                    />

                    <input 
                        type="text"
                        id="roomId"
                        value={roomId}
                        onChange={(e) => setRoomId(e.target.value)}
                        placeholder="(optional) Enter room ID..."
                    />

                    {errorMsg && <p className="error-message">{errorMsg}</p>}

                    <button
                        type="submit"
                        className="submit-button"
                    >
                        Join    
                    </button>
                </form>
            </FormCard>
        </div>
    );
};

export default LandingPage;