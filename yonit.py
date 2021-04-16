from googleapiclient.discovery import build
import requests
import re
import os 
import csv
import sqlite3
import json 


#api key 
api_key = 'AIzaSyB_Fx4Daz_iTVGMNZEBp5Oc4mwOyYDeqGI'
youtube = build('youtube', 'v3', developerKey = api_key)




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
   #Returns list of channel ids
    
    #list of tuples of artist names
    artists_tup = []
    cur.execute(f'SELECT name FROM Hot_100_Artists')
    
    for names in cur.fetchall():
        artists_tup.append(names)
    
    #list of artist names
    artists_list = [item for t in artists_tup for item in t]
    
    #for each artists, fetch info
    for i in artists_list:
        request = youtube.search().list(q = i, part = 'snippet', maxResults = 1, type = 'channel')
        response_names = request.execute()
        print(response_names)
        return response_names

    #makes a list of each artist's channel_id
    channel_ids = []
    for i in response_names:
        channel = i['items'][0]['channelId']
        channel_id.append(channel)
    print(channel_ids)
    return channel_ids
    

def getNumSubscribers(channel_ids, cur, conn):
    ''' Returns list of tuples: (artist, subscribers)
    '''
    #print all channel ids
    for i in channel_ids:
        request = youtube.channel().list(part = 'statistics', maxResults = 1, channelId = i)
        response_channels = request.execute()
        print(response_channels)
        return response_channels
    
    #print num subscribers
    numSubscribers = []
    for i in response_channels:
        subscribers = i['subscriberCount']
        numSubscribers.append(subscribers)
    print(numSubscribers)
    return numSubscribers
    

def getViewCount(response_channels, cur, conn):
    ''' Returns list of tuples: (artist, viewCount)
    '''
    viewCount = []
    for i in response_channels:
        views = i['viewCount']
        viewCount.append(views)
    print(viewCount)
    return viewCount

def createTups(artist_list, numSubscribers, viewCount, channel_ids):
    all_info = [(artist_list[i], channel_ids[i], numSubscribers[i], viewCount[i]) for i in range(0, len(artist_list))]

def setUpYouTubeTable(all_info, cur, conn):
    ''' create's table with each artist's youtube data
    '''
    cur.execute("CREATE TABLE IF NOT EXISTS YouTube (artist_id INTEGER PRIMARY KEY, name TEXT, channel_id TEXT, number of subscribers INTEGER, view count INTEGER)")
    data = createTups()
    artist_id = 0
    for artist in data:
        artist_id += 1 
        name = artist[0]
        channel_id = artist[1]
        subscribers = artist[2]
        views = artist[3]
        cur.execute("INSERT OR IGNORE INTO YouTube (artist_id, name, channel_id, subscribers, views) VALUES (?, ?, ?, ?, ?)", (artist_id, name, channel_id, subscribers, views, ))
    conn.commit()



def avgSubscribers(numSubscribers):
    '''Calculate avg number of subscribers for top 100 artists
    '''
    subCount = 0
    for i in numSubscribers:
        subCount += i

    avgSubscribers = subCount/100
    return avgSubscribers


def avgViews(viewCount):
    '''Calculate avg view count for top 100 artists
    '''
    viewsTotal = 0
    for i in viewCount:
        viewsTotal += i
    avgViews = viewsTotal/100
    return avgViews


def main():
    cur, conn = setUpDatabase('top_100_artists.db')
    getChannels(cur,conn)
    getNumSubscribers()
    getViewCount()
    createTups()
    setUpYouTubeTable()
    avgSubscribers()
    avgViews()

if __name__ == "__main__":
    main()