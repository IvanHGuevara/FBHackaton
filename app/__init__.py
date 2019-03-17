from flask import Flask, render_template, jsonify
import getpass
import sys
import telnetlib
import requests
import socket
#socket.getaddrinfo('127.0.0.1', 5000)

app = Flask(__name__)


def validationMessage(income):
    incoming_message=income

    
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
    else:
        outgoing_message = "Sorry! I don't recognize that instruction. Please try again"

    return outgoing_message

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/<id_root>/<instruction>")
def send_instruction(id_root, instruction):

    message = validationMessage(instruction)

    return jsonify(message)
    #return jsonify("SERVER ->"+ id_root + "\nACTIONS -> "+ instruction)