import { CardType } from "./types/Card"
import PlayerHand from "./components/PlayerHand"

import './App.css'


function App() {
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
  )
}

export default App
