#!/usr/bin/env python3

"""
Python driver module for DS18x20 temperature sensors.
This driver reads out the temperature using the device tree.

Connect your 1-wire sensor to gnd, 3v3, GPIO4, add a pullup
resistor between 3v3 and GPIO4 and enable 1-wire using
raspi-config

This driver reads out all connected sensors and returns them as a dict
"""

import os
import glob
import time

## A DS18x20 driver module
#
# Read out the temperature values of all connected 1-wire temperature
# sensors
class DS18X20(object):
    def __init__(self, base_dir="/sys/bus/w1/devices/"):
        # Get all device dirs and corresponding files for all connected
        # 1-wire temperature sensors
        self.device_dirs = {}
        self.device_data_files = {}

        self.base_dir = base_dir

        # For DS1820 and DS18S20: 10*
        # For DS18B20: 28*
        for device in \
                glob.glob(self.base_dir + "10*") +\
                glob.glob(self.base_dir + "28*")  \
               :
            device_id = device.split("/")[-1]
            device_data = device + "/w1_slave"
            self.device_dirs[device_id] = device
            self.device_data_files[device_id] = device_data


    # Read the raw temperature string
    def __read_temp_raw(self):
        raw_temps = {}
        for node in self.device_data_files:
            lines = None
            with open(self.device_data_files[node], "r") as f:
                lines = f.readlines()
            raw_temps[node] = lines
        return raw_temps

    ## Return the id of all known and connected sensors
    def get_sensors(self):
        return self.device_dirs.keys()

    ## Return the temperature of one specific sensor
    def read_temp(self, node_id):
        if not node_id in self.get_sensors():
            return None

        lines = self.__read_temp_raw()[node_id]
        while lines[0].strip()[-3:] != "YES":
            time.sleep(0.2)
            lines = self.__read_temp_raw()[node_id]

        temp_pos = lines[1].find("t=")
        if temp_pos != -1:
            temp_string = lines[1][temp_pos+2:]
            return float(temp_string) / 1000.0
        else:
            return None

    # Return the temperature of all known sensors
    def read_temps(self):
        temps = {}
        for node_id in self.get_sensors():
            temps[node_id] = self.read_temp(node_id)

        return temps


if __name__ == "__main__":
    sensor = DS18X20()

    while True:
        print(sensor.read_temps())
        time.sleep(0.5)
