from gpiozero import Servo
from time import sleep

# This uses default pin factory (RPi.GPIO)
left_servo = Servo(26)
right_servo = Servo(20)

def open_arms():
    print("Opening arms...")
    left_servo.value = -1.0
    right_servo.value = 1.0
    sleep(1)

def close_arms():
    print("Closing arms...")
    left_servo.value = 1.0
    right_servo.value = -1.0
    sleep(1)
