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
    conn = sqlite3.connect(path+'/'+ db_name)
    cur = conn.cursor()
    return cur, conn


#how to get statistics for someone's channel
request = youtube.channels().list(part = 'statistics', id = 'UCxeOKL4PQYB5z_85dliQA_Q')
response = request.execute()
print(response)


'''def getChannels(cur, conn):
   #Returns list of tuples: (username, artist, subscribers, views)
   
    cur.execute('SELECT name FROM Hot_100_Artists')
    for row in cur.fetchall():
        print(row)
    cur.close()'''

def getNumSubscribers():
    ''' Returns list of tuples: (artist, subscribers)
    '''
def getViewCount():
    ''' Returns list of tuples: (artist, viewCount)
    '''

def setUpTable():
    ''' 

    '''

def avgSubscribers():
    '''Calculate avg number of subscribers for top 100 artists
    '''

def avgViews():
    '''Calculate avg view count for top 100 artists
    '''

def main():
    cur, conn = setUpDatabase('top_100_artists.db')
    getChannels(cur,conn)
