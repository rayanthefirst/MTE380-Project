#!/usr/bin/env python3
from gpiozero import Motor
import time

# Set up the motors.
# For the left motor, GPIO 14 is forward and GPIO 15 is backward.
# For the right motor, GPIO 12 is forward and GPIO 13 is backward.
left_motor = Motor(forward=14, backward=15)
right_motor = Motor(forward=12, backward=13)

SPEED = 0.5
# Calibration constant: seconds per degree of turning.
TURN_TIME_MULTIPLIER = 0.01

def init():
    """Initialize the motors (no extra GPIO setup needed for gpiozero)."""
    print("Motors initialized using gpiozero.")

def forward():
    """
    Drive the robot forward.
    Left wheel runs forward and right wheel runs backward.
    """
    left_motor.forward(speed=SPEED)
    right_motor.backward(speed=SPEED)
    print("Motor running forward.")

def backward():
    """
    Drive the robot backward.
    Left wheel runs backward and right wheel runs forward.
    """
    left_motor.backward(speed=SPEED)
    right_motor.forward(speed=SPEED)
    print("Motor running backward.")

def stop():
    """Stop both motors."""
    left_motor.stop()
    right_motor.stop()
    print("Motor stopped.")

def turn_right(degree):
    """
    Pivot right by running both wheels in the same direction.
    For a right turn (clockwise), run both motors forward.
    """
    duration = degree * TURN_TIME_MULTIPLIER
    left_motor.forward(speed=SPEED)
    right_motor.forward(speed=SPEED)
    time.sleep(duration)
    stop()
    print("Turned right {}°.".format(degree))

def turn_left(degree):
    """
    Pivot left by running both wheels in the same direction.
    For a left turn (counterclockwise), run both motors backward.
    """
    duration = degree * TURN_TIME_MULTIPLIER
    left_motor.backward(speed=SPEED)
    right_motor.backward(speed=SPEED)
    time.sleep(duration)
    stop()
    print("Turned left {}°.".format(degree))

def pid_control():
    """
    Implement PID control for the robot.
    This function will be called repeatedly in a loop.
    """
    # Implement PID control here.
    
# Example usage:
if __name__ == '__main__':
    try:
        init()
        forward()
        time.sleep(2)
        stop()
        turn_right(90)
        time.sleep(1)
        backward()
        time.sleep(2)
        stop()
        turn_left(90)
    except KeyboardInterrupt:
        stop()
        print("Exiting program.")
