#!/usr/bin/env python3
from gpiozero import Motor
import time
from threading import Thread
from camera.camera import Camera

# Set up the motors.
motor = Motor(forward=14, backward=15)  # Left motor
motor2 = Motor(forward=12, backward=13)  # Right motor

SPEED = 0.5  # Base speed for forward movement
Kp = 0.3  # Proportional gain for correction (adjust for tuning)
STOP_DELAY = 0.2  # Delay before stopping if red is lost
camera = Camera()
camera.initCamera()
thread = Thread(target=camera.start_detection, args=(True,))


def main():
    # Start the camera thread.
    thread.start()
    
    print("Waiting for red line detection...")

    while True:
        if camera.isRedLineDetected:
            error = camera.getRedLinePositionError()  # Get deviation from center
            adjust_motor_speed(error)
        else:
            stop_motors()

        time.sleep(0.1)  # Small delay to avoid excessive CPU usage


def adjust_motor_speed(error):
    """Adjusts motor speeds based on deviation from the red line center."""
    correction = Kp * error  # Calculate speed adjustment

    left_speed = SPEED - correction  # Reduce left speed if veering right
    right_speed = SPEED + correction  # Increase right speed if veering right

    # Ensure motor speeds stay in range (0 to 1)
    left_speed = max(0, min(1, left_speed))
    right_speed = max(0, min(1, right_speed))

    print(f"Error: {error} | Left Speed: {left_speed:.2f} | Right Speed: {right_speed:.2f}")

    motor.forward(speed=left_speed)
    motor2.backward(speed=right_speed)


def stop_motors():
    """Stops motors when red is lost."""
    print("Red line lost, stopping...")
    motor.stop()
    motor2.stop()
    time.sleep(STOP_DELAY)  # Small delay before checking again


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting program.")
        motor.stop()
        motor2.stop()
