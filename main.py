from services.hestia_logger import setup_logger
logger = setup_logger(__name__)

# importent that moduels are imported after the logger is set up. 
from modules.camera.hestia_camera import capture_jpeg_binary

def main():
    logger.info('Started')

    capture_jpeg_binary(640, 480)
        
    logger.info('Finished')

if __name__ == '__main__':
    main()