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



# def setUpDatabase(db_name):
#     path = os.path.dirname(os.path.abspath(__file__))
#     conn = sqlite3.connect('top_100_artists.db')
#     cur = conn.cursor()
#     return cur, conn


# def getTitleList(cur, conn):
#     '''Takes in cursor and connection; Returns list of titles of tracks
#     '''
#     #List of tuples of artists, but we want ot change this to songs hopefully
#     title_tup = []
#     cur.execute(f'SELECT name FROM Hot_100_Artists')
#     for titles in cur.fetchall():
#         title_tup.append(titles)
    
#     #change tuple to list
#     titles_list = [item for t in title_tup for item in t]
#     #print(titles_list)
#     return titles_list




def getTitleIDs(titles_list):
    '''Takes in cursor and connection and list of titles of tracks; Returns IDS of each track
    '''
    
    #this is from an exmaple online (https://github.com/plamere/spotipy/blob/master/examples/search.py)
    title_ids = []
    for title in titles_list:
        if len(sys.argv) > 1:
            search_str = sys.argv[1]
        else:
            search_str = title
        info = sp.search(search_str)
        t_id = info['tracks']
        t_id = t_id['items'][0]#['album']['artists'][0]['id']
        title_ids.append(t_id)
        #use Beauitufl Soup to access the actual id?
        #track_id = info[]
        #title_ids.append(track_id)
    pprint.pprint(t_id)
   #print(title_ids)
    #print(title_ids)
    return title_ids


def getTrackFeatures(title_ids):
    '''Takes in a list of track IDs;
    Returns a list of all these different features of each track in list
    '''
    #https://betterprogramming.pub/how-to-extract-any-artists-data-using-spotify-s-api-python-and-spotipy-4c079401bc37

    #list of lists
    tracks_features_list = []
    for item in title_ids:
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
    
    #print(tracks_features_list)
  # return tracks_features_list


def create_spotify_table(cur, conn, tracks_features_list):
    #create Spotify table with this list of lists (tracks_features_list)
    #can add all of those feautres if we want to
    cur.execute("CREATE TABLE IF NOT EXISTS Spotify (track_id INTEGER PRIMARY KEY, name TEXT, artist INTEGER, length INTEGER, popularity INTEGER, energy INTEGER, loudness INTEGER)")
    track_id = 0
    for track in tracks_features_list:
        track_id += 1 
        name = track[0]
        artist = track[1]
        length = track[2]
        popularity = track[3]
        energy = track[4]
        loudness = track[5]
        cur.execute("INSERT OR IGNORE INTO Spotify (track_id, name, artist, length, popularity, energy, loudness) VALUES (?, ?, ?, ?, ?, ?, ?)", (track_id, name, artist, length, popularity, energy, loudness))
    conn.commit()


#then after the table is created, I can use select statements to find the average anything







def join_tables(cur, conn):
    #This function ???
    pass

def get_artists_list():
    #This function returns an artist list???
    pass

#def create_spotify_table(cur, conn):
    #Takes in the database cursor and connection as inputs and returns nothing. 
    # Creates a table called Spotify_Table and finds the Spotify popularity 
    # of each artist (is that possible? it's possible for each song) and inserts it into the table
    #pass

def average_weeks(cur,conn):
    #This function will take the database cursor and connection as inputs. 
    # Returns an integer, which is the average number of weeks on the Top 100 list 
    # of current Billboard Top 100 Artists on Spotify.
    pass

def write_data_to_file(filename, cur, conn):
    #Takes in a filename (string) as an input and the database cursor/connection. 
    # Returns nothing. Creates a file and writes return value of the 
    # function average_weeks() to the file.
    pass


def main():
    #Takes in nothing and returns nothing. Calls the functions.
    
    #cur, conn = setUpDatabase('top_100_artists.db')
    t_list = ['Levitating']
    getTitleIDs(t_list)
    #getTrackFeatures(["1dI77VhaLcQSgQLSnIs03D"])
                        #^^ that is the correct ID to get!!! You need to figure out how to get that specific one
if __name__ == "__main__":
    main()