import React, { useCallback } from "react";

import "./GamePage.css"
import PlayerHand from "./PlayerHand";
import { useWebSocket } from "../services/WebSocket";
import OpponentHand from "./OpponentHand";
import LastCombo from "./LastCombo";
import BiddingWindow from "./BiddingWindow";

const GamePage: React.FC = () => {
  const {
    gameState,
    sendMsg,
    playerHand,
  } = useWebSocket();

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
  }, []);

  const isMyBid = useCallback(() => {
    return gameState?.gamePhase == "bidding" && gameState?.currentPlayerTurnId == localStorage.getItem("playerID");
  }, [gameState]);

  return (
    <div className="game-page">
      <h1 className="title">--title bar placeholder--</h1>

      { isMyBid() ? <BiddingWindow makeBidCallback={makeBid}/> : null }

      <div className="opponents-container">
        <OpponentHand cardCount={15} position="left" landlord={false} /> 
        <OpponentHand cardCount={7} position="right" landlord={true} />
      </div>

      <LastCombo cards={gameState?.lastPlayedCombo || []}/>
      <PlayerHand cards={playerHand ? playerHand : []} playHandCallback={playHand} />
    </div>
  );
};

export default GamePage;