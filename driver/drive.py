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

def drive(speedLeft, speedRight, forward=True):
    """
    Drive the robot in a straight line.
    For forward motion: left motor goes forward and right motor goes backward.
    For backward motion, the directions are reversed.
    """
    if forward:
        left_motor.forward(speed=speedLeft)
        right_motor.backward(speed=speedRight)
        # print("Driving forward.")
    else:
        left_motor.backward(speed=speedLeft)
        right_motor.forward(speed=speedRight)
        # print("Driving backward.")

def stop():
    """Stop both motors."""
    left_motor.stop()
    right_motor.stop()


# def find_line(time, highSpeed, lowSpeed):
#     drive(highSpeed, lowSpeed)
#     time.sleep(time)

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



def test_spin(speed):
    startTime = time()
    left_motor.forward(speed=speed)
    right_motor.forward(speed=speed)
    while time() - startTime <= 2:
        pass

    stop()




