from bs4 import BeautifulSoup
import requests
import re
import os 
import csv
import sqlite3
import json 


def get_artist_information():
    url = 'https://www.billboard.com/charts/artist-100'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    artist_name_list = []
    artist_rank_list = []
    weeks_on_chart_list = []
    peak_list = [] 

    chart = soup.find("div", class_ = "chart-details")
    chart2 = chart.find_all("div", class_ = "chart-list chart-details__left-rail")
    for table in chart2:
        artists = table.find_all("div", class_ = "chart-list-item")
        for artist in artists:
            find_name = artist.find("span", class_ = "chart-list-item__title-text")
            name = find_name.get_text('href')
            name = name.replace('\nhref\n', '')
            name = name.replace('\n', '')
            name = name.strip()
            artist_name_list.append(name)
        
            rank = int(artist.get('data-rank'))
            artist_rank_list.append(rank)

            find_weeks = artist.find('div', class_ = "chart-list-item__weeks-on-chart")
            weeks_on_chart = int(find_weeks.get_text())
            weeks_on_chart_list.append(weeks_on_chart)

            find_peak = artist.find('div', class_ = "chart-list-item__weeks-at-one")
            peak = int(find_peak.get_text())
            peak_list.append(peak)

    info_list = []

    for i in range(len(artist_name_list)):
        tup = (artist_name_list[i], artist_rank_list[i], weeks_on_chart_list[i], peak_list[i])
        info_list.append(tup)
    

    return info_list
    

def set_up_database(database_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+database_name)
    cur = conn.cursor()
    return cur, conn


def creating_top_100_artists_table(cur, conn):
    # CAN ONLY UPLOAD 25 AT A TIME
    cur.execute("CREATE TABLE IF NOT EXISTS Hot_100_Artists (artist_id INTEGER PRIMARY KEY, name TEXT, rank INTEGER, weeks_on_chart INTEGER, peak_on_chart INTEGER)")
    data = get_artist_information()
    artist_id = 0
    for artist in data:
        artist_id += 1 
        name = artist[0]
        rank = artist[1]
        weeks_on_chart = artist[2]
        peak_on_chart = artist[3]
        cur.execute("INSERT OR IGNORE INTO Hot_100_Artists (artist_id, name, rank, weeks_on_chart, peak_on_chart) VALUES (?, ?, ?, ?, ?)", (artist_id, name, rank, weeks_on_chart, peak_on_chart))
    conn.commit()



def main():
    cur, conn = set_up_database("top_100_artists.db")
    creating_top_100_artists_table(cur, conn)

if __name__ == "__main__":
    main()

