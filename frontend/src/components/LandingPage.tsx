import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import FormCard from "./FormCard";

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
            <FormCard title="Join Game">
                <form onSubmit={handleJoinGame}>
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
                        Join    
                    </button>
                </form>
            </FormCard>
        </div>
    );
};

export default LandingPage;