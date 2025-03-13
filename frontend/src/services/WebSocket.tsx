import React, { createContext, useCallback, useContext, useEffect, useState } from "react";

import { CardType } from "../types/Card";

const SERVER_URL = "ws://localhost/ws";

interface Player {
    playerId: string;
    name: string;
};

export interface GameState {
    gameId: string;

    gamePhase: "pregame" | "bidding" | "gameplay" | "over";
    players: Player[];  // will include self
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
    playerHand: CardType[] | null;
    error: string | null;
};


interface WebSocketProviderProps {
    children: React.ReactNode;
};

export const WebSocketContext = createContext<WebSocketContextType | null>(null);

export const WebSocketProvider: React.FC<WebSocketProviderProps> = ({ children }) => {
    const [socket, setSocket] = useState<WebSocket | null>(null);
    const [isConnected, setIsConnected] = useState<boolean>(false);
    const [gameState, setGameState] = useState<GameState | null>(null);
    const [playerHand, setPlayerHand] = useState<CardType[] | null>(null);
    const [error, setError] = useState<string | null>(null);

    const connect = useCallback(() => {
        if (socket) {
            return;
        }

        try {
            const ws = new WebSocket(SERVER_URL);

            ws.onopen = () => {
                console.log("opened conn");
            };

            ws.onclose = () => {
                console.log("closed conn");
            };

            ws.onerror = (event) => {
                console.log(event);
            };

            ws.onmessage = (event) => {
                console.log(event);
            };

        } catch (err) {
            setError(String(err));
            console.error(err);
        }  

    }, [socket]);

    const disconnect = useCallback(() => {
        if (socket) {
            socket.close();
            setSocket(null);
            setIsConnected(false);
        }
    }, [socket])

    const sendMsg = useCallback((data: any) => {

    }, []);

    // connect when mounted and disconnect when unmounted
    useEffect(() => {
        connect();

        return () => {
            disconnect();
        };
    }, [connect, disconnect]);

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