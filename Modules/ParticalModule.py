import busio
import digitalio
import board
import time
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
# from services.hestia_logger import setup_logger

# logger = setup_logger(__name__)

# SPI setup
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D22)
mcp = MCP.MCP3008(spi, cs)
chan0 = AnalogIn(mcp, MCP.P0)

# Constants
RAW_MIN = 0
RAW_MAX = 65535
RAW_RANGE = RAW_MAX - RAW_MIN

# Estimated PPM range based on typical smoke sensor analog output
PPM_MIN = 0       # Clean air
PPM_MAX = 1000    # Heavy smoke (adjust based on calibration)
PPM_RANGE = PPM_MAX - PPM_MIN

def convert_raw_to_ppm(raw_value):
    """Converts raw ADC value to estimated PPM."""
    ppm = (raw_value - RAW_MIN) / RAW_RANGE * PPM_RANGE + PPM_MIN
    return round(max(PPM_MIN, min(PPM_MAX, ppm)), 1)

def read_smoke_level():
    try:
        current_value = chan0.value

        if not (RAW_MIN <= current_value <= RAW_MAX):
            raise ValueError(f"Sensor value {current_value} is out of range {RAW_MIN}-{RAW_MAX}")

        ppm_value = convert_raw_to_ppm(current_value)

        return {
	        "MQ-135":{
                    "raw_data": current_value,
                    "ppm": ppm_value,
	            "Type": "MQ-135"
	        }
               }

    except ValueError as ve:
        print(f"ValueError: {ve}")
        return None

    except ZeroDivisionError as zde:
        print(f"ZeroDivisionError: {zde}")
        return None

    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


