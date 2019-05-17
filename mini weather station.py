#!/usr/bin/python
# libraries
import json #library to import the json file for spreadsheets
import time #library for time management
import datetime #to show the date and time details




import os #import the Raspbian OS for executing commands
import sys
import urllib2
import json
import gspread
#to import the data from the oauth file created by Google to the service account for the user
from oauth2client.service_account import ServiceAccountCredentials
#to import the sense HAT libraries
from sense_HAT import SenseHAT

# Oauth JSON File
GDOCS_OAUTH_JSON = 'SenseFinal-debd6ac268c0.json'

# Google Docs spreadsheet name.
GDOCS_SPREADSHEET_NAME = 'Sense HAT Logs'	

# How long to wait (in seconds) between measurements.
FREQUENCY_SECONDS = 30 #delay time between the measurements is taken as 30 seconds

deflogin_open_sheet(oauth_key_file, spreadsheet):

	"""Connect to Google Docs spreadsheet and return the first worksheet"""
	try:
		scope = ['https://spreadsheets.google.com/feeds']
		credentials = ServiceAccountCredentials.from_json_keyfile_name('SenseFinal-debd6ac268c0.json', scope)
		gc = gspread.authorize(credentials)
		worksheet = gc.open(spreadsheet).sheet1
		return worksheet
	except Exception as ex:
		print ("Unable to login and get spreadsheet. Check OAuth credentials,spreadsheet name, and make sure spreadsheet is shared to the client_email address in the OAuth.json file")
		print ("Google sheet login failed with error:"), ex
	sys.exit(1)

sense = SenseHAT()
sense.clear()




print ("Logging sensor measurements to {0} every {1} seconds.").format(GDOCS_SPREADSHEET_NAME, FREQUENCY_SECONDS)
print ("Press Ctrl-C to quit.")
worksheet = None
#main code to take in the data from the sense HAT and keep updating on the spreadsheets
while True:
# Login if necessary.
	if worksheet is None:
		worksheet = login_open_sheet(GDOCS_OAUTH_JSON,GDOCS_SPREADSHEET_NAME)

# Attempt to get sensor reading.
	temp = sense.get_temperature()
	temp = round(temp, 1)
	humidity = sense.get_humidity()
	humidity = round(humidity, 1)
	pressure = sense.get_pressure()
	pressure = round(pressure, 1)
#notification part to send alert if values ecxeed or drop below a certain level
	h='WEATHER_EXTREMITY_ALERT!!'
	a='Temp is:'
	b='Humidity is:'
	if temp>35 or humidity>65:
		cmd = 'echo'+ ' '+ str(a) + str(temp) + ' '+ str(b) + str(humidity) + ' '+ '|'+ ' '+'mail'+ ' '+'-s'+ str(h) + ' '+ 'vishal8757@gmail.com'
	os.system(cmd)

#to display the data on the 8x8 LED RGB matrix of the sense HAT
	# 8x8 RGB
	sense.clear()
	info = 'Temperature (C): ' + str(temp) + 'Humidity: ' + str(humidity) + 'Pressure: ' +
	str(pressure)
	sense.show_message(info, text_colour=[255, 0, 0])

	# Print
	print ("Temperature (C): ", temp)
	print ("Humidity:", humidity)
	print ("Pressure: ", pressure)

	# Append the data in the spreadsheet, including a timestamp
	try:
		worksheet.append_row((datetime.datetime.now(), temp,humidity,pressure))

	except:
	# Error appending data, most likely because credentials are stale.
		print 'Append error, logging in again'
		worksheet = None
		time.sleep(FREQUENCY_SECONDS)
		continue

	# Wait 30 seconds before continuing
	print 'Wrote a row to {0}'.format(GDOCS_SPREADSHEET_NAME)
	time.sleep(FREQUENCY_SECONDS)