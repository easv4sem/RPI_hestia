import RPi.GPIO as GPIO
import time

BUZZER_PIN = 5

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

buzz = GPIO.output(BUZZER_PIN, False)

def buzzing():
    try:
        print("Buzzing...")
        buzz = GPIO.output(BUZZER_PIN, True)
        time.sleep(2)
    finally:
        buzz = GPIO.output(BUZZER_PIN, False)



