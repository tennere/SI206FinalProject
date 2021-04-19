import requests
import re
import os 
import csv
import sqlite3
import json 


base = 'https://api.deezer.com/'

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect('top_100_artists.db')
    cur = conn.cursor()
    return cur, conn

def getArtistList(cur, conn):
     #List of tuples of artist names
    artists_tup = []
    cur.execute(f'SELECT name FROM Hot_100_Artists')
    for names in cur.fetchall():
        artists_tup.append(names)

    
    #change tuple to list
    artists_list = [item for t in artists_tup for item in t]
    names_no_spaces = []
    for i in artists_list:
        names_no_spaces.append(i.replace(' ',''))
    return names_no_spaces
    
def makeDeezerTable(cur):
    cur.execute(f'CREATE TABLE IF NOT EXISTS Deezer (artist id TEXT, name TEXT)')

def getReq(base):
    r = requests.get(base)
    if r.status_code == 200:
        return json.loads(r.content)
    else:
        return None

def artist_url(base, cur, conn):
    artists = getArtistList(cur, conn)
    for artist in artists:
        artist_url = base + 'search/artist?q={}'.format(artist)
        artist_data = getReq(base)

        if len(artist_data["data"]) == 0 or artist_data == None:
           continue

        artist_id = artist_data["data"][0]['id']

    print(artist_id)

def main():
    cur, conn = setUpDatabase('top_100_artists.db')
    getArtistList(cur,conn)
    makeDeezerTable(cur)
    getReq(base)
    artist_url(base, cur, conn)


if __name__ == "__main__":
    main()

#DEEZER_APP_ID = "473902"
#DEEZER_APP_SECRET = "6db382500bf99d5bbd8fd1b0820a549d"
#DEEZER_REDIRECT_URI = "https://deezer-player.si206.me"

