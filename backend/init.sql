CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    running_total INTEGER,
    username TEXT
)