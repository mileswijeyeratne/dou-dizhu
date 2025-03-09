export type Suit = "diamonds" | "hearts" | "clubs" | "spades" | "joker";
export type Rank = "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "10" | "J" | "Q" | "K" | "A" | "small" | "big";

export interface CardType {
    suit: Suit;
    rank: Rank;
}