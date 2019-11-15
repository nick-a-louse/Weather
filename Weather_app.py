import urllib.request, urllib.parse, urllib.error
import http
import sqlite3
import json
import datetime
import ssl
import sys
from address_lookup import get_coordinates
from meteostat_station_lookup import get_station
from meteostat_weather_retrieval import get_weather

#-----------API keys-----------:
keys_file = open('key.txt')
lines = keys_file.readlines()
google_key = lines[0].rstrip()
meteo_key = lines[1].rstrip()

#-----------Google geocode api endpoint-----------
gserviceurl = "https://maps.googleapis.com/maps/api/geocode/json?"
meteostationserviceurl = "https://api.meteostat.net/v1/stations/nearby?"
meteodataserviceurl = "https://api.meteostat.net/v1/history/daily?"
#-------------------------------------------------

# Additional detail for urllib
# http.client.HTTPConnection.debuglevel = 1

#-----------Preparing the DB tables-----------
conn = sqlite3.connect('geodata.sqlite')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS Locations (
    id              INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    address         TEXT,
    geodata         TEXT,
    station_id      INTEGER
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Stations (
    id              INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    station_id      INTEGER UNIQUE,
    station_name    TEXT
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Weather (
    id              INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    unique_id       TEXT UNIQUE,
    station_id      INTEGER,
    date            TEXT,
    temperature     FLOAT,
    temperature_min FLOAT,
    temperature_max FLOAT,
    precipitation   FLOAT,
    snowfall        INTEGER,
    snowdepth       INTEGER,
    winddirection   INTEGER,
    windspeed       FLOAT,
    peakgust        FLOAT,
    sunshine        FLOAT,
    pressure        FLOAT
)
''')

#-----------De-duplicate dates-----------

def dedup(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

#-----------Ignore SSL certificate errors-----------
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

print ('\r\n')

#-----------Retrieve the coordinates of the locations-----------


while True:
    location_1 = (input('Enter location 1:')).lower()
    if len(location_1) < 1:
        print ('Location too short\r\n')
        continue
    else:
        loc_1_coords = get_coordinates(location_1)
        break

while True:
    location_2 = (input('Enter location 2: ')).lower()
    if location_2 == location_1:
        print ('location 2 is the same as location 1. Please enter a different adddress')
        continue
    elif len(location_2) < 1:
        print ('Location too short\r\n')
        continue
    else:
        loc_2_coords = get_coordinates(location_2)
        break

while True:
    start_date = (input('Enter a start date (in the format YYYY-MM-DD): '))
    if len(start_date) == 0:
        print ('Please enter a start date')
        continue
    elif len(start_date) < 10:
        print ('Please enter a valid start date')
        continue
    else:
        break

while True:
    end_date = (input('Enter an end date (in the format YYYY-MM-DD): '))
    if len(end_date) == 0:
        print ('Please enter an end date')
        continue
    elif len(end_date) < 10:
        print ('Please enter a valid end date')
        continue
    else:
        break

#print ('\r\nLocation 1, Latitude:', loc_1_coords[0], ', Longitude:', loc_1_coords[1])
#print ('Location 2, Latitude:', loc_2_coords[0], ', Longitude:', loc_2_coords[1])

#-----------Retrieve and store the nearest weather station details-----------

loc_1_station = get_station(loc_1_coords)
loc_2_station = get_station(loc_2_coords)

#print ('\r\nLocation 1, Weather Station Name:',loc_1_station[0], ', Station Id:', loc_1_station[1])
#print ('Location 2, Weather Station Name:',loc_2_station[0], ', Station Id:', loc_2_station[1], '\r\n')

#-----------Retrieve the weather for the selected weather station and add to the database-----------

print ('Retrieving weather for', loc_1_station[0])
dates = list()
loc_1_weather = get_weather(loc_1_station[1], start_date, end_date, dates)

#do something here with dates

while True:
    if loc_1_weather[0] > 0:
        print ('Found',loc_1_weather[0], 'days of data for this station in the selected date range\r\n')
        print ('loc 1 dates list', len(loc_1_weather[1]))

        print ('Retrieving weather for', loc_2_station[0])
        loc_2_weather = get_weather(loc_2_station[1], start_date, end_date, loc_1_weather[1])
        if loc_2_weather[0] > 0:
            print ('Found',loc_2_weather[0], 'days of data for this station in the selected date range\r\n')
            print ('loc 2 dates list', len(loc_2_weather[1]))
            dates = (loc_2_weather[1])
        else:
            print ('No data available for this station in the selected date range. Stopping.\r\n')
            break
        break
    else:
        print ('No data available for this station in the selected date range. Stopping\r\n')
        break

print (len(dates))

#d_dates = dedup(dates)
#print (len(d_dates))


#-----------Perform analysis on the data-----------

#query = "SELECT * FROM `tbl`"

#cursor.execute(query)

#result = cursor.fetchall() //result = (1,2,3,) or  result =((1,3),(4,5),)

#final_result = [list(i) for i in result]

#----------
#cur.execute('SELECT date, temperature FROM Pages WHERE url=? LIMIT 1', ( href, ))
#try:#
#    row = cur.fetchone()
#    toid = row[0]

#dates = ['bar', 'chocolate', 'chips']
#loc_1_temps = [0.05, 0.1, 0.25]
#loc_2_temps = [2.0, 5.0, 3.0]
#temp_delta = [40.0, 50.0, 12.0]


#titles = ['date',(loc_1_station, '(°C)'), (loc_2_station, '(°C)'), 'Delta (°C)']
#data = [titles] + list(zip(names, weights, costs, unit_costs))

#for i, d in enumerate(data):
#    line = '|'.join(str(x).ljust(12) for x in d)
#    print(line)
#    if i == 0:
#        print('-' * len(line))
