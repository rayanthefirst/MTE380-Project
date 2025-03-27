from gpiozero import Servo
from time import sleep

# These use the default RPi.GPIO pin factory
def open_arms():
    print("Opening arms...")
    left = Servo(26)
    right = Servo(20)
    left.value = -1.0
    right.value = 1.0
    sleep(1)
    left.detach()
    right.detach()

def close_arms():
    print("Closing arms...")
    left = Servo(26)
    right = Servo(20)
    left.max()      # Equivalent to left.value = 1.0
    right.min()     # Equivalent to right.value = -1.0
    sleep(1)
    left.detach()
    right.detach()
