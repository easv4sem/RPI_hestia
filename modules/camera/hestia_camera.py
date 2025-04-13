from services.hestia_logger import setup_logger
from picamzero import Camera
from time import sleep
import tempfile
import os
import subprocess

logger = setup_logger(__name__)

# Configurable capture limits
min_width : int = 640 
max_width : int = 2592
min_height : int = 480
max_height : int = 1944
sleep_time : int = 2  # seconds

# Method to capture a JPEG image from the camera and return it as a byte string
def capture_jpeg_binary(width, height):
    logger.info('Starting JPEG capture process')

    # Validate input with dimensions
    if not (min_width <= width <= max_width):
        logger.error(f"Width {width} is out of bounds ({min_width}, {max_width})")
        raise ValueError(f"Width must be between {min_width} and {max_width}")
    
    # Validate input height dimensions
    if not (min_height <= height <= max_height):
        logger.error(f"Height {height} is out of bounds ({min_height}, {max_height})")
        raise ValueError(f"Height must be between {min_height} and {max_height}")

    cam = Camera()
    cam.still_size = (width, height)
    sleep(sleep_time)

    # Create a temporary file to store the JPEG data
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        temp_path = tmp.name

    # Capture the image and save it to the temporary file
    cam.take_photo(temp_path)

    # Read the JPEG data from the temporary file
    try:
        with open(temp_path, "rb") as f:
            jpeg_data = f.read()
    finally:
        # Clean up the temporary file, even if an error occurs
        os.remove(temp_path)

    # Return the JPEG data as a byte string
    logger.info(f"Captured JPEG: {len(jpeg_data)} bytes")
    return jpeg_data


# Method to check if the camera is available
# This method uses subprocess to run the libcamera-hello command 
# and checks its output for available cameras 
# It returns True if cameras are available, otherwise False 
def is_camera_available() -> bool:
    logger.info('Checking camera availability')
    try:
        result = subprocess.run(
            ["libcamera-hello", "--list-cameras"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )
        logger.debug(f"Camera availability output: {result.stdout.decode()}")
        return "Available cameras" in result.stdout.decode()
    except Exception as e:
        logger.error(f"Error checking camera availability: {e}")
        return False