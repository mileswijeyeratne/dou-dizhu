import React from "react";

import "./PlayerHand.css"
import { CardType } from "../types/Card";
import { Card, CARD_WIDTH } from "./Card";

const CARD_OVERLAP = 15;

interface PlayerHandProps {
    cards: Array<CardType>;
}

const PlayerHand: React.FC<PlayerHandProps> = ({ cards }) => {
    const cardsWidth = cards.length * CARD_WIDTH - (cards.length - 1) * CARD_OVERLAP

    return (
        <div className="player-hand">
            <h2>Your Hand</h2>
            <div className="hand-cards" style={{minWidth: `${cardsWidth}px`}}>
                {cards.map((card, index) => (
                    <div
                        key={index}  // TODO icl this should change
                        className="card-wrapper"
                        style={{
                            left: `${index * (CARD_WIDTH - CARD_OVERLAP)}px`
                        }}
                    >
                        <Card faceDown={false} cardType={card}/>                    
                    </div>
                ))}
            </div>
        </div>
    )
}

export default PlayerHand;