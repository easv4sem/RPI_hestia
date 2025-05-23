from services.hestia_logger import setup_logger
from picamera2 import Picamera2, Preview
from time import sleep
import tempfile
import os
import subprocess

logger = setup_logger(__name__)

# Configurable capture limits
min_width: int = 640
max_width: int = 2592
min_height: int = 480
max_height: int = 1944
sleep_time: int = 2  # seconds

# Method to capture a JPEG image from the camera and return it as a byte string
def capture_jpeg_binary(width, height):
    logger.info('Starting JPEG capture process')

    if not (min_width <= width <= max_width):
        logger.error(f"Width {width} is out of bounds ({min_width}, {max_width})")
        raise ValueError(f"Width must be between {min_width} and {max_width}")

    if not (min_height <= height <= max_height):
        logger.error(f"Height {height} is out of bounds ({min_height}, {max_height})")
        raise ValueError(f"Height must be between {min_height} and {max_height}")

    picam2 = Picamera2()
    config = picam2.create_still_configuration(main={"size": (width, height)})
    picam2.configure(config)
    picam2.start()
    sleep(sleep_time)  # Allow camera to warm up

    try:
        # Capture the image directly into memory as bytes
        jpeg_data = picam2.capture_buffer("main")
    finally:
        picam2.stop()

    logger.info(f"Captured JPEG: {len(jpeg_data)} bytes")
    return jpeg_data

# Method to check if the camera is available
def is_camera_available() -> bool:
    logger.info('Checking camera availability')
    try:
        result = subprocess.run(
            ["libcamera-hello", "--list-cameras"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )
        output = result.stdout.decode()
        logger.debug(f"Camera availability output: {output}")
        return "Available cameras" in output
    except Exception as e:
        logger.error(f"Error checking camera availability: {e}")
        return False
