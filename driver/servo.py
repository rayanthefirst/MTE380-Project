from gpiozero import Servo
from time import sleep

# Adjust pins to the actual GPIOs used for the servos
left_servo = Servo(22)
right_servo = Servo(23)

def open_arms():
    print("Opening arms...")
    left_servo.min()   # Fully open left arm
    right_servo.max()  # Fully open right arm
    sleep(1)

def close_arms():
    print("Closing arms...")
    left_servo.max()   # Pull left arm in
    right_servo.min()  # Pull right arm in
    sleep(1)
