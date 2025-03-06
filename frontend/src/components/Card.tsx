import React from "react";

import "./Card.css"

interface CardProps {
    faceDown: boolean;
    suit: string;
    rank: string;
}

const Card: React.FC<CardProps> = ({faceDown, suit, rank}) => {
    if (faceDown) {
        return (
            <div className = "card card-facedown">
            </div>
        );
    }

    if (suit === "joker") {
        const isBig = rank === "big";

        return (
            <div className={`card ${isBig ? "card-red" : "card-black"}`}>
                <div className="card-corner top-left">
                    <div className="joker-text">JOKER</div>
                </div>

                <div className="card-center">🃟</div>

                <div className="card-corner bottom-right">
                    <div className="joker-text">JOKER</div>
                </div>
            </div>
        )
    }

    const suitSymbol: string = {"hearts": '♥',
      "diamonds": "♦",
      "clubs": "♣",
      "spades": "♠"
    }[suit] || suit;

    const isRed: boolean = suit === "hearts" || suit == "diamonds";


    return (
        <div className={`card ${isRed ? "card-red" : "card-black"}`}>
            <div className="card-corner top-left">
                <div className="card-rank">{rank}</div>
                <div className="card-suit">{suitSymbol}</div>
            </div>

            <div className="card-center">{suitSymbol}</div>

            <div className="card-corner bottom-right">
                <div className="card-suit">{suitSymbol}</div>
                <div className="card-rank">{rank}</div>
            </div>
        </div>
    )
}

export default Card;