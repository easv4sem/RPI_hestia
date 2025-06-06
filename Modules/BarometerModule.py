import smbus2
import bme280
import json

port = 1
address = 0x76
bus = smbus2.SMBus(port)


def measure_barometer():
	calibration_params = bme280.load_calibration_params(bus, address)

	# the sample method will take a single reading and return a
	# compensated_reading object
	data = bme280.sample(bus, address, calibration_params)

	data = {
		"bme280": {
			"Temperature": data.temperature,
			"Pressure": data.pressure,
			"Humidity": data.humidity,
			"Type": "bme280"
		}
	}

	output = json.dumps(data)

	return output

