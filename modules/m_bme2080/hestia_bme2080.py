import smbus2
import bme280
import json

port = 1

address = 0x76

bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)

# Function that takes the measurements from the sensor,
# formats it as a json and returns it
def bme280_module():
	data = bme280.sample(bus, address, calibration_params)

	bme = {"bme": [
		{"Temperature": data.temperature,
		 "Humidity": data.humidity,
		 "Pressure": data.pressure
		 }]
	}

	bme280_output = json.dumps(bme)

	print(bme280_output)

	return bme280_output


