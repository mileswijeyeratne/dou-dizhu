import Card from "./components/Card"

import './App.css'


function App() {

  return ( <>
    <Card faceDown={false} suit="clubs" rank="J" />
    <Card faceDown={true} suit="clubs" rank="J" />
    <Card faceDown={false} suit="diamonds" rank="A" />
    <Card faceDown={false} suit="hearts" rank="9" />
    <Card faceDown={false} suit="spades" rank="8" />
    <Card faceDown={false} suit="joker" rank="big" />
    <Card faceDown={false} suit="joker" rank="small" />
  </>)
}

export default App
