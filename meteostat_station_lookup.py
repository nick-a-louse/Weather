import urllib.request, urllib.parse, urllib.error
import http
import sqlite3
import json
import time
import ssl
import sys

#-----------API keys-----------:
keys_file = open('key.txt')
lines = keys_file.readlines()
meteo_key = lines[1].rstrip()

#-----------API endpoint-----------
meteostationserviceurl = "https://api.meteostat.net/v1/stations/nearby?"

#-----------Connect to database-----------
conn = sqlite3.connect('geodata.sqlite')
cur = conn.cursor()

#-----------Ignore SSL certificate errors-----------
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def get_station (coordinates):

    while True:
        #-----------Setting up the parameters to create the concatenated url-----------
        meteo_station = dict()
        meteo_station['lat'] = coordinates[0]
        meteo_station['lon'] = coordinates[1]
        meteo_station['key'] = meteo_key
        meteo_station['limit'] = '1'
        meteostateurl = meteostationserviceurl + urllib.parse.urlencode(meteo_station)

        ms = urllib.request.urlopen(meteostateurl, context=ctx)
        msdata = ms.read().decode()
        #print('Retrieved', len(msdata), 'characters', end = "\r\n")

        try:
            ms_js = json.loads(msdata)
        except:
            print ('No station found')
            break

        cur.execute('INSERT OR IGNORE INTO Stations (station_id, station_name) VALUES ( ?, ? )', (ms_js["data"][0]["id"], ms_js["data"][0]["name"]) )
        conn.commit()

        return (ms_js["data"][0]["name"],ms_js["data"][0]["id"], ms_js["data"][0]["distance"])
        break
