#SI206 Final Project
#By Yonit Robin

import requests
import re
import os 
import csv
import sqlite3
import json 

#base url 
base = 'https://api.deezer.com/'

def setUpDatabase(db_name):
# sets up the database. takes in the database name, returns 
# cursor and connection.
    
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect('top_100_songs.db')
    cur = conn.cursor()
    return cur, conn


def getInfo(cur, conn):
# Selects the song name and artist from the Hot 100 Songs table and
# uses this information to get data for each song from the Deezer API.
# Takes in cursor and connection. Returns tuple with all of Deezer data.
    
    #select song names and artists from Hot 100 songs table and create a tuple called SongArt
    cur.execute(f'SELECT song_name, artist FROM Hot_100_Songs')
    songArt = cur.fetchall()

    #name empty lists 
    artists = []
    artists_no_featuring = []
    songs = []
    songs_no_spaces = []

    #make a list of all artist names
    for i in songArt:
        artists.append(i[1])
    
    #make a list of just the first artist for each song so thatt deezer can fetch the data. Takes away words like 'featuring' or 'duet'
    #replaces spaces with hyphens so that terms can be searched
    for i in artists:
        if 'Featuring' in i or 'Duet' in i or '&' in i:
            no_featuring = i.split('Featuring')[0]
            artists_no_featuring.append(no_featuring.replace(' ','-'))
        else:
            artists_no_featuring.append(i.replace(' ','-'))

    #make list of song names
    for i in songArt:
        songs.append(i[0])
    
    #make list of song names with hyphens instead of spaces
    for i in songs:
        songs_no_spaces.append(i.replace(' ','-'))
    
    #make list of deezer ranks for each song
    deezer_ranks = []
    for song in songs_no_spaces:
        #call the api on each song
        song_url = base + 'search/track?q={}'.format(song)
        song_data = getReq(song_url)

        #if there is no data, say N/A
        if len(song_data["data"]) == 0 or song_data == None:
            ranks = 'N/A'

        #when there is data, fetch the rank of each song and add it to the list
        ranks = song_data['data'][0]['rank']
        deezer_ranks.append(ranks)
    
    #make list of fan numbers for each artist
    fan_numbers = []
    for person in artists_no_featuring:
        #call the api on each artist
        fan_url = base + 'search/artist?q={}'.format(person)
        fan_data = getReq(fan_url)

        #if there is no data, say N/A
        if len(fan_data["data"]) == 0 or fan_data == None:
            fans = 'N/A'

        #when there is data, fetch the number of fans for each artist and add it to the list
        else:
            fans = fan_data['data'][0]['nb_fan']
        fan_numbers.append(fans)
    
    #puts all data into a tuple 
    DeezData = [(songs[i], artists[i], deezer_ranks[i], fan_numbers[i]) for i in range(0, len(songs))]
    
    return DeezData
        
def makeDeezerTable(cur):
# Creates a table to hold all of the Deezer data. Takes in cur. Returns nothing. 

    cur.execute(f'CREATE TABLE IF NOT EXISTS Deezer (track_id INTEGER PRIMARY KEY, song_name TEXT, artist_name TEXT, songs_deezer_rank INTEGER, artist_fan_number INTEGER)')

def getReq(base):
# Takes in the API request. Returns the data in dictionary format
# if the status code is 200. Returns nothing if else.  
    
    #request works if status code is 200
    r = requests.get(base)
    if r.status_code == 200:
        return json.loads(r.content)
    else:
        return None


def fillTable(cur, conn):
# Takes in cur and connection. Fills up the Deezer table 
# with the fetched information. Prints a "done" statement when collection is finished. 
    

    #call the getInfo function
    data = getInfo(cur, conn)

    #initialize track_id and increment value for each song
    track_id = 0

    #loop thru data and assign each value to a column in the table
    for song in data:
        track_id += 1
        song_name = song[0]
        artist_name = song[1]
        songs_deezer_rank = song[2]
        artist_fan_number = song[3]
        cur.execute('INSERT OR IGNORE INTO Deezer (track_id, song_name, artist_name, songs_deezer_rank, artist_fan_number) VALUES (?,?,?,?,?)', (track_id, song_name, artist_name, songs_deezer_rank, artist_fan_number))
    conn.commit()

    #code takes a very long time to run, so this prints "done filling table" when the code is done
    print('done filling table')

def avgFans(cur,conn):
# Takes in cursor and connection. Calculates the average Deezer fan number for
# artists of Billboard's top 100 songs. Returns the calculation in a string statement. 
    
    #select fan numbers from deezer table
    cur.execute("SELECT artist_fan_number FROM Deezer")
    data = cur.fetchall()

    #make a list of all fan numbers
    fans_list =  [i for t in data for i in t]

    #set all 'N/A's to 0 so that it does not effect the average
    new_lst = [0 if i =='N/A' else i for i in fans_list]

    #turn all fan numbers from strings to integers
    fan_ints = [int(item) for item in new_lst]

    #calculate the average
    all_fans = 0
    for i in fan_ints:
        all_fans += i
    avgFans = all_fans/len(fan_ints)

    fanStatement = f"The average fan number for the artists in the 'Hot 100 Songs' chart is {avgFans}"
    return fanStatement
       
def avgRank(cur, conn):
# Takes in cursor and connection. Calculates the average Deezer fan number for Billboard's 
# top 100 songs. Returns the statistic in a string statement. 

    #select song rank from deezer table
    cur.execute("SELECT songs_deezer_rank FROM Deezer")
    data = cur.fetchall()

    #make a list of all ranks
    rank_list =  [i for t in data for i in t]

    #set all 'N/A's to 0 so that it does not effect the average
    new_lst = [0 if i =='N/A' else i for i in rank_list]

    #turn all fan numbers from strings to integers
    rank_ints = [int(item) for item in new_lst]

    #calculate the average
    all_ranks = 0
    for i in rank_ints:
        all_ranks += i
    avgRanks = all_ranks/len(rank_ints)

    rankStatement = f"The average deezer rank for the songs in the 'Hot 100 Songs' chart is {avgRanks}"
    return rankStatement

def writeToFile(filename, cur, conn):
# Takes in the filename, cursor and connection. Creates a file and writes the statements 
# from avgRank() and avgFans() into a .txt file. Returns nothing.
    
    path = os.path.dirname(os.path.abspath(__file__)) + os.sep
    
    #open file for writing
    f = open(path + filename, "w")

    #call on the avgRank() and avgFans() functions
    avg_deezer_rank = avgRank(cur, conn)
    avg_fan_number = avgFans(cur, conn)

    #format the txt file
    f.write("Statistics from the 'Deezer' Table: \n\n")
    f.write("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n\n")
    f.write(avg_deezer_rank + "\n\n")
    f.write(avg_fan_number + "\n\n")

    #close the file
    f.close()
    
def main():
    cur, conn = setUpDatabase('top_100_songs.db')
    getInfo(cur, conn)
    makeDeezerTable(cur)
    getReq(base)
    fillTable(cur, conn)
    avgFans(cur,conn)
    avgRank(cur, conn)
    writeToFile('deezer_calculations.txt', cur, conn)

if __name__ == "__main__":
    main()

