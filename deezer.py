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
    conn = sqlite3.connect('top_100_songs.db')
    cur = conn.cursor()
    return cur, conn



def getSongList(cur, conn):
    #returns list of song names
    
    songs_tup = []
    cur.execute(f'SELECT song_name FROM Hot_100_Songs')
    for names in cur.fetchall():
        songs_tup.append(names)


    song_list = [item for i in songs_tup for item in i]
    names_no_spaces = []
    for i in song_list:
        names_no_spaces.append(i.replace(' ','-'))
    #replace space with hyphen so that search will work
    return names_no_spaces


def makeDeezerTable(cur):
    '''Creates a table to hold Deezer information
    '''
    cur.execute(f'CREATE TABLE IF NOT EXISTS Deezer (artist_id INTEGER PRIMARY KEY, song_name TEXT, artist_name TEXT, songs_deezer_rank INTEGER, artist_fan_number INTEGER)')

def getReq(base):
    '''Takes in the api request and returns in a dictionary format
    '''
    r = requests.get(base)
    if r.status_code == 200:
        return json.loads(r.content)
    else:
        return None

def getDeezData(base, cur, conn):
    '''Calls on the getArtistList function. Loops thru the list of artists and retrieves each search url. If there is data 
    for a given artist, returns number of fans for each artist in a list
    '''

    song_names = getSongList(cur, conn)
    song_ranks = []
    for rank in song_names:
        song_url = base + 'search/track?q={}'.format(rank)
        song_data = getReq(song_url)

        if len(song_data["data"]) == 0 or song_data == None:
           continue

        song_rank = song_data["data"][0]['rank']
        song_ranks.append(song_rank)
    
    #get artist name
    artist_names = []

    for song in song_names: 
        artist_url = base + 'search/track?q={}'.format(song)
        artist_data = getReq(artist_url)

        if len(artist_data["data"]) == 0 or artist_data == None:
           continue
        artist = artist_data['data'][0]['artist']['name']
        artist_names.append(artist.replace(' ','-'))

    artist_fans = []
    #print(artist_names)
    #print(len(artist_names))
    for person in artist_names:
        fan_url = base + 'search/artist?q={}'.format(person)
        fan_data = getReq(fan_url)

        
        fans = fan_data['data'][0]['nb_fan']
        artist_fans.append(fans)
    


    DeezData = [(song_names[i], artist_names[i], song_ranks[i], artist_fans[i]) for i in range(0, len(song_names))]
    return DeezData
    



    
def fillTable(cur, conn):
    '''Fills up Deezer table
    '''
    data = getDeezData(base, cur, conn)
    artist_id = 0
    for artist in data:
        artist_id += 1
        song_name = artist[0]
        artist_name = artist[1]
        songs_deezer_rank = artist[2]
        artist_fan_number = artist[3]
        cur.execute('INSERT OR IGNORE INTO Deezer (artist_id, song_name, artist_name, songs_deezer_rank, artist_fan_number) VALUES (?,?,?,?,?)', (artist_id, song_name, artist_name, songs_deezer_rank, artist_fan_number))
    conn.commit()
    print('done')


def main():
    cur, conn = setUpDatabase('top_100_songs.db')
    makeDeezerTable(cur)
    getReq(base)
    getDeezData(base, cur, conn)
    fillTable(cur, conn)

if __name__ == "__main__":
    main()

