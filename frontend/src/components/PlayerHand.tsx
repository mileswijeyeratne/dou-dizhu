import React, { useEffect, useState } from "react";

import "./PlayerHand.css"
import { CardType } from "../types/Card";
import { Card, CARD_WIDTH } from "./Card";

const CARD_OVERLAP = 15;

interface PlayerHandProps {
    cards: Array<CardType>;
    playHandCallback: (selectedCards: boolean[]) => void;
    skipTurnCallback: () => void;
    isMyTurn: () => boolean;
}

const PlayerHand: React.FC<PlayerHandProps> = ({ cards, playHandCallback, skipTurnCallback, isMyTurn }) => {
    const cardsWidth = cards.length * CARD_WIDTH - (cards.length - 1) * CARD_OVERLAP

    const [isSelected, setIsSelected] = useState<boolean[]>([]);

    useEffect(() => {
        setIsSelected(new Array(cards.length).fill(false));
    }, [cards])

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
                disabled={!isMyTurn()}
                onClick={() => playHandCallback(isSelected)}
            >
                Play hand
            </button>
            <button
                disabled={!isMyTurn()}
                onClick={skipTurnCallback}
            >
                Skip
            </button>
        </div>
    )
}

export default PlayerHand;