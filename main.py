from services.hestia_logger import setup_logger
logger = setup_logger(__name__)

# importent that moduels are imported after the logger is set up. 
from modules.camera.hestia_camera import capture_jpeg_binary

# Temperature, Humidity and Pressure sensor import
from modules.m_bme2080 import hestia_bme2080 as bme280

def main():
    logger.info('Started')

    capture_jpeg_binary(640, 480)
        
    logger.info('Finished')

    bme280_output = bme280.bme280_module()

if __name__ == '__main__':
    main()