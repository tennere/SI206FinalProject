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
            artist_name_list.append(name)
        
            rank = artist.get('data-rank')
            artist_rank_list.append(rank)

            find_weeks = artist.find('div', class_ = "chart-list-item__weeks-on-chart")
            weeks_on_chart = find_weeks.get_text()
            weeks_on_chart_list.append(weeks_on_chart)

            find_peak = artist.find('div', class_ = "chart-list-item__weeks-at-one")
            peak = find_peak.get_text()
            peak_list.append(peak)

    info_list = []

    for i in range(len(artist_name_list)):
        tup = (artist_name_list[i], artist_rank_list[i], weeks_on_chart_list[i], peak_list[i])
        info_list.append(tup)
    
    return info_list
    

   

    

def set_up_database(database_name):
    # yeah
    table = 'table'

def set_up_categories_table(data, cur, conn):
    table = 'table'

def set_up_artist_table(data, cur, conn):
    table = 'table'




def main():
    info_list = get_artist_information()
    print(info_list)

if __name__ == "__main__":
    main()

