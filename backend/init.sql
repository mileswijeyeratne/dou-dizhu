CREATE TABLE IF NOT EXISTS accounts (
    account_id SERIAL PRIMARY KEY,
    email TEXT UNIQUE,
    password_hash TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS players (
    player_id SERIAL PRIMARY KEY,
    public_player_id UUID NOT NULL,
    account_id INTEGER REFERENCES accounts (account_id),
    running_total INTEGER,
    username TEXT
);

CREATE TABLE IF NOT EXISTS games (
    game_id SERIAL PRIMARY KEY,
    public_game_id UUID NOT NULL,
    highest_bid INTEGER,
    stake INTEGER,
    landlord_id INTEGER REFERENCES players (player_id),
    player_1_id INTEGER REFERENCES players (player_id),
    player_2_id INTEGER REFERENCES players (player_id),
    landlord_won BOOLEAN
);