#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM matches;")
    cur.execute("DELETE FROM standings;")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""

    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM standings;")
    cur.execute("DELETE FROM players;")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""

    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM players;")
    result=cur.fetchone()
    conn.close()
    return result[0]



def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO players (id,name) VALUES (DEFAULT, (%s) ) RETURNING id", (name,))
    idplayer = cur.fetchone()[0]
    cur.execute ("INSERT INTO standings (id_player,n_wins, n_loss) VALUES (%s,%s,%s)", (idplayer, 0, 0))
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

    conn = connect()
    cur = conn.cursor()
    cur.execute(" SELECT players.id, players.name, standings.n_wins, standings.n_wins + standings.n_loss FROM players,standings WHERE players.id = standings.id_player ORDER BY standings.n_wins DESC; ")
    rows = cur.fetchall()
    conn.close()
    return rows


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO matches (id_match, id_player1, id_player2, winner) VALUES (DEFAULT, %s, %s, %s) ; ", (winner, loser, winner))
    cur.execute("UPDATE standings SET n_wins = n_wins+1 WHERE id_player =  %s ;", (winner,))
    cur.execute("UPDATE standings SET n_loss = n_loss+1 WHERE id_player =  %s ;", (loser,))
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

    ranks = playerStandings()
    pairs = []

    for i in range(0,len(ranks),2):
        pairs.append(( ranks[i][0], ranks[i][1] , ranks[i+1][0] , ranks[i+1][1] ))

    return pairs
        







