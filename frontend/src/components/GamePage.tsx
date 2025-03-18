import React from "react";

import "./GamePage.css"
import PlayerHand from "./PlayerHand";
import { useWebSocket } from "../services/WebSocket";
import OpponentHand from "./OpponentHand";
import LastCombo from "./LastCombo";
// import { CardType } from "../types/Card";

const GamePage: React.FC = () => {
  const { gameState, playerHand } = useWebSocket();

  // placeholder cards
  // const cards: CardType[] = [
  //   {rank: "2", suit: "clubs"},
  //   {rank: "2", suit: "spades"},
  //   {rank: "2", suit: "hearts"},
  //   {rank: "small", suit: "joker"},
  // ];
  // const cards2: CardType[] = [
  //   {rank: "8", suit: "hearts"},
  //   {rank: "J", suit: "clubs"},
  //   {rank: "K", suit: "spades"},
  //   {rank: "big", suit: "joker"},
  // ];

  return (
    <div className="game-page">
      <h1 className="title">--title bar placeholder--</h1>

      <div className="opponents-container">
        <OpponentHand cardCount={15} position="left" landlord={false} /> 
        <OpponentHand cardCount={7} position="right" landlord={true} />
      </div>

      {/*
      Placeholder cards
      <LastCombo cards={cards}/>
      <PlayerHand cards={cards2} />
      */}

      <LastCombo cards={gameState?.lastPlayedCombo || []}/>
      <PlayerHand cards={playerHand ? playerHand : []} />
    </div>
  );
};

export default GamePage;