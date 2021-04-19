#Name: Emma Tenner
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import requests
import sys
import re
import os
import csv
import sqlite3
import json
import pprint

c_id = '9131842b33cd43bebd1704950e78b73a'
c_secret = 'ee9385f45c994c5183118ed534cfc240'

client_credentials_manager = SpotifyClientCredentials(client_id = c_id, client_secret = c_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)



def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect('top_100_songs.db')
    cur = conn.cursor()
    return cur, conn


def getTitleList(cur, conn):
    '''Takes in cursor and connection; Returns list of titles of tracks
    '''
    #List of tuples of songs
    title_tup = []
    cur.execute(f'SELECT song_name FROM Hot_100_Songs')
    for titles in cur.fetchall():
        title_tup.append(titles)
    
    #change tuple to list
    titles_list = [item for t in title_tup for item in t]
    #print(titles_list)
    return titles_list


def getTitleIDs(titles_list):
    '''Takes in cursor and connection and list of titles of tracks; Returns a list of IDS of each track
    '''
    #this is from an exmaple online (https://github.com/plamere/spotipy/blob/master/examples/search.py)
    title_ids = []
    for title in titles_list:
        if len(sys.argv) > 1:
            search_str = sys.argv[1]
        else:
            search_str = title
        info = sp.search(search_str, limit = 1) #the default already assings offset = 0 and type = 'track'
        t_id = info['tracks']['items']
        for x in t_id:
            #print(x)
            title_ids.append(x['id'])

    #print(info)
    #print(t_id)
    #print(title_ids)
    #pprint.pprint(t_id)
    return title_ids


def getTrackFeatures(title_ids):
    '''Takes in a list of track IDs;
    Returns a list of all these different features of each track in list
    '''
    #https://betterprogramming.pub/how-to-extract-any-artists-data-using-spotify-s-api-python-and-spotipy-4c079401bc37

    #list of lists
    tracks_features_list = []
    for item in title_ids:
        #print(item)
        info = sp.track(item)
        features = sp.audio_features(item)
        #info
        name = info['name']
        album = info['album']['name']
        artist = info['album']['artists'][0]['name']
        length = info['duration_ms']
        popularity = info['popularity']
    
         #features
        danceability = features[0]['danceability']
        energy = features[0]['energy']
        liveness = features[0]['liveness']
        loudness = features[0]['loudness']
        tempo = features[0]['tempo']

        track_features = [name, album, artist, length, popularity, danceability, energy, liveness, loudness, tempo]
        tracks_features_list.append(track_features)
    
    print(len(tracks_features_list))
    return tracks_features_list


def create_spotify_table(cur, conn, tracks_features_list):
    #create Spotify table with this list of lists (tracks_features_list)
    #can add all of those feautres if we want to
    cur.execute("CREATE TABLE IF NOT EXISTS Spotify (track_id INTEGER PRIMARY KEY, name TEXT, artist TEXT, length INTEGER, popularity INTEGER, energy REAL, loudness REAL)")
    #CHANGE track_id = 0 ... that's incorrect!!
    track_id = 0
    for track in tracks_features_list:
        track_id += 1 
        name = track[0]
        artist = track[2]
        length = track[3]
        popularity = track[4]
        energy = track[6]
        loudness = track[8]
        cur.execute("INSERT OR IGNORE INTO Spotify (track_id, name, artist, length, popularity, energy, loudness) VALUES (?, ?, ?, ?, ?, ?, ?)", (track_id, name, artist, length, popularity, energy, loudness))
    conn.commit()


#then after the table is created, I can use select statements to find the average anything

#For Visualizations: 
    #length vs popularity 
    #popularity vs weeks on chart (USE JOIN?)
    #energy vs popularity


def join_tables(cur, conn):
    #This function ???
    pass


def average_popularity(cur,conn):
    #takes in cursor and connection as inputs. 
    # Returns a number, which is the average popularity of songs on top 100 list
    popularities = []
    cur.execute("SELECT popularity FROM Spotify")
    data = cur.fetchall()
    
    total_pops = 0
    for i in data:
        pop = i[0]
        popularities.append(pop)
        total_pops += pop

    ave_pop = total_pops / len(popularities)
    ave_pop_message = f"The average popularity of songs in the 'Hot 100 songs' chart is {ave_pop}."
    
    return ave_pop_message


def average_length(cur,conn):
    #takes in cursor and connection as inputs. 
    # Returns a number, which is the average length of songs on top 100 list
    lengths = []
    cur.execute("SELECT length FROM Spotify")
    data = cur.fetchall()
    
    total_length = 0
    for i in data:
        length = i[0]
        lengths.append(length)
        total_length += length

    ave_length = total_length / len(lengths)
    ave_length_message = f"The average length of songs in the 'Hot 100 songs' chart is {ave_length}."
    
    return ave_length_message


def average_energy(cur, conn):
    #takes in cur, conn. Returns a number, which is the average energy of the top 100 songs
    energies = []
    cur.execute("SELECT energy FROM Spotify")
    data = cur.fetchall()
    
    total_energy = 0
    for i in data:
        energy = i[0]
        energies.append(length)
        total_energy += energy

    ave_energy = total_energy / len(energies)
    ave_energy_message = f"The average energy of songs in the 'Hot 100 songs' chart is {ave_energy}."
    
    return ave_length_message


def write_data_to_file(filename, cur, conn):
    #Takes in a filename (string) as an input and the database cursor/connection. 
    # Returns nothing. Creates a file and writes return value of the 
    # function average_popularity() and average_length to the file.
    pass


def main():
    #Takes in nothing and returns nothing. Calls the functions.
    cur, conn = setUpDatabase('top_100_songs.db')
    t_list = getTitleList(cur, conn)
    
    #t_list = ['Levitating', 'Leave The Door Open']
    #getTitleIDs(t_list)
    #getTrackFeatures(["463CkQjx2Zk1yXoBuierM9"])
                    
    x = getTrackFeatures(getTitleIDs(t_list))
    #getTrackFeatures(["1dI77VhaLcQSgQLSnIs03D"])
                        #^^ that is the correct ID to get!!! You need to figure out how to get that specific one
    
    create_spotify_table(cur, conn, x)


if __name__ == "__main__":
    main()