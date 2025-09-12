CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    public_user_id UUID NOT NULL,
    running_total INTEGER,
    username TEXT
);

CREATE TABLE IF NOT EXISTS games (
    game_id SERIAL PRIMARY KEY,
    public_game_id UUID NOT NULL,
    highest_bid INTEGER,
    stake INTEGER,
    landlord_id INTEGER REFERENCES users (user_id),
    player_1_id INTEGER REFERENCES users (user_id),
    player_2_id INTEGER REFERENCES users (user_id),
    landlord_won BOOLEAN
);