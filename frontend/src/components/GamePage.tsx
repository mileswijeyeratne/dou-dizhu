import React from "react";

import PlayerHand from "./PlayerHand";
import { CardType } from "../types/Card";

const GamePage: React.FC = () => {
  // placeholder hand
  const hand: Array<CardType> = [
    {rank: "9", suit: "diamonds"},
    {rank: "8", suit: "hearts"},
    {rank: "9", suit: "diamonds"},
    {rank: "9", suit: "diamonds"},
    {rank: "8", suit: "hearts"},
    {rank: "9", suit: "diamonds"},
    {rank: "8", suit: "hearts"},
    {rank: "J", suit: "clubs"},
    {rank: "K", suit: "spades"},
    {rank: "big", suit: "joker"},
    {rank: "9", suit: "diamonds"},
    {rank: "8", suit: "hearts"},
    {rank: "J", suit: "clubs"},
    {rank: "K", suit: "spades"},
    {rank: "big", suit: "joker"},
    {rank: "9", suit: "diamonds"},
    {rank: "8", suit: "hearts"},
    {rank: "J", suit: "clubs"},
    {rank: "K", suit: "spades"},
    {rank: "big", suit: "joker"},
  ];

  return (
    <PlayerHand cards={hand} />
  );
};

export default GamePage;