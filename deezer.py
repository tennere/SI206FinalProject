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

'''def getSongList(cur, conn):
    #returns list of song names
    songs_tup = []
    cur.execute(f'SELECT song_name FROM Hot_100_Songs')
    for names in cur.fetchall():
        songs_tup.append(names)

    song_list = [item for i in songs_tup for item in i]
    songs_no_spaces = []
    for i in song_list:
        songs_no_spaces.append(i.replace(' ','-'))
    #replace space with hyphen so that search will work
    return songs_no_spaces'''

def getInfo(cur, conn):
    cur.execute(f'SELECT song_name, artist FROM Hot_100_Songs')
    songArt = cur.fetchall()
    artists = []
    artists_no_featuring = []
    songs = []
    songs_no_spaces = []
    for i in songArt:
        artists.append(i[1])
    for i in artists:
        if 'Featuring' in i or 'Duet' in i or '&' in i:
            no_featuring = i.split('Featuring')[0]
            artists_no_featuring.append(no_featuring.replace(' ','-'))
        else:
            artists_no_featuring.append(i.replace(' ','-'))
    for i in songArt:
        songs.append(i[0])
    for i in songs:
        songs_no_spaces.append(i.replace(' ','-'))
    
    deezer_ranks = []

    for song in songs_no_spaces:
        song_url = base + 'search/track?q={}'.format(song)
        song_data = getReq(song_url)

        if len(song_data["data"]) == 0 or song_data == None:
            ranks = 'N/A'

        ranks = song_data['data'][0]['rank']
        deezer_ranks.append(ranks)
    
    fan_numbers = []
    for person in artists_no_featuring:
        fan_url = base + 'search/artist?q={}'.format(person)
        fan_data = getReq(fan_url)

        if len(fan_data["data"]) == 0 or fan_data == None:
            fans = 'N/A'
        else:
            fans = fan_data['data'][0]['nb_fan']
        fan_numbers.append(fans)
    
        
        
        
    #print(len(songs))
    #print(len(artists))
    #print(len(deezer_ranks))
    #print(len(fan_numbers))

    
    DeezData = [(songs[i], artists[i], deezer_ranks[i], fan_numbers[i]) for i in range(0, len(songs))]
    #print(DeezData)
    return DeezData
        
     
    


def makeDeezerTable(cur):
    #Creates a table to hold Deezer information
    cur.execute(f'CREATE TABLE IF NOT EXISTS Deezer (song_id INTEGER PRIMARY KEY, song_name TEXT, artist_name TEXT, songs_deezer_rank INTEGER, artist_fan_number INTEGER)')

def getReq(base):
    #Takes in the api request and returns in a dictionary format
    
    r = requests.get(base)
    if r.status_code == 200:
        return json.loads(r.content)
    else:
        return None


def fillTable(cur, conn):
    #Fills up Deezer table
    
    data = getInfo(cur, conn)
    song_id = 0
    for song in data:
        song_id += 1
        song_name = song[0]
        artist_name = song[1]
        songs_deezer_rank = song[2]
        artist_fan_number = song[3]
        cur.execute('INSERT OR IGNORE INTO Deezer (song_id, song_name, artist_name, songs_deezer_rank, artist_fan_number) VALUES (?,?,?,?,?)', (song_id, song_name, artist_name, songs_deezer_rank, artist_fan_number))
    conn.commit()
    print('done filling table')
    

def main():
    cur, conn = setUpDatabase('top_100_songs.db')
    getInfo(cur, conn)
    makeDeezerTable(cur)
    getReq(base)
    getInfo(cur, conn)
    fillTable(cur, conn)
    

if __name__ == "__main__":
    main()

