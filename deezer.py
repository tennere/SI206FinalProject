import requests
import re
import os 
import csv
import sqlite3
import json 

#base url 
base = 'https://api.deezer.com/'

def setUpDatabase(db_name):
    '''takes in the database, returns cursor and connection
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect('top_100_artists.db')
    cur = conn.cursor()
    return cur, conn

def getArtistList(cur, conn):
    '''Returns a list of artist names
    '''
     #List of tuples of artist names
    artists_tup = []
    cur.execute(f'SELECT name FROM Hot_100_Artists')
    for names in cur.fetchall():
        artists_tup.append(names)

    
    #change tuple to list
    artists_list = [item for t in artists_tup for item in t]
    names_no_spaces = []
    for i in artists_list:
        names_no_spaces.append(i.replace(' ','-'))
    #replace space with hyphen so that search will work
    return names_no_spaces
    
def makeDeezerTable(cur):
    '''Creates a table to hold Deezer information
    '''
    cur.execute(f'CREATE TABLE IF NOT EXISTS Deezer (artist_id INTEGER PRIMARY KEY, name TEXT, num_fans INTEGER)')

def getReq(base):
    '''Takes in the api request and returns in a dictionary format
    '''
    r = requests.get(base)
    if r.status_code == 200:
        return json.loads(r.content)
    else:
        return None

def getNumFans(base, cur, conn):
    '''Calls on the getArtistList function. Loops thru the list of artists and retrieves each search url. If there is data 
    for a given artist, returns number of fans for each artist in a list
    '''
    artist_names = getArtistList(cur, conn)
    artist_fans = []
    for artist in artist_names:
        artist_url = base + 'search/artist?q={}'.format(artist)
        artist_data = getReq(artist_url)
        #print(artist_url)

        if len(artist_data["data"]) == 0 or artist_data == None:
           continue
        #print(artist_url)

        num_fans = artist_data["data"][0]['nb_fan']
        artist_fans.append(num_fans)
    fans_tup = [(artist_names[i], artist_fans[i]) for i in range(0, len(artist_fans))]
    print(fans_tup)

    return fans_tup

    


def main():
    cur, conn = setUpDatabase('top_100_artists.db')
    getArtistList(cur,conn)
    makeDeezerTable(cur)
    getReq(base)
    getNumFans(base, cur, conn)


if __name__ == "__main__":
    main()

