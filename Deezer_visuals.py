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


    cur.execute('SELECT song_id, songs_deezer_rank FROM Deezer')
    results = cur.fetchall()

    #creates empty lists to store the information
    songs_list = []
    ranks_list = []

    for r in results: 
        songs_list.append(r[0])
        ranks_list.append(r[1])
    
    figure1 = go.Figure()
    figure1.add_trace(go.Scatter(
        x = ranks_list,
        y = songs_list,
        marker = dict(color = 'red', size = 10),
        mode = 'markers',
        name = 'Deezer Song Rank vs Rank in Billboard 100 Chart',
    ))
    figure1.update_layout(title = 'Deezer Song Rank vs Rank in Billboard 100 Chart', xaxis_title = 'Deezer Rank',
        yaxis_title = 'Billboard Rank', xaxis = dict(range = [20000,1000000]))
    figure1.show()
    
    #creates a scatter plot of each songs Spotify popularity vs weeks on Hot 100 chart to see if correlation
    


if __name__ == "__main__":
    main()

