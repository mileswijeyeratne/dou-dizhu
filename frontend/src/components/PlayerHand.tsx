import React, { useState } from "react";

import "./PlayerHand.css"
import { CardType } from "../types/Card";
import { Card, CARD_WIDTH } from "./Card";

const CARD_OVERLAP = 15;

interface PlayerHandProps {
    cards: Array<CardType>;
    playHandCallback: (selectedCards: boolean[]) => void;
}

const PlayerHand: React.FC<PlayerHandProps> = ({ cards, playHandCallback }) => {
    const cardsWidth = cards.length * CARD_WIDTH - (cards.length - 1) * CARD_OVERLAP

    const [isSelected, setIsSelected] = useState<boolean[]>(new Array(cards.length).fill(false));

    return (
        <div className="player-hand">
            <h2>Your Hand</h2>
            <div 
                className="hand-cards"
                style={{minWidth: `${cardsWidth}px`}}
            >
                {cards.map((card, index) => (
                    <div
                        key={index}  // TODO icl this should change
                        className={`card-wrapper ${isSelected[index] ? "selected" : ""}`}
                        style={{
                            left: `${index * (CARD_WIDTH - CARD_OVERLAP)}px`
                        }}
                        onClick={() => {
                            setIsSelected(isSelected.map((val, i) => (
                                i == index ? !val : val
                            )));
                        }}
                    >
                        <Card faceDown={false} cardType={card}/>                    
                    </div>
                ))}
            </div>
            <button
                onClick={() => playHandCallback(isSelected)}
            >
            Play hand
            </button>
        </div>
    )
}

export default PlayerHand;