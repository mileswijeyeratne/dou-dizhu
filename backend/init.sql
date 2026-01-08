CREATE TABLE IF NOT EXISTS accounts (
    account_id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

CREATE TABLE IF NOT EXISTS players (
    player_id SERIAL PRIMARY KEY,
    public_player_id UUID NOT NULL,
    account_id INTEGER UNIQUE REFERENCES accounts (account_id),
    running_total INTEGER DEFAULT 0,
    username TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS games (
    game_id SERIAL PRIMARY KEY,
    public_game_id UUID NOT NULL,
    highest_bid INTEGER NOT NULL,
    stake INTEGER NOT NULL,
    landlord_id INTEGER REFERENCES players (player_id) NOT NULL,
    player_1_id INTEGER REFERENCES players (player_id) NOT NULL,
    player_2_id INTEGER REFERENCES players (player_id) NOT NULL,
    landlord_won BOOLEAN NOT NULL
);