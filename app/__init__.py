from flask import Flask, render_template, jsonify
import getpass
import sys
import telnetlib
import requests
import socket
#socket.getaddrinfo('127.0.0.1', 5000)
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

PORT_NUMBER = 8080
SPOTIPY_CLIENT_ID = "79d4b9443c804d1c84ecb8190dcf4898"
SPOTIPY_CLIENT_SECRET = "c9e17ddc434b4aa09a48b8d02a83f1c1"
SPOTIPY_REDIRECT_URI = 'http://localhost:8080'
SCOPE = 'user-library-read'
CACHE = '.spotipyoauthcache'

client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

app = Flask(__name__)


def validationMessage(income):
    incoming_message=income
    
    if(len(incoming_message) < 0): 
        outgoing_message = "No data"
    #if(id_root == str(1)):
    HOST = "192.168.1.5"

    dict={
        "Prender luces": "Luces encendidas",
        "prender luces": "Luces encendidas",
        "Apagar luces": "Luces apagadas",
        "apagar luces": "Luces apagadas",
        "state?": "state",
        "State?": "state",
        "Estado?": "state",
        "estado?": "state",
        "estado": "state",
        "state": "state",
        "Turn On" : "Luces encendidas",
        "Turn Off" : "Luces apagadas",
        "turn on" : "Luces encendidas",
        "turn off" : "Luces apagadas"
    }

    if incoming_message in dict:
        if dict[incoming_message] != "state":
            outgoing_message = dict[incoming_message]
            if(outgoing_message == "Luces encendidas"):
                req = requests.get("http://"+HOST+"/on")
                print(req.text)
            elif(outgoing_message == "Luces apagadas"):
                req = requests.get("http://"+HOST+"/off")
        else:
            req = requests.get("http://"+HOST+"/state")
            state = ""
            if(req.text == "Off"):
                state = "OFF"
            else:  
                state = "ON"
            outgoing_message = "The current light state is: " + state
    elif(incoming_message[0:4] == "info"):
        outgoing_message = search_song(incoming_message[4:])
    elif(incoming_message[0:4] == "open"):
        outgoing_message = get_linkTo(incoming_message[4:])
    else:
        print(incoming_message[0:4])
        outgoing_message = "Sorry! I don't recognize that instruction. Please try again"

    return outgoing_message

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/<id_root>/<instruction>")
def send_instruction(id_root, instruction):

    message = validationMessage(instruction)

    return message
    #return jsonify("SERVER ->"+ id_root + "\nACTIONS -> "+ instruction)

@app.route("/search/<name>")
def search_song(name):
    results = spotify.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        artist = items[0]
        text_complete = "The band name is "+artist['name']+"\n"
        text_complete += "His popularity is "+str(artist['popularity'])+"% \n"
        text_complete += "Play genres like: "+" ".join(artist['genres'])+"\n"
        text_complete += "Has a lot of followers, precisly "+str(artist['followers']['total'])+"\n"
    else:
        text_complete = "Write better the name, using ""info *the band whatever you want*"""
    return text_complete
    #return items

def get_linkTo(name):
    results = spotify.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        artist = items[0]
        text = artist['external_urls']['spotify']
    else:
        text = "No artist find"    
    return text