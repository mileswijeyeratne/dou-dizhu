import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const LandingPage: React.FC = () => {
    const [playerName, setPlayerName] = useState<string>("");
    const [errorMsg, setErrorMsg] = useState<string>("");
    const navigate = useNavigate();

    const handleJoinGame = (e: React.FormEvent) => {
        e.preventDefault();
        
        if (playerName === "") {
            setErrorMsg("Please enter a name");
            return;
        }

        localStorage.setItem("playerName", playerName);

        navigate("/g")
    };

    return (
        <div className="landing-page">
            {/* title and other elements */}

            <div className="game-entry-form-container">
                <form onSubmit={handleJoinGame}>
                    <label htmlFor="playerName">Name</label>
                    <input 
                        type="text"
                        id="playerName"
                        value={playerName}
                        onChange={(e) => setPlayerName(e.target.value)}
                        placeholder="Enter name..."
                    />

                    {errorMsg && <p className="error-msg">{errorMsg}</p>}

                    <button
                        type="submit"
                        className="submit-button"
                    >
                        Join Game     
                    </button>
                </form>
            </div>
        </div>
    );
};

export default LandingPage;