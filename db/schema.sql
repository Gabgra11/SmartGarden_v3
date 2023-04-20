DROP TABLE IF EXISTS data;
DROP TABLE IF EXISTS votes;

CREATE TABLE data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp INTEGER NOT NULL,
    moisture REAL,
    humidity REAL,
    temperature REAL
);

CREATE TABLE votes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp INTEGER NOT NULL,
    vote INTEGER NOT NULL, 
    user TEXT NOT NULL
);