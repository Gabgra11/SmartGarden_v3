DROP TABLE IF EXISTS data;
DROP TABLE IF EXISTS votes;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS waterings;
DROP TABLE IF EXISTS images;
DROP TABLE IF EXISTS notes;

CREATE TABLE data (
    id SERIAL NOT NULL PRIMARY KEY,
    timestamp INTEGER NOT NULL,
    moisture REAL,
    humidity REAL,
    temperature REAL
);

CREATE TABLE votes (
    id SERIAL NOT NULL PRIMARY KEY,
    timestamp INTEGER NOT NULL,
    vote INTEGER NOT NULL,
    userid TEXT NOT NULL
);

CREATE TABLE users (
    id TEXT PRIMARY KEY NOT NULL,
    name TEXT
);

CREATE TABLE waterings (
    timestamp INTEGER NOT NULL PRIMARY KEY
);

CREATE TABLE images (
    timestamp INTEGER NOT NULL PRIMARY KEY,
    id TEXT
);

CREATE TABLE updates (
    timestamp INTEGER NOT NULL PRIMARY KEY,
    title TEXT,
    body TEXT
);