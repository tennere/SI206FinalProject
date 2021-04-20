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
    """Takes no inputs and returns nothing. Selects data from the database in order to create visualizations (two dot plots, a scatterplot, and two bar charts.) """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/top_100_songs.db')
    cur = conn.cursor()


    #creates two lists by using JOIN ... one of weeks on chart and one of popularity
    cur.execute('SELECT Hot_100_Songs.weeks_on_chart, Spotify.popularity FROM Hot_100_Songs JOIN Spotify ON Spotify.track_id = Hot_100_Songs.rank')
    results = cur.fetchall()
    #separate them into lists
    popularity_list = []
    weeks_on_chart_list = []
    for r in results:
        popularity_list.append(r[1])
        weeks_on_chart_list.append(r[0])
    
    #creates a scatter plot of each songs popularity vs weeks on chart to see if correlation
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


    #Ewelina's:
    #Creates a scatterplot of comparing popularity of a song on Spotify versus its ranking on the Billboard Hot 100.
    fig = go.Figure(data=go.Scatter(x = popularity_list,
                                y = weeks_on_chart_list,
                                mode = 'markers',
                                marker_color = "rgb(153, 0, 153)"))
    fig.update_traces(mode='markers', marker_line_width=2, marker_size=15)
    fig.update_layout(title='Spotify Popularity of Top 100 Songs vs. # Weeks on Billboard 100 Chart', xaxis_title="Popularity on Spotify", yaxis_title="# Weeks on Chart")
    fig.show()




    if __name__ == "__main__":
        main()