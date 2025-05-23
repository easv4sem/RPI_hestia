import busio
import digitalio
import board
import time
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
#rom services.hestia_logger import setup_logger

#logger = setup_logger(__name__)

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
 
# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)
 
# create the mcp object
mcp = MCP.MCP3008(spi, cs)
 
# create an analog input channel on pin 0
chan1 = AnalogIn(mcp, MCP.P1)


# Constants for valid sensor range (16-bit value)
MIN_SENSOR_VALUE = 0        # Maximum soil moisture level (very wet)
MAX_SENSOR_VALUE = 65535    # Minimum soil moisture level (very dry)

# global variables
moisture_range = MAX_SENSOR_VALUE - MIN_SENSOR_VALUE
raw_value = 0
percent_value = 0



def measure_moisture_percent():
    # result in percent
    moisture_percent = (1 - (raw_value / moisture_range)) * 100 
    moisture_percent = round(moisture_percent, 1)
    moisture_percent = max(0,min(100, moisture_percent))

    return moisture_percent


def measure_moisture():
    global raw_value, percent_value

    try:
        current_value = chan1.value

        # check that current value is in valid range
        if not (MIN_SENSOR_VALUE <= current_value <= MAX_SENSOR_VALUE):
            #logger.warning(f"Sensor value {current_value} is out of bounds.")
            raise ValueError(f"Sensor value {current_value} is not in range {MIN_SENSOR_VALUE}-{MAX_SENSOR_VALUE}")

        # check for division by zero
        if moisture_range == 0:
            #logger.error("Moisture range is 0")
            raise ZeroDivisionError("Moisture range cannot be 0")

        raw_value = current_value
        percent_value = measure_moisture_percent()

        #logger.info(f"Moisture percent: {percent_value} % (sensor value: {current_value})

        data = {
	    "YL-69":{
                "raw_data" : raw_value,
                "percent" : percent_value,
	        "Type": "YL-69"
	    }
        }

        return data


    # CHATGPT! 
    except ValueError as value_error:
        #logger.error(f"ValueError: {value_error}")
        print(f"Error: {value_error}")
        return None  # Eller en passende standardværdi

    except ZeroDivisionError as zero_division_error:
        #logger.error(f"ZeroDivisionError: {zero_division_error}")
        print(f"Error: {zero_division_error}")
        return None  # Eller en passende standardværdi

    except Exception as e:
        #logger.error(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}")
        return None  # Eller en passende standardværdi



