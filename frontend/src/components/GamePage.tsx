import React, { useCallback, useEffect } from "react";

import "./GamePage.css"
import PlayerHand from "./PlayerHand";
import { useWebSocket } from "../services/WebSocket";
import OpponentHand from "./OpponentHand";
import LastCombo from "./LastCombo";
import BiddingWindow from "./BiddingWindow";

const GamePage: React.FC = () => {
  const {
    gameState,
    roomInfo,
    sendMsg,
    playerHand,
  } = useWebSocket();

  // TESTING (not landlord always skips)
  // useEffect(() => {
  //   if (gameState?.gamePhase == "gameplay" && gameState?.landlordId != localStorage.getItem("playerId") && gameState?.currentPlayerTurnId == localStorage.getItem("playerId")) {
  //     sendMsg(JSON.stringify({"action": "skip"}))
  //   }
  // }, [gameState]);

  const makeBid = useCallback((amount: number) => {
    sendMsg(JSON.stringify({
      "action": "bid",
      "amount": amount
    }));
  }, []);

  const playHand = useCallback((selectedCards: boolean[]) => {
    sendMsg(JSON.stringify({
      "action": "play",
      "cards": playerHand.filter((_, index) => selectedCards[index])
    }));
  }, [playerHand]);

  const skipTurn = useCallback(() => {
    sendMsg(JSON.stringify({
      "action": "skip"
    }))
  }, [])

  const myPlayerIndex = useCallback(() => {
    return gameState?.players.findIndex((player) => player.playerId === localStorage.getItem("playerId"));
  }, [gameState]);

  const oppoonentPlayer = useCallback((position: "left" | "right") => {
    const selfIndex = myPlayerIndex();
    if (selfIndex === undefined) return null;
    const offset = position === "left" ? 2 : 1;
    return gameState?.players[(selfIndex + offset) % 3];
  }, [gameState, myPlayerIndex]);
  
  const opponentId = useCallback((position: "left" | "right") => {
    return oppoonentPlayer(position)?.playerId || "";
  }, [gameState, myPlayerIndex]);

  const opponentName = useCallback((position: "left" | "right") => {
    return oppoonentPlayer(position)?.name || "";
  }, [gameState, myPlayerIndex]);

  const isMyBid = useCallback(() => {
    return gameState?.gamePhase == "bidding" && gameState?.currentPlayerTurnId == localStorage.getItem("playerId");
  }, [gameState]);

  const isMyTurn = useCallback(() => {
    return gameState?.gamePhase == "gameplay" && gameState?.currentPlayerTurnId == localStorage.getItem("playerId");
  }, [gameState]);

  return (
    <div className="game-page">
      <h1 className="title">{roomInfo?.isPrivate ? `Private room ${roomInfo?.roomId}` : "Public room"}</h1>

      { isMyBid() ? <BiddingWindow makeBidCallback={makeBid}/> : null }

      <div className="opponents-container">
        <OpponentHand
          cardCount={gameState?.numberOfCards?.get(opponentId("left")) || 0}
          position="left"
          landlord={gameState?.landlordId === opponentId("left") || false}
          name={opponentName("left")}
        /> 
        <OpponentHand
          cardCount={gameState?.numberOfCards?.get(opponentId("right")) || 0}
          position="right"
          landlord={gameState?.landlordId === opponentId("right") || false}
          name={opponentName("right")}
        /> 
      </div>

      <LastCombo cards={gameState?.lastPlayedCombo || []}/>
      <PlayerHand
        cards={playerHand ? playerHand : []}
        playHandCallback={playHand}
        skipTurnCallback={skipTurn}
        isMyTurn={isMyTurn}
      />
    </div>
  );
};

export default GamePage;