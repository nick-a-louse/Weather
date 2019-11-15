import urllib.request, urllib.parse, urllib.error
import http
import sqlite3
import json
import time
import ssl
import sys

#-----------API keys-----------
keys_file = open('key.txt')
lines = keys_file.readlines()
google_key = lines[0].rstrip()

#-----------API endpoint-----------
gserviceurl = "https://maps.googleapis.com/maps/api/geocode/json?"

#-----------Connect to database-----------
conn = sqlite3.connect('geodata.sqlite')
cur = conn.cursor()

#-----------Ignore SSL certificate errors-----------
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def get_coordinates(address):
    while True:

        #-----------Check if the address is in the database-----------
        print ('Checking database for location')
        cur.execute("SELECT geodata FROM Locations WHERE address LIKE ?", (memoryview(address.encode()), ))

        try:
            data = cur.fetchone()[0]
            print("Location found in database\r\n")

            js = json.loads(data)

            latitude = js['results'][0]['geometry']['location']['lat']
            longitude = js['results'][0]['geometry']['location']['lng']

            return (latitude, longitude)
            break

        except:
            pass

        #-----------Retrieve address details from Google Geocode APIs-----------
        parms = dict()
        parms['address'] = address
        parms['key'] = google_key
        url = gserviceurl + urllib.parse.urlencode(parms)

        #-----------print('Retrieving', url)-----------
        uh = urllib.request.urlopen(url, context=ctx)
        data = uh.read().decode()
#        print('Retrieved', len(data), 'characters', end = "\r\n")

        try:
            js = json.loads(data)
        except:
            js = None

        if not js or 'status' not in js or js['status'] != 'OK':
            print('==== Failure To Retrieve ====')
            print(data)
            continue

        #-----------Add location to the database-----------
        cur.execute('''INSERT INTO Locations (address, geodata)
            VALUES ( ?, ? )''', (memoryview(address.encode()), memoryview(data.encode()) ) )
        conn.commit()

        print ("Location added to database\r\n")

        latitude = js['results'][0]['geometry']['location']['lat']
        longitude = js['results'][0]['geometry']['location']['lng']

        return (latitude, longitude)

        break
