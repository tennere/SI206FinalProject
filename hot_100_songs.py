# SI 206 Final Project
# By Julia Kaplan (jhkaplan)

from bs4 import BeautifulSoup
import requests
import re
import os 
import csv
import sqlite3
import json 


def get_artist_information():
# Webscrapes data from the Billboard "Hot 100 Songs" table. Takes in nothing. Returns a list of tuples 
# containing the song name, artist name, peak on the Billboard chart, and the number of continuous week
# on the Billboard chart.  

    url = 'https://www.billboard.com/charts/hot-100'
    r = requests.get(url)
    # creates the beautiful soup object
    soup = BeautifulSoup(r.text, 'html.parser')

    # creates a list for each variable that is being scraped
    song_name_list = []
    song_artist_list = []
    peak_list = []
    weeks_on_chart_list = [] 

    # finds every song on the Billboard website and adds each song to a list
    song_find = soup.find_all("span", class_ = 'chart-element__information__song text--truncate color--primary')
    for song in song_find:
        song_text = song.get_text()
        song_name_list.append(song_text)

    # finds every artist on the Billboard website and adds each item to a list
    artist_find = soup.find_all("span", class_ = 'chart-element__information__artist text--truncate color--secondary')
    for artist in artist_find:
        artist_text = artist.get_text()
        song_artist_list.append(artist_text)
    
    # finds every peak length on the Billboard website and adds each item to a list
    peak_find = soup.find_all("span", class_ = 'chart-element__meta text--center color--secondary text--peak')
    for peak in peak_find:
        peak_text = int(peak.get_text())
        peak_list.append(peak_text)
    
    # finds every continuous weeks on chart number on the Billboard website and adds each item to a list
    weeks_find = soup.find_all("span", class_ = "chart-element__meta text--center color--secondary text--week")
    for week in weeks_find:
        weeks_text = int(week.get_text())
        weeks_on_chart_list.append(weeks_text)

    # creates a list that each tuple will be added to
    info_list = []

    # runs through each song and creates a tuple that includes song name, song artist, song peak, and continuous weeks
    # on the chart. Adds each tuple to a list. 
    for i in range(len(song_name_list)):
        tup = (song_name_list[i], song_artist_list[i], peak_list[i], weeks_on_chart_list[i])
        info_list.append(tup)
    
    #returns a list of song information tubles 
    return info_list 
    

def set_up_database(database_name):
# sets up database and where the database will be housed on the computer. 
# takes in the name of the database. returns cur and the connector.  
    
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+database_name)
    cur = conn.cursor()
    return cur, conn


def creating_top_100_songs_table(cur, conn):
# creates the table of the top 100 songs on the Billboard website. the table includes the 
# rank, song name, artist, peak on chart, and continuous weeks on chart for each song.
# puts 25 songs in the database at a time. after 100 songs, returns function renturns an error statement.
# takes in cur and conn, returns nothing. 
    
    cur.execute("CREATE TABLE IF NOT EXISTS Hot_100_Songs (rank INTEGER PRIMARY KEY, song_name TEXT, artist TEXT,  peak_on_chart INTEGER, weeks_on_chart INTEGER)")
    data = get_artist_information()
    cur.execute('SELECT * FROM Hot_100_Songs')
    # ranks from table are used as a counter 
    ranks = cur.fetchall()
    current = len(ranks) 
    
    # try statement runs if the first four times the function is ran
    try:
        # inserts 25 song data rows into the table 
        for i in range(0, 25):
            name = data[current + i][0]
            artist = data[current + i][1]
            peak_on_chart = data[current + i][2]
            weeks_on_chart = data[current + i][3]
            cur.execute("INSERT OR IGNORE INTO Hot_100_Songs (rank, song_name, artist, peak_on_chart, weeks_on_chart) VALUES (?, ?, ?, ?, ?)", (current + i + 1, name, artist, peak_on_chart, weeks_on_chart))
        conn.commit()
    # after running the function four times, an error statement will print
    
    except:
        print("ERROR: Ran too many times!")


def find_average_weeks_on_chart(cur, conn):
# finds the average number of continous weeks each song has spent on the Billboard chart.
# takes in cur and conn, returns the average weeks within a string statement
    
    weeks_on_chart_list = []
    
    # selects all of the continous weeks data for each song and returns in a tuple 
    cur.execute("SELECT weeks_on_chart FROM Hot_100_Songs")
    weeks_on_chart_data = cur.fetchall()
    
    # looks at each indivdual song tuple and appends the weeks to the list 
    for week_tuple in weeks_on_chart_data:
        week = week_tuple[0]
        weeks_on_chart_list.append(week)
    
    # finds the total number of weeks all of the songs have spent on the chart in total 
    total = 0
    for week in weeks_on_chart_list:
        total += week
    
    # calculates the average weeks
    average_weeks = total / len(weeks_on_chart_list)
    
    # creates a message including the average weeks calculation
    average_weeks_message = f"The average time each song has spent on the 'Hot 100 Songs' chart is {average_weeks} weeks. "
    
    return average_weeks_message


def find_max_weeks_on_chart(cur, conn):
# finds the maximum weeks a song has spent on the Billboard chart.
# takes in cur and conn, returns the max weeks within a string statement 
    
    weeks_on_chart_list = []

    # selects all of the continous weeks data for each song and returns in a tuple 
    cur.execute("SELECT weeks_on_chart FROM Hot_100_Songs")
    weeks_on_chart_data = cur.fetchall()
    
    # looks at each indivdual song tuple and appends the weeks to the list
    for week_tuple in weeks_on_chart_data:
        week = week_tuple[0]
        weeks_on_chart_list.append(week)
    
    # finds the max weeks
    max_weeks = max(weeks_on_chart_list)

    # converts max weeks to max years
    max_years = round(max_weeks / 52, 2)

    # creates a message including the max weeks and years calculation
    max_time_message = f"The maximum time song has spent on the 'Hot 100 Songs' chart is {max_weeks} weeks, which is equal to approximately {max_years} years."

    return max_time_message


def data_collection_finished(cur, conn):
# function checks if all 100 song entries have been entered into the chart.
# takes in cur and conn. returns true if all 100 songs have been entered. returns false if else. 
    
    cur.execute('SELECT song_name FROM Hot_100_Songs')
    artists = cur.fetchall()

    # if all 100 songs have been entered into the chart
    if len(artists) == 100:
        return True
    else:
        return False


def create_txt_file(filename, cur, conn):
# creates a txt file containing the statistics calculations. 
# takes in the filename of the .txt file, cur and conn. returns nothing. 

    # creates path to locate the file 
    path = os.path.dirname(os.path.abspath(__file__)) + os.sep
    f = open(path + filename, "w")

    # both functions return a message about the statistics calculation
    avg_weeks_on_chart = find_average_weeks_on_chart(cur, conn)
    max_weeks_on_chart = find_max_weeks_on_chart(cur, conn)

    f.write("Statistics from the 'Billboard Hot 100 Songs' Table: \n\n")
    f.write("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n\n")
    
    # writes the average weeks message
    f.write(avg_weeks_on_chart + "\n\n")

    # writes the max weeks message 
    f.write(max_weeks_on_chart + "\n\n")

    f.close()


def main():
# takes in nothing. returns nothing. creates cur and conn with set_up_database().
# runs creating_top_100_songs_table(), data_collection_finished(), and 
# runs create_txt_file() if data collection is finished. 
   
    # creates the database
    cur, conn = set_up_database("top_100_songs.db")
    
    # fills the data base, 25 songs at a time 
    creating_top_100_songs_table(cur, conn)
    
    # determines if 100 songs data sets have been entered into the table
    collection_finished = data_collection_finished(cur, conn)
    
    # if all the song data has been entered, create the statistics text file
    if collection_finished:
        create_txt_file('top_100_songs_statistics.txt', cur, conn)
    
    
    conn.close()
    

if __name__ == "__main__":
    main()

