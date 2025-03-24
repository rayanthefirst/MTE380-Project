from gpiozero import Servo
from time import sleep


left_servo = Servo(26, min_pulse_width=0.0005, max_pulse_width=0.0025)
right_servo = Servo(20, min_pulse_width=0.0005, max_pulse_width=0.0025)

def open_arms():
    print("Opening arms...")
    left_servo.min()  
    right_servo.max()  
    sleep(1)

def close_arms():
    print("Closing arms...")
    left_servo.max()   
    right_servo.min()  
    sleep(1)
