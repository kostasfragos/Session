CREATE TABLE users (
    user_id       INTEGER    PRIMARY KEY ASC AUTOINCREMENT,
    username      TEXT (255) NOT NULL,
    password_hash TEXT (64)  NOT NULL
);

-- CREATE TABLE users (
    -- `user_id` INTEGER PRIMARY KEY ASC, 
    -- `username` VARCHAR(255) NOT NULL,
    -- `password_hash` VARCHAR(64) NOT NULL
-- );

