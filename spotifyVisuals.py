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

    #creates two lists by using JOIN, one list is of the popularity for each song (from the Spotify table) and one list is of the # weeks on chart (from the Hot_100_Songs table)
    cur.execute('SELECT Hot_100_Songs.weeks_on_chart, Spotify.popularity FROM Hot_100_Songs JOIN Spotify ON Spotify.track_id = Hot_100_Songs.rank')
    results = cur.fetchall()

    #creates empty lists to store the information
    popularity_list = []
    weeks_on_chart_list = []

    for r in results: 
        #appends the first element of each result to the weeks_on_chart list & appends the second element of each result to the popularity_list
        popularity_list.append(r[1])
        weeks_on_chart_list.append(r[0])
    
    #creates a scatter plot of each songs Spotify popularity vs weeks on Hot 100 chart to see if correlation
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x = popularity_list,
        y = weeks_on_chart_list,
        marker = dict(color = 'rgb(200,255,255)', size = 10),
        mode = 'markers',
        name = 'Spotify Popularity vs # Weeks on Billboard Hot 100 Chart',
    ))
    fig1.update_layout(title = "Spotify Popularity of Top 100 Songs vs. # Weeks on Billboard 100 Chart",
                        xaxis_title="Spotify Popularity", yaxis_title="# Weeks on Chart", xaxis=dict(range=[0, 250]))
    fig1.show()


    if __name__ == "__main__":
        main()