CREATE TABLE users (
    user_id       INTEGER    PRIMARY KEY ASC AUTOINCREMENT,
    username      TEXT (255) NOT NULL,
    password_hash TEXT (64)  NOT NULL
);


CREATE TABLE profile (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id   INTEGER REFERENCES users (user_id) ON DELETE CASCADE,
    user_data TEXT    NOT NULL
);
