# ft2gee: Fusion table to EE tables CLI
Convert all fusion table in your Google Drive and Google Earth Engine scripts to Google Earth Engine Tables. The tool was resultant of the end of service for Google Fusion tables at the end of 2019 and while there might be migration options available at that period of time, earlier and more consistent move out of the Fusion table environment maybe necessary for some workflow. This requires creation of the Google Drive API credentials file with read access to run this on your Google Drive and you can find a more [detailed tutorial here](https://medium.com/@samapriyaroy/google-fusion-table-migration-with-within-google-earth-engine-93d103111ce7).

## Table of contents
* [Installation](#installation)
* [Getting started](#getting-started)
* [ft2gee Fusion table to EE tables CLI](#ft2gee-fusion-table-to-ee-tables-cli)
    * [quota](#quota)
    * [drive2tab](#drive2tab)
    * [gee2tab](#gee2tab)
    * [scriptcheck](#scriptcheck)

## Installation
This assumes that you have native python & pip installed in your system, you can test this by going to the terminal (or windows command prompt) and trying

```python``` and then ```pip list```

If you get no errors and you have python 2.7.14 or higher you should be good to go. Please note that I have tested this only on python 2.7.15, but it should run on Python 3.

To install **ft2gee: Simple CLI for Google Home & Mini** you can install using two methods.

```pip install ft2gee```

or you can also try

```
git clone https://github.com/samapriya/ft2gee.git
cd ft2gee
python setup.py install
```
For Linux use sudo or try ```pip install ft2gee --user```.

Installation is an optional step; the application can also be run directly by executing ft2gee.py script. The advantage of having it installed is that ft2gee can be executed as any command line tool. I recommend installation within a virtual environment. If you don't want to install, browse into the ft2gee folder and try ```python ft2gee.py``` to get to the same result.


## Getting started

As usual, to print help:

```
usage: ft2gee [-h] [--auth_host_name AUTH_HOST_NAME]
              [--noauth_local_webserver]
              [--auth_host_port [AUTH_HOST_PORT [AUTH_HOST_PORT ...]]]
              [--logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
              {quota,drive2tab,gee2tab,scriptcheck} ...

Fusion table to EE tables CLI

positional arguments:
  {quota,drive2tab,gee2tab,scriptcheck}
    quota               Print Earth Engine total quota and used quota
    drive2tab           Exports Google Drive Fusion tables to Earth Engine
                        tables
    gee2tab             Exports Earth Engine referenced fusion tables to Earth
                        Engine tables
    scriptcheck         Replaces referenced fusion tables in Earth Engine
                        scripts to EE tables

optional arguments:
  -h, --help            show this help message and exit
  --auth_host_name AUTH_HOST_NAME
                        Hostname when running a local web server.
  --noauth_local_webserver
                        Do not run a local web server.
  --auth_host_port [AUTH_HOST_PORT [AUTH_HOST_PORT ...]]
                        Port web server should listen on.
  --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set the logging level of detail.
```

To obtain help for specific functionality, simply call it with _help_ switch, e.g.: `ft2gee gee2tab -h`. If you didn't install ft2gee, then you can run it just by going to *ft2gee* directory and running `python ft2gee.py [arguments go here]`. Ignore the optional arguments for the main program as they are resultant of the oauth step with google API(s).

## ft2gee Fusion table to EE tables CLI
This tool is designed to use existing fusion tables in your google drive and your earth engine scripts and export them into Earth Engine tables. At that point they can be further exported out as shapefiles , or geojson and so on.

### quota
Just a simple tool to print your earth engine quota quickly.

```
usage: ft2gee quota [-h]

optional arguments:
  -h, --help  show this help message and exit
```

### drive2tab
This requires you to create a google drive credentials file, you can get instructions for this on the medium tutorial that was included at the beginning of the readme. This tool will use your credentials to give you access to all fusion tables in your drive and will export all of them to an earth engine folder.

```
usage: ft2gee drive2tab [-h] --gee GEE [--credentials CREDENTIALS]

optional arguments:
  -h, --help            show this help message and exit

Required named arguments.:
  --gee GEE             Path to Google Earth Engine asset folder for tables to
                        be exported

Optional named arguments:
  --credentials CREDENTIALS
                        Credentials file downloaded for gdrive
```

### gee2tab
This tool in designed to parse through Google Earth Engine codes that you can download from [Earth Engine Git Repo](https://earthengine.googlesource.com/). Once you have downloaded your files, you can point this to a folder and it will parse all lines with a fusion table and export them to an earth engine folder.

```
usage: ft2gee gee2tab [-h] --local LOCAL --gee GEE

optional arguments:
  -h, --help     show this help message and exit

Required named arguments.:
  --local LOCAL  Local path to folder with Google Earth Engine Scripts
  --gee GEE      Path to Google Earth Engine asset folder for tables to be
                 exported
```

### scriptcheck
This is still under development but the idea is once you have exported all your fusion tables to an Earth Engine folder, you can point a script and give it the folder path and it will replace the fusion table paths with Google table paths. For now it generates a file with '_FT' added to filename and current time when the script was written. It is designed for a single script for now but can be used for all scripts in folder for example.

```
usage: ft2gee scriptcheck [-h] --local LOCAL --gee GEE

optional arguments:
  -h, --help     show this help message and exit

Required named arguments.:
  --local LOCAL  Local path to a Google Earth Engine Script to check
  --gee GEE      Earth Engine folder where EE tables were exported
```
