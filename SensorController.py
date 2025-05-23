#from Services.hestia_logger import setuplogger
from Services.hestia_api_service import api_GET, api_POST
from Services.hestia_heartbeat import start_heartbeat_thread

from Utility.Mac_Address_Util import get_mac_address
from Utility.Date_Util import get_date

from Modules.MoistureModule import measure_moisture
from Modules.ParticalModule import read_smoke_level
from Modules.BarometerModule import measure_barometer
from Modules.BuzzerModule import buzzing

import json
import time

with open('config.json') as json_data:
	d = json.load(json_data)
	BASE_URL = d['IP']

def get_from_api(url):

	response = api_GET(url)


def post_to_api(url, payload):

	response = api_POST(url, payload)



def payload_builder(mac_add, soil_val, camera_val, smoke_val, baro_val, date):

	sensorData = {
		"Mac-Add": mac_add,
		"Moisture": soil_val,
		"Camera": camera_val,
		"PPM": smoke_val,
		"Barometer": baro_val,
		"Date": date
	}
	return sensorData



def take_measurements():

	mac_add = get_mac_address()
	soil_val = measure_moisture()
	camera_val = 1 #Temp val until camera works
	smoke_val = read_smoke_level()
	baro_val = measure_barometer()
	date = get_date()

	payload = payload_builder(mac_add, soil_val, camera_val, smoke_val, baro_val, date)

	return payload

def main_loop():

	while True:
		print("Inside while loop")
		smoke_level = read_smoke_level()
		if (smoke_level["MQ-135"]["ppm"] > 1):
			post_to_api(BASE_URL + "/api/sensorReadings/", take_measurements())
			#buzzing()

		print("Sleepy time...")
		time.sleep(10)

start_heartbeat_thread()

main_loop()

