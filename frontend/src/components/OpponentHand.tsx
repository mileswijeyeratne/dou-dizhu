import React from "react"

import "./OpponentHand.css"
import { Card, CARD_WIDTH } from "./Card";

const OPPONENT_HAND_OVERLAP = 70;
const OUTSIDE_PADDING = 30;

interface OpponentHandProps {
    cardCount: number;
    position: "left" | "right";
    landlord: boolean;
    name: string;
}

const OpponentHand: React.FC<OpponentHandProps> = ({ cardCount, position, landlord, name }) => {
    // todo render landlord
    return (
        <div className={`opponent-hand ${landlord ? "landlord" : ""}`}>
            {Array(cardCount).fill(0).map((_, index) => (
                <div
                    className="opponent-card-container" 
                    key={index}
                    style={position === "left" ? {
                        left: `${OUTSIDE_PADDING + index * (CARD_WIDTH - OPPONENT_HAND_OVERLAP)}px`
                    } : {
                        right: `${OUTSIDE_PADDING + index * (CARD_WIDTH - OPPONENT_HAND_OVERLAP)}px`
                    }}
                >
                    <Card faceDown={true} />
                </div>
            ))}
            <p
                className={`opponent-card-count card-count-position-${position}`}
                style={position === "left" ? {
                    left: `${CARD_WIDTH / 2 + OUTSIDE_PADDING + (cardCount-1) * (CARD_WIDTH - OPPONENT_HAND_OVERLAP)}px`
                } : {
                    right: `${CARD_WIDTH / 2 + OUTSIDE_PADDING + (cardCount-1) * (CARD_WIDTH - OPPONENT_HAND_OVERLAP)}px`
                }}
            >
                {cardCount}
            </p>
            <p
                className="opponent-name"
            >
                {name}
            </p>
        </div>
    );
};

export default OpponentHand;