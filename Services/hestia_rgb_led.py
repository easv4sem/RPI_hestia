import RPi.GPIO as GPIO
import threading
import time

green_pin = 26

GPIO.setmode(GPIO.BCM)

GPIO.setup(green_pin, GPIO.OUT)

green_pwm = GPIO.PWM(green_pin, 500)

green_pwm.start(0)

def on_led():

        while 1:
                for dc in range(0, 101, 5):
                    green_pwm.ChangeDutyCycle(dc)
                    time.sleep(0.1)
                for dc in range(100, -1, -5):
                    green_pwm.ChangeDutyCycle(dc)
                    time.sleep(0.1)

def start_led_thread():

	thread = threading.Thread(target=on_led, daemon=True)
	thread.start()
