import React from "react";
import { CardType } from "../types/Card";
import { Card } from "./Card";

import "./LastCombo.css"

interface LastComboProps {
    cards: CardType[];
};

const LastCombo: React.FC<LastComboProps> = ({ cards }) => {
    return (
        <div className="last-combo">
            {cards.map((card, index) => (
                <div className="last-combo-card-wrapper" key={index}>
                    <Card faceDown={false} cardType={card} />
                </div>
            ))}
        </div>
    );
};

export default LastCombo;