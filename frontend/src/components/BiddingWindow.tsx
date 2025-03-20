import React from "react";

import "./BiddingWindow.css"

interface BiddingWindowProps {
    makeBidCallback: (amount: number) => void;
};

const BiddingWindow: React.FC<BiddingWindowProps> = ({ makeBidCallback }) => {
    return (
        <div className="bidding-window">
            <h1>Your bid</h1>            

            <button
                onClick={() => makeBidCallback(1)}
            >1</button>
            <button
                onClick={() => makeBidCallback(2)}
            >2</button>
            <button
                onClick={() => makeBidCallback(3)}
            >3</button>

            <button
                onClick={() => makeBidCallback(0)}
            >Skip</button>
        </div>
    );
};

export default BiddingWindow;