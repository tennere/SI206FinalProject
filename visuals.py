import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import sqlite3
import json



def visual1(cur):
# Collects data from database. Creates empty lists and stores track id, song name, 
# deezer rank, artist fan number, and artist name in seperate lists. Creates a scatterplot 
# of Deezer rank vs Billboard rank. Displays scatterplot. Takes in cur, returns nothing.    
    
    cur.execute('SELECT track_id, song_name, songs_deezer_rank, artist_fan_number, artist_name FROM Deezer')
    results = cur.fetchall()

    #creates empty lists to store the information
    songs_list = []
    song_names = []
    ranks_list = []
    fan_number_list = []
    artist_names = []

    for r in results: 
        songs_list.append(r[0])
        song_names.append(r[1])
        ranks_list.append(r[2])
        fan_number_list.append(r[3])
        artist_names.append(r[4])
    
    #figure 1: scatter plot of deezer rank vs billboard rank
    figure1 = go.Figure()
    figure1.add_trace(go.Scatter(
        x = ranks_list,
        y = songs_list,
        marker = dict(color = 'red', size = 10),
        mode = 'markers',
        name = 'Deezer Song Rank vs Rank in Billboard 100 Chart',
    ))
    figure1.update_layout(title = 'Deezer Song Rank vs Rank in Billboard 100 Chart', xaxis_title = 'Deezer Rank',
        yaxis_title = 'Billboard Rank', xaxis = dict(range = [20000,1000000]), yaxis = dict(autorange = 'reversed'))
    figure1.show()


def visual2(cur):
# Collects data from database. Creates empty lists and stores fan number aand artist names
# in seperate lists. Creates a bar chart displaying the Deezer fan number for each of the artists 
# from the top 30 Billboard songs. Displays bar chart. Takes in cur, returns nothing.   
 
    cur.execute('SELECT artist_fan_number, artist_name FROM Deezer')
    results = cur.fetchall()

    #creates empty lists to store the information
    fan_number_list = []
    artist_names = []

    for r in results: 
        fan_number_list.append(r[0])
        artist_names.append(r[1])
    figure2 = px.bar(
        x = artist_names[0:30],
        y = fan_number_list[0:30]
        )
    figure2.update_layout(title = 'Fan numbers for the artists of Billboard top 30 songs', xaxis_title = 'artist name', yaxis_title = 'artist fan number')
    figure2.show()    


def visual3(cur):
# Collects data from database using a JOIN statement. Creates empty lists and stores Spotify popularity 
# and Billboard weeks on chart in seperate lists. Creates a scatterplot of Spotify Popularity of Top 100 Songs 
# vs. # Weeks on Billboard 100 Chart. Displays scatterplot. Takes in cur, returns nothing.    

    #using JOIN selects spotify popularity and # weeks on chart
    cur.execute('SELECT Hot_100_Songs.weeks_on_chart, Spotify.popularity FROM Hot_100_Songs JOIN Spotify ON Hot_100_Songs.rank = Spotify.track_id')
    results = cur.fetchall()

    #creates empty lists
    popularity_list = []
    weeks_on_chart_list = []

    for r in results: 
        #appends the first element of each result to the weeks_on_chart list & appends the second element of each result to the popularity_list
        popularity_list.append(r[1])
        weeks_on_chart_list.append(r[0])
    
    #creates a scatter plot of each songs Spotify popularity vs weeks on Hot 100 chart to see if correlation
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x = popularity_list,
        y = weeks_on_chart_list,
        marker = dict(color = 'green', size = 10),
        mode = 'markers',
        name = 'Spotify Popularity vs # Weeks on Billboard Hot 100 Chart',
    ))
    fig3.update_layout(title = "Spotify Popularity of Top 100 Songs vs. # Weeks on Billboard 100 Chart",
                        xaxis_title="Spotify Popularity", yaxis_title="# Weeks on Chart", xaxis=dict(range=[0, 100]))
    fig3.show()


def visual4(cur):
# Collects data from database using a JOIN statement. Creates empty lists and stores 
# Billboard rank and Spotify energy levels in seperate lists. Creates a scatterplot of 
# Hot 100 Songs rank vs Spotify energy levels. Displays scatterplot. Takes in cur, returns nothing. 

    #using JOIN selects Hot 100 rank and Spotify energy
    cur.execute('SELECT Hot_100_Songs.rank, Spotify.energy FROM Hot_100_Songs JOIN Spotify ON Hot_100_Songs.rank = Spotify.track_id')
    data = cur.fetchall()

    # creates empty lists
    rank_list = []
    energy_list = []

    # puts data into each list
    for element in data:
        rank_list.append(element[0])
        energy_list.append(element[1])

    fig4 = go.Figure()
    
    # creates scatter plot of Hot 100 rank and Spotify energy
    fig4.add_trace(go.Scatter(
        x = rank_list,
        y = energy_list,
        marker = dict(color = 'blue', size = 10),
        mode = 'markers',
        name = 'Billboard Hot 100 Rank vs Spotify Song Energy',
    ))
    fig4.update_layout(title = "Billboard Hot 100 Rank vs Spotify Song Energy",
                        xaxis_title="Hot 100 Rank", yaxis_title="Spotify Song Energy", xaxis=dict(range=[0, 100]))
    fig4.show()

def main():
    
    #sets up cur and conn
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/top_100_songs.db')
    cur = conn.cursor()

    # runs each visual 
    visual1(cur)
    visual2(cur)
    visual3(cur)
    visual4(cur)

    
if __name__ == "__main__":
    main()

