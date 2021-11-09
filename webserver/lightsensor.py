import RPi.GPIO as GPIO
import time

pin = 7
def get_light():
    GPIO.setmode(GPIO.BOARD)
    return rc_time(pin)

def rc_time (pin):
    count = 0
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.1)
    GPIO.setup(pin, GPIO.IN)
    while (GPIO.input(pin) == GPIO.LOW):
        count += 1

    return count

def light_loop():        
    try:
        while True:
            print(rc_time(pin))
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()