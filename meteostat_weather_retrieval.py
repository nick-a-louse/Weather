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
meteostationserviceurl = "https://api.meteostat.net/v1/history/daily?"

#-----------Connect to database-----------
conn = sqlite3.connect('geodata.sqlite')
cur = conn.cursor()

#-----------Ignore SSL certificate errors-----------
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

dates_list= list()


def get_weather (station,start_date,end_date,in_dates):
#    print('incoming dates list',len(in_dates))
    while True:
        #-----------Setting up the parameters to create the concatenated url-----------
        request_params = dict()
        request_params['station'] = station
        request_params['start'] = start_date
        request_params['end'] = end_date
        request_params['key'] = meteo_key

        stationdataurl = meteostationserviceurl + urllib.parse.urlencode(request_params)
        sd = urllib.request.urlopen(stationdataurl, context=ctx)
        station_data = sd.read().decode()

#        print('Retrieved', len(station_data), 'characters', end = "\r\n\r\n")

        try:
            js = json.loads(station_data)
            weather_data = js['data']
#            print ('data',weather_data[:2])
            dates_list = [i['date'] for i in weather_data if 'date' in i]
#            print (dates_list)
# put in a new list callled dates and add the dates from js['data']

            if (len(weather_data)) < 1:
                return (0)
                break

        except:
            break

        for item in weather_data:
            if ( len(weather_data) > 1 ) :
                cur.execute('''INSERT OR IGNORE INTO Weather
                (unique_id,station_id, date, temperature, temperature_min, temperature_max, precipitation, snowfall, snowdepth, winddirection, windspeed, peakgust, sunshine, pressure)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', ((str(station)+'_'+item['date']),station, item['date'], item['temperature'], item['temperature_min'], item['temperature_max'], item['precipitation'], item['snowfall'], item['snowdepth'], item['winddirection'], item['windspeed'], item['peakgust'], item['sunshine'], item['pressure']) )
        conn.commit()
        in_dates.append(dates_list)
#        print('Found',(len(weather_data)), 'days of data for this station in the selected date range\r\n')
#        print (len(weather_data))
#        print(dates_list)
        print('out dates',len(in_dates))
        return (len(weather_data), in_dates)

# update the return with the dates list

        break
