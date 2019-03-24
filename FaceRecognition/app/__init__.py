import requests
from flask import Flask, jsonify
import faceRecognition

pathFoto = "./app/static/detection/"

app = Flask(__name__)
@app.route("/quien_es")
def index(): 
    return jsonify(faceRecognition.run(pathFoto))