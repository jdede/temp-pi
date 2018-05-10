#!/usr/bin/env python3
"""
Basic Flask server serving temperature readings on a RaspberryPi

Jens Dede <github@jdede.de>, 2018
"""

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

## Serve a static HTML page reading the sensor data from /json
@app.route("/")
def index():
    return Response(get_file("index.html"), mimetype="text/html")

## Return the sensor readings as json object
@app.route("/json")
def get_temps():
    return jsonify(sensors.read_temps())

## Return a signe value
@app.route("/json/<sensor_id>")
def get_temp_value(sensor_id):
    temps = sensors.read_temps()
    if sensor_id in temps:
        return jsonify(temps[sensor_id])
    else:
        return Response("Sensor not found", 404)


## Serve on all known addresses on port 8080
if __name__ == "__main__":
    app.run(
            host = "::",
            port = 8080
            )

