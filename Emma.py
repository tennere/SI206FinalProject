#Name: Emma Tenner
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import requests
import re
import os
import csv
import sqlite3
import json

c_id = '9131842b33cd43bebd1704950e78b73a'
c_secret = 'ee9385f45c994c5183118ed534cfc240'

client_credentials_manager = SpotifyClientCredentials(client_id = c_id, client_secret = c_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def join_tables(cur, conn):
    #This function ???
    pass

def get_artists_list():
    #This function returns an artist list???
    pass

def create_spotify_table(cur, conn):
    #Takes in the database cursor and connection as inputs and returns nothing. 
    # Creates a table called Spotify_Table and finds the Spotify popularity 
    # of each artist (is that possible? it's possible for each song) and inserts it into the table
    pass

def average_weeks(cur,conn):
    #This function will take the database cursor and connection as inputs. 
    # Returns an integer, which is the average number of weeks on the Top 100 list 
    # of current Billboard Top 100 Artists on Spotify.
    pass

def write_data_to_file(filename, cur, conn):
    #Takes in a filename (string) as an input and the database cursor/connection. 
    # Returns nothing. Creates a file and writes return value of the 
    # function average_weeks() to the file.
    pass

def main():
    #Takes in nothing and returns nothing. Calls the functions.
    pass