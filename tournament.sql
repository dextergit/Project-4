-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP TABLE IF EXISTS players;

CREATE TABLE players (id SERIAL PRIMARY KEY, name VARCHAR(40), UNIQUE (id, name));
CREATE TABLE matches (id SERIAL PRIMARY KEY, winner integer references players(id), loser integer references players(id))


-- insert into players (name) values ('joe1');
-- insert into players (name) values ('joe2');
-- insert into players (name) values ('joe3');
-- insert into players (name) values ('joe4');
-- insert into players (name) values ('joe5');
