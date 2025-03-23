import React, { createContext, useCallback, useContext, useEffect, useState, useRef } from "react";

import { CardType } from "../types/Card";

const SERVER_URL = "ws://localhost:3000/ws";

// interface Player {
//     playerId: string;
//     name: string;
// };

export interface GameState {
    gameId: string;

    gamePhase: "pregame" | "bidding" | "gameplay" | "over";
    players: string[];  // will include self
    currentPlayerTurnId: string;
    numberOfCards: Map<string, number>;
    bids: Map<string, number>;
    stake: number;
    tableCards: CardType[];
    landlordId: string | null;  // null indiates landlord not decided yet
    lastPlayedCombo: CardType[];
};

interface WebSocketContextType {
    isConnected: boolean;
    connect: () => void;
    sendMsg: (data: any) => void;
    disconnect: () => void;
    gameState: GameState | null;
    playerHand: CardType[];
    error: string | null;
};


interface WebSocketProviderProps {
    children: React.ReactNode;
};

export const WebSocketContext = createContext<WebSocketContextType | null>(null);

export const WebSocketProvider: React.FC<WebSocketProviderProps> = ({ children }) => {
    const socket = useRef<WebSocket | null>(null);
    const [isConnected, setIsConnected] = useState<boolean>(false);
    const [gameState, setGameState] = useState<GameState | null>(null);
    const [playerHand, setPlayerHand] = useState<CardType[]>([]);
    const [error, setError] = useState<string | null>(null);

    const connect = useCallback(() => {
        if (socket.current) {
            return;
        }

        try {
            let url = SERVER_URL;
            const playerId = localStorage.getItem("playerId");
            if (playerId) {
                url += `/${playerId}`;
            }
            const ws = new WebSocket(url);

            ws.onopen = () => {
                socket.current = ws;
                setIsConnected(true);
                console.log("opened conn");
                ws.send(JSON.stringify({"name": localStorage.getItem("playerName")}));
            };

            ws.onclose = () => {
                console.log("closed conn");
            };

            ws.onerror = (event) => {
                console.log(event);
            };

            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);

                if (data.id) {
                    localStorage.setItem("playerId", data.id);
                    console.log(data.id)
                }

                if (data.action == "update-hand") {
                    setPlayerHand(data.hand);
                }

                if (data.action == "update-state") {
                    console.log(data.state);
                    setGameState({...gameState, ...data.state});
                }
            };

        } catch (err) {
            setError(String(err));
            console.error(err);
        }  

    }, []);

    const disconnect = useCallback(() => {
        if (socket.current) {
            socket.current.close();
            socket.current = null;
            setIsConnected(false);
        }
    }, [])

    const sendMsg = useCallback((data: any) => {
        if (socket.current) {
            socket.current.send(data);
        }
    }, []);

    // connect when mounted and disconnect when unmounted
    useEffect(() => {
        connect();

        return () => {
            disconnect();
        };
    }, []);

    return (
        <WebSocketContext.Provider
            value = {{
                isConnected,
                connect,
                sendMsg,
                disconnect,
                gameState,
                playerHand,
                error,
            }}
        >
            {children}
        </WebSocketContext.Provider>
    )
}

export const useWebSocket = () => {
    const context = useContext(WebSocketContext);

    if (!context) {
        throw new Error("using context that doesn't exist");
    }

    return context;

};