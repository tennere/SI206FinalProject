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



def main():
    #Takes in nothing; Returns nothing; Selects data from the database and uses JOIN in order to create a scatterplot
    
    #sets up cur and conn
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/top_100_songs.db')
    cur = conn.cursor()


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
    
    #figure 1 = scatter plot of deezer rank vs billboard rank
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
    
    #figure 2: bar 
    figure2 = px.bar(
        x = artist_names[0:30],
        y = fan_number_list[0:30]
        )
    figure2.update_layout(title = 'Fan numbers for the artists of Billboard top 30 songs', xaxis_title = 'artist name', yaxis_title = 'artist fan number')
    figure2.show()    

    


if __name__ == "__main__":
    main()

