from gpiozero import Servo
from time import sleep

# Lazy-loaded servos
left_servo = None
right_servo = None

def initialize_servos():
    global left_servo, right_servo
    if left_servo is None or right_servo is None:
        print("Initializing servos...")
        left_servo = Servo(26)
        right_servo = Servo(20)
        sleep(0.5)  # Give them time to settle

def open_arms():
    initialize_servos()
    print("Opening arms...")
    left_servo.value = -1.0
    right_servo.value = 1.0
    sleep(1)

def close_arms():
    initialize_servos()
    print("Closing arms...")
    left_servo.value = 1.0
    right_servo.value = -1.0
    sleep(1)
