#left_servo = Servo(26, min_pulse_width=0.0005, max_pulse_width=0.0025)
#right_servo = Servo(20, min_pulse_width=0.0005, max_pulse_width=0.0025)

# driver/servo.py

from gpiozero import Servo
from time import sleep

left_servo = None
right_servo = None

def init_servos():
    global left_servo, right_servo
    if left_servo is None or right_servo is None:
        left_servo = Servo(26, min_pulse_width=0.0005, max_pulse_width=0.0025)
        right_servo = Servo(20, min_pulse_width=0.0005, max_pulse_width=0.0025)

def open_arms():
    init_servos()
    print("Opening arms...")
    left_servo.value = 1.0
    right_servo.value = -1.0
    sleep(1)

def close_arms():
    init_servos()
    print("Closing arms...")
    left_servo.value = -1.0
    right_servo.value = 1.0
    sleep(1)
