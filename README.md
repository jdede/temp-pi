This is the Temp-Pi-Repository
==============================

Temp-Pi serves the sensor reading from DS1820, DS18S20 and DS18B20 one-wire
temperature sensors on a RaspberryPi using Apache2, Flask and Python3.

Hardware
--------

To use this repository, you will need the following hardware:

- RaspberryPi (version one is sufficient) with Raspbian
- One of the above mentioned sensors
- A pullup-resistor (4k7)

Connect the sensor as follows with the RaspberryPi pinheader:

- Ground to a ground pin (GND)
- VDD to 3V3
- Data to GPIO 4
- The 4k7 resistor between 3V3 and GPIO4

Afterwards, enable the one wire bus using `sudo raspi-config`.

You should now be able to read the temperature from the file

`/sys/bus/w1/devices/xx-yyyyyyyyyyyy/w1_slave`

where `xx` is the sensor type (10 or 28) and `yyyyyyyyyyyy` is the sensor id.
Per default, you can connect up to 10 sensors to the RaspberryPi.

Software: Bare Minimum
----------------------

We assume that everything is located in `/home/pi/src/tempPi/`.
Clone this repository to `/home/pi/src/`, i.e. create the `src` directory and
clone this repository using the following command:

`git clone https://github.com/jdede/temp-pi tempPi`

You will need the following Software (in addition to this repository) for the minimum example:

- Python 3
- Flask

On Raspbian, you can install both using the following command:

`sudo apt-get install python3-flask`

Python 3 will be installed automatically due to the dependencies.

If everything is installed and connected correctly, you can start the Flask
server: `./tempserver.py`. It offers two services on port 8080:

- `/json`: Return the ids and current readings from all sensors as a json
  object
- `/`: Get the data from `/json` and output it in a basic webpage

Both URLs show the data of all connected sensors in different ways.


Software: WSGI & Apache
-----------------------

This repository contains the files to serve the data using Apache2 and wsgi.
First, you should ensure that the bare minimum example works without any
problems. Afterwards, install the following packets:

- mod-wsgi-py3
- apache2

by entering the following command:

`sudo apt install libapache2-mod-wsgi-py3 apache2`

Now, perform the following steps:

1) Copy the virtual host configuration to the `/etc/apache2/sites-available/`:
`sudo cp temppi.conf /etc/apache2/sites-available`
2) Disable the default config. This is required as temp-pi serves at the same
URL: `sudo a2dissite 000-default.conf`
3) Enable the configuration for temp-pi: `sudo a2ensite temppi.conf`
4) Enable mod_wsgi: `a2enmod wsgi`
5) Reload apache2: `sudo systemctl reload apache2`

You can now access your sensor reading on port 80, i.e. by typing
`http://raspberrypi/` into your browser (assuming you have not changed the name
of your RaspberryPi).

Files
-----

This section briefly describes the main files in this repository.

- `ds18x20.py`: This is a basic driver for accessing the sensor readings.
- `tempserver.py`: This is the Flask app serving the readings.
- `index.html`: The file served when accessing the Flask application using the
  base URL `/`.
- `temppi.conf`: The configuration of the virtual host for Apache 2
- `tempserver.wsgi`: The WSGI configuration


License
=======

This work is licensed under the GPLv3 license

