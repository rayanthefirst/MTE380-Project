#!/usr/bin/env python3
from gpiozero import Motor, RotaryEncoder
from time import sleep, time

# Setup motor drivers.
left_motor = Motor(forward=14, backward=15)
right_motor = Motor(forward=12, backward=13)

# Setup encoders – update the GPIO pins as needed.
# Here we use a RotaryEncoder for each motor.
left_encoder = RotaryEncoder(a=9, b=10, max_steps=0)
right_encoder = RotaryEncoder(a=17, b=18, max_steps=0)

SPEED = 0.25
# Calibration: encoder counts per degree of turn (experimentally determined).
ENCODER_COUNTS_PER_DEGREE = 0.1

def drive(forward=True):
    """
    Drive the robot in a straight line.
    For forward motion: left motor goes forward and right motor goes backward.
    For backward motion, the directions are reversed.
    """
    if forward:
        left_motor.forward(speed=SPEED)
        right_motor.backward(speed=SPEED)
        print("Driving forward.")
    else:
        left_motor.backward(speed=SPEED)
        right_motor.forward(speed=SPEED)
        print("Driving backward.")

def stop():
    """Stop both motors."""
    left_motor.stop()
    right_motor.stop()
    print("Motors stopped.")

def pivot_turn(turn_right=True, degree=90):
    """
    Perform a pivot turn using encoder feedback.
    
    For a right pivot turn, both motors run forward; for a left pivot turn, both run backward.
    The function waits until the encoder (using the left encoder in this example) registers 
    enough counts corresponding to the desired angle.
    """
    target = degree

    if turn_right:
        left_motor.forward(speed=SPEED/2)
        right_motor.forward(speed=(SPEED/4))
        sleep(0.5)
        direction = "right"
    else:
        left_motor.backward(speed=(SPEED/4))
        right_motor.backward(speed=SPEED/2)
        sleep(0.5)
        direction = "left"

    # Use one encoder (e.g., left) to track the turn.
    # while abs(left_encoder.steps) < target:
    #     sleep(0.001)

    print("Pivot turned {} {}°.".format(direction, degree))



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