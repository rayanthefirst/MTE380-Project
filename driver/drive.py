import time

import RPi.GPIO as GPIO

# Configure GPIO pins for the motor driver.
# Adjust these pin numbers based on your wiring.
FORWARD_PIN = 17
BACKWARD_PIN = 27

def init():
    """Initialize Raspberry Pi GPIO settings."""
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FORWARD_PIN, GPIO.OUT)
    GPIO.setup(BACKWARD_PIN, GPIO.OUT)


def forward():
    """Drive the motor forward."""
    GPIO.output(FORWARD_PIN, GPIO.HIGH)
    GPIO.output(BACKWARD_PIN, GPIO.LOW)
    print("Motor running forward.")


def backward():
    """Drive the motor backward."""
    GPIO.output(FORWARD_PIN, GPIO.LOW)
    GPIO.output(BACKWARD_PIN, GPIO.HIGH)
    print("Motor running backward.")


def stop():
    """Stop the motor."""
    GPIO.output(FORWARD_PIN, GPIO.LOW)
    GPIO.output(BACKWARD_PIN, GPIO.LOW)
    print("Motor stopped.")


# Calibration constant: adjust this value until the turning angle is accurate.
TURN_TIME_MULTIPLIER = 0.01  # seconds per degree

def turn_right(degree):
    """Turn right by the specified degree.
    The turning is achieved by running the motor in forward direction
    for a period proportional to the degree.
    """
    turn_duration = degree * TURN_TIME_MULTIPLIER
    forward()
    time.sleep(turn_duration)
    stop()

def turn_left(degree):
    """Turn left by the specified degree.
    The turning is achieved by running the motor in backward direction
    for a period proportional to the degree.
    """
    turn_duration = degree * TURN_TIME_MULTIPLIER
    backward()
    time.sleep(turn_duration)
    stop()
