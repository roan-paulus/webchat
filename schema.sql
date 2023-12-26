BEGIN;

CREATE TABLE IF NOT EXISTS user (
    id PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL
);

COMMIT;

