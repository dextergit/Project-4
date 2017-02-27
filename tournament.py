#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import math


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""

    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""

    conn = connect()
    c = conn.cursor()
    c.execute("TRUNCATE TABLE matches;")
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("TRUNCATE TABLE players CASCADE;")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    number_of_players = 0
    conn = connect()
    c = conn.cursor()
    SQL="SELECT COUNT(*) FROM players;"
    c.execute(SQL)
    number_of_players = c.fetchone()
    conn.close()
    return number_of_players[0]


def registerPlayer(fullname):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    SQL="INSERT INTO players (name) VALUES (%s)"
    params=((fullname, ))
    c.execute(SQL, params )
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should
    be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    players = []

    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM rank ORDER BY wins DESC;")
    results = c.fetchall()

    for row in results:
        players.append((row[0], row[1], row[3], row[2]))

    conn.close()
    return players


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    conn = connect()
    c = conn.cursor()
    SQL="INSERT INTO matches (winner, loser) VALUES (%s, %s)"
    params=(winner, loser, )
    c.execute(SQL, params)
    conn.commit()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    pairings = []
    number_of_players = countPlayers()
    pairs = number_of_players / 2
    rounds = int(math.log(number_of_players, 2))

    conn = connect()
    c = conn.cursor()
    SQL="SELECT id, name FROM rank ORDER BY wins DESC;"
    c.execute(SQL)
    results = c.fetchall()

    pair_count = 1
    pair_index = 0

    while (pair_count <= pairs):
        player1 = results[pair_index]
        player2 = results[pair_index + 1]
        pair_index += 2
        pair_count += 1
        pairings.append((player1[0], player1[1], player2[0], player2[1]))

    return pairings
