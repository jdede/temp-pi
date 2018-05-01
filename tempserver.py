#!/usr/bin/env python3

from flask import Flask
from flask import Response
from flask import jsonify
import os
from ds18x20 import DS18X20

app = Flask(__name__)

sensors = DS18X20()

## Serve a file from the same directory where this script is located
def get_file(filename):
    f = os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)
    return open(f).read()


@app.route("/")
def index():
    return Response(get_file("index.html"), mimetype="text/html")

@app.route("/json")
def get_temps():
    return jsonify(sensors.read_temps())
    
## Serve on all known addresses on port 8080
if __name__ == "__main__":
    app.run(
            host = "::",
            port = 8080
            )

