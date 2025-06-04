# Heartbeat sends Date, Status, Token, Mac-Add
# Need to make it run in a service thread, make it send something every 1 min at least for testing
# Make Monitoring service in web api, that makes a map of all devices and then last heartbeat.

from Services.hestia_api_service import api_POST
from Utility.Mac_Address_Util import get_mac_address
from Utility.Date_Util import get_date

from enum import Enum
import threading
import json
import time

DeviceMode = Enum('DeviceMode', [('Online', 'Online')])

with open('config.json') as json_data:
    d = json.load(json_data)
    BASE_URL = d['IP'] + "/api/devices/heartbeat"
    TOKEN = d['Token']

def heart_beat():
    while True:
        #Send online confirmation to webApi
        api_POST(BASE_URL, heart_beat_payload())
        time.sleep(60)

def one_time_heartbeat():
	api_POST(BASE_URL, heart_beat_payload())


def heart_beat_payload():

    return {
        "date": get_date(),
        "Status": DeviceMode.Online.name,
        "Token": TOKEN,
        "mac": get_mac_address()
    }

def start_heartbeat_thread():
    thread = threading.Thread(target=heart_beat, daemon=True)
    thread.start()
