#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python driver module for DS18x20 temperature sensors.
This driver reads out the temperature using the device tree.

Connect your 1-wire sensor to gnd, 3v3, GPIO4, add a pullup
resistor between 3v3 and GPIO4 and enable 1-wire using
raspi-config

This driver reads out all connected sensors and returns them as a dict

Jens Dede <github@jdede.de>, 2018
"""

import os
import glob
import time

import configparser


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

        self.raw_temps_cache = {}

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
    def __read_temp_raw(self, timeout=30):
        # Cache the values with a default timeout of 30 seconds as the file system
        # access is quite slow...
        cur_time = time.time()
        if len(self.raw_temps_cache.keys()) == 0 or \
            cur_time - float(list(self.raw_temps_cache.keys())[0]) > timeout:
                self.raw_temps_cache = {}
                self.raw_temps_cache[cur_time] = {}
                for node in self.device_data_files:
                    lines = None
                    with open(self.device_data_files[node], "r") as f:
                        lines = f.readlines()
                    self.raw_temps_cache[cur_time][node] = lines
                return self.raw_temps_cache[cur_time]
        else:
            return self.raw_temps_cache[list(self.raw_temps_cache.keys())[0]]

    # Get timestamp of last data
    def get_last_data_timestamp(self):
        return float(list(self.raw_temps_cache.keys())[0])

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

    # Return a more detailled dict of sensor data
    def read_all(self, configFile=os.path.join(os.path.abspath(os.path.dirname(__file__)), "sensorconfig.ini")):
        detailReturn = dict()

        config = configparser.ConfigParser()
        with open(configFile, "r", encoding="utf8") as f:
            config.read_file(f)

        defaults = config["DEFAULT"]

        # Fill values from ini file
        temps = self.read_temps()
        for node in temps:
            detailReturn[node] = dict()
            detailReturn[node]["value"] = temps[node]
            detailReturn[node]["id"] = node
            
            # Add either the sensor-specific data or the default values
            for df in defaults:
                if node in config.sections() and df in config[node]:
                    detailReturn[node][df] = config[node][df]
                else:
                    detailReturn[node][df] = defaults[df]

        # Post-processing, replace strings, calculate the corrected values
        for num, node in enumerate(detailReturn):
            for v in detailReturn[node]:
                if type(detailReturn[node][v]) == str:
                    detailReturn[node][v] = \
                            detailReturn[node][v].replace("##number##", str(num))

                # Convert to proper data types (not string)
                detailReturn[node][v] = self.__to_generic_type(detailReturn[node][v])

            detailReturn[node]["corrected_value"] = \
                    detailReturn[node]["value"] - float(detailReturn[node]["offset"])

            # Local timestamp
            detailReturn[node]["timestamp"] = self.get_last_data_timestamp()

            # Sensor type
            node_type = node.split("-")[0]
            if node_type == "28":
                detailReturn[node]["type"] = "DS18B20"
            elif node_type == "10":
                detailReturn[node]["type"] = "DS18S20/DS1820"
            else:
                detailReturn[node]["type"] = "UNKNOWN"

        return detailReturn

    # Convert a value to float, int or string
    def __to_generic_type(self, value):
        if type(value) != str:
            return value
        elif value.isnumeric():
            return int(value)
        try:
            return float(value)
        except:
            return value

                    
if __name__ == "__main__":
    sensor = DS18X20()

    while True:
        print(sensor.read_temps())
        print(sensor.read_all())
        time.sleep(5)
