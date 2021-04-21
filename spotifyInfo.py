#Name: Emma Tenner (tennere)
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
   #Takes in the database name; Returns cursor and connector

   path = os.path.dirname(os.path.abspath(__file__))
   conn = sqlite3.connect('top_100_songs.db')
   cur = conn.cursor()
   return cur, conn
 
 
def getTitleList(cur, conn):
   #Takes in cursor and connector; Returns list of titles of songs from Hot_100_Songs table
   
   #Creates empty list to hold song titles 
   title_tup = []

   #selects song_name from table
   cur.execute(f'SELECT song_name FROM Hot_100_Songs')

   #goes through each row of table and appends song name to list
   for titles in cur.fetchall():
       title_tup.append(titles)

   #change tuple to list
   titles_list = [item for t in title_tup for item in t]

   #returns list of song titles
   return titles_list
 
 
def getTitleIDs(titles_list):
   #Takes in a list of song titles; Returns a list of Spotify IDs of each song
   
   #create empty list that will hold all of the IDs
   title_ids = []

   #goes through the passed in list and uses the Spotipy search() function to select the correct ID for each song
   for title in titles_list:
       if len(sys.argv) > 1:
           search_str = sys.argv[1]
       else:
           search_str = title
       info = sp.search(search_str, limit = 1)
       t_id = info['tracks']['items']
       #appends the id to the title_ids list
       for x in t_id:
           title_ids.append(x['id'])
 
   #returns list of spotify IDs
   return title_ids
 
 
def getTrackFeatures(title_ids):
   #Takes in a list of song's IDs; Returns a list of lists of features for each song
 
   #creates empty list that will store the features of every song
   tracks_features_list = []

   #goes through the passed in list and uses the Spotipy track() and audio_features() functions to retreive the intended features
   for item in title_ids:
      #retreives all of the data
       info = sp.track(item)
       features = sp.audio_features(item)

      #goes through the 'info' data to select the correct features
       name = info['name']
       album = info['album']['name']
       artist = info['album']['artists'][0]['name']
       length = info['duration_ms']
       popularity = info['popularity']
  
      #goes through the 'features' data to select the correct features
       danceability = features[0]['danceability']
       energy = features[0]['energy']
       liveness = features[0]['liveness']
       loudness = features[0]['loudness']
       tempo = features[0]['tempo']

      #creates a list of a single songs' features
       track_features = [name, album, artist, length, popularity, danceability, energy, liveness, loudness, tempo]
      #appends that list to the original list
       tracks_features_list.append(track_features)
  
   #returns a list of lists of every songs features
   return tracks_features_list
 
 
def create_spotify_table(cur, conn, tracks_features_list):
   #Takes in cursor, connection, and list of lists of songs' features; Creates a Spotify table; Returns nothing
   #The table includes the track_id, the song's name, the artist, the length (MS), the Spotify popularity, the energy, and the loudness
 
   
   cur.execute("CREATE TABLE IF NOT EXISTS Spotify (track_id INTEGER PRIMARY KEY, name TEXT, artist TEXT, length INTEGER, popularity INTEGER, energy REAL, loudness REAL)")
   track_id = 0
   for track in tracks_features_list:
      #goes through the passed in list and retreives the specific features we want to add to the table for each song
       track_id += 1
       name = track[0]
       artist = track[2]
       length = track[3]
       popularity = track[4]
       energy = track[6]
       loudness = track[8]
       cur.execute("INSERT OR IGNORE INTO Spotify (track_id, name, artist, length, popularity, energy, loudness) VALUES (?, ?, ?, ?, ?, ?, ?)", (track_id, name, artist, length, popularity, energy, loudness))
   conn.commit()
 
 #THIS WAS TRYING TO DO THE LIMIT 25, BUT DON'T NEED IT ANYMORE?:
 
   # cur.execute("CREATE TABLE IF NOT EXISTS Spotify (track_id INTEGER PRIMARY KEY, name TEXT, artist TEXT, length INTEGER, popularity INTEGER, energy REAL, loudness REAL)")
   # #!!CHANGE track_id = 0 ... that's incorrect!!
   # track_id = 0
  
   # #to limit 25: grab length of table (how many rows we have so far ... starting at 0), then loop thru a range of 25 but start getting values at length spot ...
   # cur.execute('SELECT * FROM Spotify')
   # #this gets length of list
   # length = len(cur.fetchall())
   # #then start at row = length
   # for num in range(25):
   #     length = num
   #     track = tracks_features_list[length] 
   #     track_id += 1
   #     name = track[0]
   #     artist = track[2]
   #     length = track[3]
   #     popularity = track[4]
   #     energy = track[6]
   #     loudness = track[8]
   #     cur.execute("INSERT OR IGNORE INTO Spotify (track_id, name, artist, length, popularity, energy, loudness) VALUES (?, ?, ?, ?, ?, ?, ?)", (track_id, name, artist, length, popularity, energy, loudness))
   #     length += 1
   # conn.commit()

 
def average_popularity(cur,conn):
   #Takes in cursor and connection; Returns a message that has the average Spotify popularity of the songs from the Hot_100_Songs Chart
   
   #selects the popularity value from the Spotify table
   cur.execute("SELECT popularity FROM Spotify")
   data = cur.fetchall()

   #list to keep track of all of the popularities
   popularities = []
   
   #variable to keep track of total popularity
   total_pops = 0

   for i in data:
      #goes through each row and appends the popularity to the the list and adds to the total popularity
       pop = i[0]
       popularities.append(pop)
       total_pops += pop
   
   #calculates average
   ave_pop = total_pops / len(popularities)
   ave_pop = round(ave_pop, 2)
   ave_pop_message = f"The average popularity of songs in the 'Hot 100 songs' chart is {ave_pop}."
  
   #returns the message
   return ave_pop_message
 
 
def average_length(cur,conn):
   #Takes in cursor and connection; Returns a message that has the average length of the songs from the Hot_100_Songs Chart in ms

   #creates list to store all of the lengths
   lengths = []

   #selects the length value from the Spotify table
   cur.execute("SELECT length FROM Spotify")
   data = cur.fetchall()
   
   #creates variable to keep track of total length
   total_length = 0

   for i in data:
      #goes through each row and appends the length to the the list and adds to the total length
       length = i[0]
       lengths.append(length)
       total_length += length
   
   #calculates average
   ave_length = total_length / len(lengths)
   ave_length = round(ave_length, 2)
   ave_length_message = f"The average length of songs in the 'Hot 100 songs' chart is {ave_length} (ms)."
  
   #returns the message
   return ave_length_message
 
 
def average_energy(cur, conn):
   #Takes in cursor and connection; Returns a message that has the average energy of the songs from the Hot_100_Songs Chart
   
   #creates a list to hold the energy values
   energies = []

   #selects the energy values from the Spotify table
   cur.execute("SELECT energy FROM Spotify")
   data = cur.fetchall()
  
   #creates variable to keep track of total energy
   total_energy = 0

   for i in data:
      #goes through each row and appends the energy to the list and adds it to the total energy
       energy = i[0]
       energies.append(energy)
       total_energy += energy
   
   #calculates average
   ave_energy = total_energy / len(energies)
   ave_energy = round(ave_energy,2)
   ave_energy_message = f"The average energy of songs in the 'Hot 100 songs' chart is {ave_energy}."
  
   #returns the message
   return ave_energy_message
 
 
def max_popularity(cur, conn):
   #Takes in cursor and connection; Returns a message that has the maximum popularity out of all the songs from the Hot_100_Songs Chart
   
   #selects the popularity for each song
   cur.execute("SELECT popularity FROM Spotify")
   data = cur.fetchall()
   
   #sets the max_pop to the first popularity as a starting point
   max_pop = data[0][0]

   for i in range(len(data)):
      #goes through each popularity to check if any of them are higher than the first max_pop; If so, then that is the new max_pop
      if data[i][0] > max_pop:
         max_pop = data[i][0]
      else:
         max_pop = max_pop
  
   max_pop_message = f"The highest Spotify popularity of the top songs in the 'Hot 100 songs' chart is {max_pop}."
   
   #returns the message
   return max_pop_message
 
 
def write_data_to_file(filename, cur, conn):
   #Takes in a filename, cursor, and connection; Returns nothing; Creates a file and writes the return values of the functions average_popularity(), average_length(), average_energy(), and max_popularity() to the file.

   #Call each function and assign the return values to variables
   avg_pop = average_popularity(cur, conn)
   avg_len = average_length(cur, conn)
   avg_en = average_energy(cur, conn)
   max_pop = max_popularity(cur, conn)

   #creates file to write to
   with open('spotifyStatistics.txt', 'w') as f:
      #inputs all the messages from the various functions
      f.write("Statistics from the 'Spotify' Table: \n\n")
      f.write("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n\n")
      f.write(avg_pop + "\n\n")
      f.write(avg_len + "\n\n")
      f.write(avg_en + "\n\n")
      f.write(max_pop + "\n\n")
 
 
def main():
   #Takes in nothing; Returns nothing; Calls the functions

   #creates the database cursor and connection
   cur, conn = setUpDatabase('top_100_songs.db')

   #gets the list of titles
   t_list = getTitleList(cur, conn)       

   #gets the list of lists of track features
   x = getTrackFeatures(getTitleIDs(t_list))
  
   #creates the spotify table
   create_spotify_table(cur, conn, x)
   
   #creates and writes to the new .txt file
   write_data_to_file('spotifyStatistics.txt', cur, conn)


if __name__ == "__main__":
   main()

