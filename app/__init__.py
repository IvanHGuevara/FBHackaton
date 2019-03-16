from flask import Flask, render_template
import getpass
import sys
import telnetlib
import socket
socket.getaddrinfo('127.0.0.1', 5000)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/<id_root>/<instruction>")
def send_instruction(id_root, instruction):

    if(id_root == str(1)):
        HOST = "192.168.1.5"
    tn = telnetlib.Telnet()
    tn.open(HOST)
    tn.write(str(instruction)+" \r\n")
    tn.close()
    return "Ok"