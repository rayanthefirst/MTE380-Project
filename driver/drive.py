#!/usr/bin/env python3
from gpiozero import Motor, RotaryEncoder
from time import sleep, time
import math
# Setup motor drivers.
left_motor = Motor(forward=14, backward=15)
right_motor = Motor(forward=12, backward=13)

# Setup encoders – update the GPIO pins as needed.
# Here we use a RotaryEncoder for each motor.
left_encoder = RotaryEncoder(a=9, b=10, max_steps=0)
right_encoder = RotaryEncoder(a=17, b=18, max_steps=0)

SPEED = 0.10
TURN_SPEED = 0.15
K_differential = 0.3

def drive(forward=True):
    """
    Drive the robot in a straight line.
    For forward motion: left motor goes forward and right motor goes backward.
    For backward motion, the directions are reversed.
    """
    if forward:
        left_motor.forward(speed=SPEED)
        right_motor.backward(speed=SPEED)
        # print("Driving forward.")
    else:
        left_motor.backward(speed=SPEED)
        right_motor.forward(speed=SPEED)
        # print("Driving backward.")

def stop():
    """Stop both motors."""
    left_motor.stop()
    right_motor.stop()
    # print("Motors stopped.")

def turn(turn_right=True, error=0):
    if turn_right:
        right_motor_speed = TURN_SPEED * ((K_differential * error) / 160)
        left_motor_speed  = TURN_SPEED
        # print("motor speed, right turn :", right_motor_speed)

    else:
        left_motor_speed = TURN_SPEED * ((K_differential * error) / 160)
        right_motor_speed  = TURN_SPEED
        # print("motor speed, left turn :", left_motor_speed)
       
    left_motor.forward(speed=left_motor_speed)
    right_motor.backward(speed=right_motor_speed)


"""
Test 1
63 cm 
time: 2.58388 s
left encoder steps: 2649
right encoder steps: 2618


left constant = 42.048 encoder/cm
right constant = 41.555 encoder/cm
use smaller constant since the encoders measure at different points


"""
def determine_constants():
    """
    Determine the encoder counts per degree of turn for calibration.
    This function is used to experimentally determine the encoder counts per degree of turn.
    """
    try:
        startTime = time()
        drive(forward=True) 
        while True:
            print("Left encoder steps:", left_encoder.steps)
            print("Right encoder steps:", right_encoder.steps)
            sleep(1)
    except KeyboardInterrupt:
        stopTime = time()
        stop()
        print("Stopping the motors...")
    finally:
        elapsedTime = stopTime - startTime
        print("Elapsed time:", elapsedTime)
        print("Left encoder steps:", left_encoder.steps)
        print("Right encoder steps:", right_encoder.steps)
        stop()


RIGHT_ENCODER_CONSTANT = 41.555
LEFT_ENCODER_CONSTANT = 42.048

def test_encoder_const():
    """
    Test the encoder constants for the left and right motors.
    """
    drive(forward=True)
    try:
        while right_encoder.steps < 63 * RIGHT_ENCODER_CONSTANT:
            print("Left encoder steps:", left_encoder.steps)
            print("Right encoder steps:", right_encoder.steps)
            sleep(1)
    except KeyboardInterrupt:
        stop()
        print("Stopping the motors.")
    finally:
        stop()
        print("Left encoder steps:", left_encoder.steps)
        print("Right encoder steps:", right_encoder.steps)



def test_spin():
    startTime = time()
    left_motor.forward(speed=SPEED)
    right_motor.forward(speed=SPEED)
    while time() - startTime <= 2:
        pass

    stop()


def sigmoid(x):
    return 1 / (1 + math.exp(-x))
