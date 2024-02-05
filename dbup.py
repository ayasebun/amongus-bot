#!/usr/bin/python3.10
import sqlite3
import collections
from terminaltables import AsciiTable

# Check if user exists in the database
def leaderboardExists(userid,guildid):
    LBData = collections.namedtuple('LBData', 'Ranking, userid, counter')
    conn = sqlite3.connect('leaderboard.db')
    c = conn.cursor()

    usersql = f"INSERT OR IGNORE INTO badlist VALUES (\"{userid}\",\"{guildid}\",0)"
    c.execute(usersql)

    guildsql = f"""UPDATE badlist SET guild_ids = CASE WHEN guild_ids NOT LIKE "%{guildid}%" THEN guild_ids || ",{guildid}" ELSE guild_ids END WHERE user_id = {userid};"""
    c.execute(guildsql)
    conn.commit()


# GATHER - Obtain Leaderboard Placement
def leaderboardCheck(userid,guildid):
    LBData = collections.namedtuple('LBData', 'Ranking, userid, counter')
    conn = sqlite3.connect('leaderboard.db')
    c = conn.cursor()

    # Obtain ORDER BY list based on number of times a no-no word is said, passing the user ID
    #checksql = f"""SELECT Ranking, user_id, counter FROM (SELECT RANK () OVER (ORDER BY counter DESC) Ranking, user_id, counter FROM badlist) WHERE user_id = {userid} AND guild_ids LIKE "%{guildid}%\""""

    checksql = f"""
    SELECT Ranking, user_id, counter FROM (SELECT RANK () OVER (ORDER BY counter DESC) Ranking, user_id, counter FROM badlist WHERE guild_ids LIKE "%{guildid}%") WHERE user_id = {userid}
    """

    c.execute(checksql)
    # Return the user's Placement in list, User ID, and Counter Value in a table

    for lb_entry in map(LBData._make, c.fetchall()):
        print(lb_entry.Ranking, lb_entry.userid, lb_entry.counter)

    # Get out of SQLite3
    conn.commit()
    return lb_entry


# GATHER - Obtain Leaderboard Listing Top 10
def leaderboardTopFour(guildid):
    # Obtain ORDER BY list based on number of times a no no word is said and only return the first 10 entries.
    #LBTop = collections.namedtuple('LBTop', 'userid, counter')
    LBGive = []
    conn = sqlite3.connect('leaderboard.db')
    c = conn.cursor()

#    topsql = """
#    SELECT Ranking, user_id, counter FROM (SELECT RANK () OVER (ORDER BY counter DESC) Ranking, user_id, counter FROM badlist LIMIT 4)
#    """

    # Redoing the query to include the Guild ID
    topsql = f"""
    SELECT Ranking, user_id, counter FROM (SELECT RANK () OVER (ORDER BY counter DESC) Ranking, user_id, counter FROM badlist WHERE guild_ids LIKE "%{guildid}%") LIMIT 4
    """

    c.execute(topsql)

    #for lb_top in map(LBTop._make, c.fetchall()):
    for lb_top in (c.fetchall()):
        LBGive.append(lb_top)

    conn.commit()
    return LBGive

    # Return the list with Placement, User ID, Counter Value

# CHANGE - Increment value for Leaderboard Placements

def incrementCount(userid, guildid):
    conn = sqlite3.connect('leaderboard.db')
    c = conn.cursor()
    leaderboardExists(userid,guildid)

    # UPDATE Counter Value by 1 based on the user ID that was detected saying a no-no word
    upsql = """
    UPDATE badlist SET counter = counter + 1 WHERE user_id = %s
    """

    # Get out of DB
    c.execute(upsql % (userid))

    conn.commit()