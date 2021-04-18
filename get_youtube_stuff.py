from pyyoutube import Api
import pandas as pd
import requests
import re
import os 
import csv
import sqlite3
import json 


#api key 
yt_key = Api(api_key="AIzaSyAa1ctT3bvVji_yvLIECttn8_4v7iV5aGU")

#takes in database name, returns cur and conn

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect('top_100_artists.db')
    cur = conn.cursor()
    return cur, conn

#how to get statistics for someone's channel
#request = youtube.channels().list(part = 'statistics', id = 'UCxeOKL4PQYB5z_85dliQA_Q')
#response = request.execute()
#print(response)

def getChannels(cur, conn):
    '''Takes in cursor and connection; Returns list of channel ids
    '''
    #List of tuples of artist names
    artists_tup = []
    cur.execute(f'SELECT name FROM Hot_100_Artists')
    for names in cur.fetchall():
        artists_tup.append(names)

    
    #change tuple to list
    artists_list = [item for t in artists_tup for item in t]
    print(artists_list)

    #for each artist, fetch info
    #for i in artists_list:
    request = yt_key.search_by_keywords(q= artists_list[0], search_type='channel', limit = 1)['channel_id']

    print(request)
    
'''
    #makes a list of each artist's channel_id
    channel_ids = []
    for i in request:
        channel = i['items'][0]['channelId']
        channel_ids.append(channel)
    
    #print(channel_ids)
    return channel_ids
    
'''
def getNumSubscribers(channel_ids):
     #Takes in channel ids, cursor, and connection; Returns list subscriber counts
    
    #get statistics for each channel
    for i in channel_ids:
        request = youtube.channel().list(part = 'statistics', maxResults = 1, channelId = i)
        response_channels = request.execute()
        #print(response_channels)
    
    #list of num subscribers
    numSubscribers = []
    for i in response_channels:
        subscribers = i['subscriberCount']
        numSubscribers.append(subscribers)
    #print(numSubscribers)
    return numSubscribers
    
    pass

def getViewCount(response_channels):
    ''' Takes in channel statistics (response_channels); Returns list view counts
    '''
    viewCount = []
    for i in response_channels:
        views = i['viewCount']
        viewCount.append(views)
    print(viewCount)
    return viewCount
    pass

def createTups(artist_list, numSubscribers, viewCount, channel_ids):
    '''Takes in all lists, creates a list of tuples w all info for each artist
    '''
    all_info = [(artist_list[i], channel_ids[i], numSubscribers[i], viewCount[i]) for i in range(0, len(artist_list))]
    return all_info
    pass
def setUpYouTubeTable(all_info, cur, conn):
    ''' Takes in list of tuples (all_info), cursor, and connection; Creates table with each artist's youtube data
    '''
    cur.execute("CREATE TABLE IF NOT EXISTS YouTube (artist_id INTEGER PRIMARY KEY, name TEXT, channel_id TEXT, number of subscribers INTEGER, view count INTEGER)")
    artist_id = 0
    for artist in all_info:
        artist_id += 1 
        name = artist[0]
        channel_id = artist[1]
        subscribers = artist[2]
        views = artist[3]
        cur.execute("INSERT OR IGNORE INTO YouTube (artist_id, name, channel_id, subscribers, views) VALUES (?, ?, ?, ?, ?)", (artist_id, name, channel_id, subscribers, views, ))
    conn.commit()
    pass


def joinTables():
    '''
    
    '''
    
def avgSubscribers(numSubscribers):
    '''Calculate avg number of subscribers for top 100 artists
    '''
    subCount = 0
    for i in numSubscribers:
        subCount += i

    avgSubscribers = subCount/100
    return avgSubscribers
    pass

def avgViews(viewCount):
    '''Calculate avg view count for top 100 artists
    '''
    viewsTotal = 0
    for i in viewCount:
        viewsTotal += i
    avgViews = viewsTotal/100
    return avgViews
    pass

def main():
    cur, conn = setUpDatabase('top_100_artists.db')
    getChannels(cur,conn)
    #getNumSubscribers(channel_ids, cur, conn)
    #getViewCount(response_channels, cur, conn)
    #createTups(artist_list, numSubscribers, viewCount, channel_ids)
    #setUpYouTubeTable(all_info, cur, conn)
    #avgSubscribers(numSubscribers)
    #avgViews(viewCount)

if __name__ == "__main__":
    main()