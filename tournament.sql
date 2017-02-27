-- Initialize
DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS matches;
DROP VIEW if EXISTS standings;

-- Tables
CREATE TABLE players (id SERIAL PRIMARY KEY, name VARCHAR(40), UNIQUE (id, name));
CREATE TABLE matches (id SERIAL PRIMARY KEY, winner integer references players(id), loser integer references players(id))

-- Views
CREATE OR REPLACE VIEW standings AS SELECT players.id, players.name, (SELECT COUNT(*) FROM matches WHERE matches.winner = players.id OR matches.loser = players.id) AS matches, (SELECT COUNT(*) FROM matches WHERE matches.winner = players.id) AS wins, (SELECT COUNT(*) FROM matches WHERE matches.loser = players.id) AS loss FROM players;
