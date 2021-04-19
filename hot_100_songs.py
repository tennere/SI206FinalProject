from bs4 import BeautifulSoup
import requests
import re
import os 
import csv
import sqlite3
import json 


def get_artist_information():
    url = 'https://www.billboard.com/charts/hot-100'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    song_name_list = []
    song_artist_list = []
    peak_list = []
    weeks_on_chart_list = [] 

    song_find = soup.find_all("span", class_ = 'chart-element__information__song text--truncate color--primary')
    for song in song_find:
        song_text = song.get_text()
        #print(song_text)
        song_name_list.append(song_text)

    artist_find = soup.find_all("span", class_ = 'chart-element__information__artist text--truncate color--secondary')
    for artist in artist_find:
        artist_text = artist.get_text()
        #print(artist_text)
        song_artist_list.append(artist_text)
    
    peak_find = soup.find_all("span", class_ = 'chart-element__meta text--center color--secondary text--peak')
    for peak in peak_find:
        peak_text = int(peak.get_text())
        #print(peak_text)
        peak_list.append(peak_text)
    
    weeks_find = soup.find_all("span", class_ = "chart-element__meta text--center color--secondary text--week")
    for week in weeks_find:
        weeks_text = int(week.get_text())
        #print(weeks_text)
        weeks_on_chart_list.append(weeks_text)

    
    info_list = []

    for i in range(len(song_name_list)):
        tup = (song_name_list[i], song_artist_list[i], peak_list[i], weeks_on_chart_list[i])
        info_list.append(tup)
    
    return info_list 
    

def set_up_database(database_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+database_name)
    cur = conn.cursor()
    return cur, conn


def creating_top_100_artists_table(cur, conn):
    # CAN ONLY UPLOAD 25 AT A TIME
    cur.execute("CREATE TABLE IF NOT EXISTS Hot_100_Songs (rank INTEGER PRIMARY KEY, song_name TEXT, artist TEXT,  peak_on_chart INTEGER, weeks_on_chart INTEGER)")
    data = get_artist_information()
    rank = 0
    for song in data:
        rank += 1 
        name = song[0]
        artist = song[1]
        peak_on_chart = song[2]
        weeks_on_chart = song[3]
        cur.execute("INSERT OR IGNORE INTO Hot_100_Songs (rank, song_name, artist, peak_on_chart, weeks_on_chart) VALUES (?, ?, ?, ?, ?)", (rank, name, artist, peak_on_chart, weeks_on_chart))
    conn.commit()

'''
def find_average_weeks_on_chart(cur, conn):
    weeks_on_chart_list = []

    cur.execute("SELECT weeks_on_chart FROM Hot_100_Artists")
    weeks_on_chart_data = cur.fetchall()
    
    for week_tuple in weeks_on_chart_data:
        week = week_tuple[0]
        weeks_on_chart_list.append(week)
    
    total = 0
    for week in weeks_on_chart_list:
        total += week
    
    average_weeks = total / len(weeks_on_chart_list)
    
    average_weeks_message = f"The average time each artist has spent on the 'Hot 100 Artists' chart is {average_weeks} weeks. "
    
    return average_weeks_message

def find_max_weeks_on_chart(cur, conn):
    weeks_on_chart_list = []

    cur.execute("SELECT weeks_on_chart FROM Hot_100_Artists")
    weeks_on_chart_data = cur.fetchall()
    
    for week_tuple in weeks_on_chart_data:
        week = week_tuple[0]
        weeks_on_chart_list.append(week)
    
    max_weeks = max(weeks_on_chart_list)

    max_years = round(max_weeks / 52, 2)

    max_time_message = f"The maximum time an artist has spent on the 'Hot 100 Artists' chart is {max_weeks} weeks, which is equal to approximately {max_years} years."

    return max_time_message


def data_collection_finished(cur, conn):
    cur.execute('SELECT name FROM Hot_100_Artists')
    artists = cur.fetchall()

    if len(artists) == 100:
        return True
    else:
        return False


def create_txt_file(filename, cur, conn):
    path = os.path.dirname(os.path.abspath(__file__)) + os.sep
    f = open(path + filename, "w")

    avg_weeks_on_chart = find_average_weeks_on_chart(cur, conn)
    max_weeks_on_chart = find_max_weeks_on_chart(cur, conn)

    f.write("Statistics from the 'Billboard Hot 100 Artists' Table: \n\n")
    f.write("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n\n")
    
    f.write(avg_weeks_on_chart + "\n\n")

    f.write(max_weeks_on_chart + "\n\n")

    f.close()

'''
def main():
    
    cur, conn = set_up_database("top_100_songs.db")
    creating_top_100_artists_table(cur, conn)
    '''
    find_average_weeks_on_chart(cur, conn)
    find_max_weeks_on_chart(cur, conn)

    collection_finished = data_collection_finished(cur, conn)
    
    if collection_finished:
        create_txt_file('top_100_artists_statistics.txt', cur, conn)
    
    '''
    conn.close()
    

    get_artist_information()
if __name__ == "__main__":
    main()

