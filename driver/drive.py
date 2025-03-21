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

SPEED = 0.11
TURN_SPEED = 0.11
kp = 0.3
kd = 0.25
ki = 0.1

last_error = 0.0
integral_error = 0.0
last_time = time()



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
    global last_error, last_time, integral_error
    current_time = time()
    dt = current_time - last_time
    if dt <= 0.000001:
        dt = 0.000001



    integral_error += error * dt
    # For a simple anti-windup, clamp the integral. Adjust clamp bounds as needed.
    integral_error = max(min(integral_error, 100), -100)

    derivative = (error - last_error) / dt
    control_output = (kp * error) + (kd * derivative) + (ki * integral_error)

    # Update "memory" for next iteration
    last_error = error
    last_time = current_time

    if turn_right:
        right_motor_speed = TURN_SPEED * (control_output / 160.0)
        left_motor_speed  = TURN_SPEED
    else:
        left_motor_speed  = TURN_SPEED * (control_output / 160.0)
        right_motor_speed = TURN_SPEED

    # Enforce some clamping if needed (to avoid negative or excessively large speeds)
    right_motor_speed = max(min(right_motor_speed, 1.0), 0.0)
    left_motor_speed  = max(min(left_motor_speed, 1.0), 0.0)

    left_motor.forward(speed=left_motor_speed)
    right_motor.backward(speed=right_motor_speed)


    # if turn_right:
    #     right_motor_speed = TURN_SPEED * ((kp * error) / 160)
    #     left_motor_speed  = TURN_SPEED
    #     # print("motor speed, right turn :", right_motor_speed)

    # else:
    #     left_motor_speed = TURN_SPEED * ((kp * error) / 160)
    #     right_motor_speed  = TURN_SPEED
        # print("motor speed, left turn :", left_motor_speed)
       
    # left_motor.forward(speed=left_motor_speed)
    # right_motor.backward(speed=right_motor_speed)


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
