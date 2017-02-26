#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

# http://stackoverflow.com/questions/19191766/get-psycopg2-count-number-of-results
# https://www.postgresql.org/docs/9.1/static/datatype-numeric.html
# http://stackoverflow.com/questions/1466741/parameterized-queries-with-psycopg2-python-db-api-and-postgresql
# postgress subquery
# https://www.w3schools.com/sql/sql_join_full.asp

import psycopg2
import math


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM matches;")
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM players")
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    number_of_players = 0;
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM players;")
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
    c.execute("INSERT INTO players (name) VALUES (%s)", (fullname, ))
    conn.commit()
    conn.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    players = []
    rankPlayers()

    conn = connect()
    c = conn.cursor()
    c.execute("select id, name from players ORDER BY rank DESC")
    results = c.fetchall()

    for row in results:
        wins = getWins(row[0])
        loss = getLosses(row[0])
        players.append((row[0], row[1], int(wins), int(loss) + int(wins)))

    print players
    conn.close()
    return players

def rankPlayers():
    rank = {}
    conn = connect()
    c = conn.cursor()
    c.execute("select id from players")
    results = c.fetchall()

    for row in results:
        wins = getWins(row[0])
        loss = getLosses(row[0])
        rank[row[0]] = wins - loss

    for key in rank:
        c.execute("UPDATE players SET rank = %s WHERE id = %s", (rank[key], key, ))
        conn.commit()

    conn.close()

def getWins(player_id):
    wins = 0;
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM matches WHERE winner = (%s);", (player_id,))
    wins = c.fetchone()
    conn.close()
    return wins[0]

def getLosses(player_id):
    losses = 0;
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM matches WHERE loser = (%s);", (player_id,))
    losses = c.fetchone()
    conn.close()
    return losses[0]

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO matches (winner, loser) VALUES (%s,%s)", (winner, loser, ))
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

    rankPlayers()

    pairings = []
    number_of_players = countPlayers()
    pairs = number_of_players / 2
    rounds =  int(math.log(number_of_players,2))

    conn = connect()
    c = conn.cursor()
    c.execute("select id, name from players ORDER BY rank DESC")
    results = c.fetchall()

    i = 1
    index = 0
    while (i <= pairs):
       #print 'The count is:', i

       p1 = results[index]
       p2 = results[index + 1]
       index = index + 2
       #print(str(p1) + ", " + str(p2))
       i +=1

       pairings.append((p1[0], p1[1], p2[0], p2[1]))

    print(pairings)
    return pairings

       #
    #    results.pop(0)
    #    results.pop(1)

    # print results
    # results.pop(0)
    # print results
    # print results[0]

    # i=0;
    # for row in results:
    #     print(row)
    #     i += 1
    #     if i == pairs:
    #         print "reached"
    #         i=0
