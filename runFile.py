#!/usr/bin/env python3
# from gpiozero import Motor
import time
from threading import Thread
from camera.camera import Camera

# Set up the motors.
# GPIO pin 14 is connected to IN1 (forward) for motor (left side)
# GPIO pin 15 is connected to IN2 (backward) for motor (left side)
# GPIO pin 12 is connected to IN1 (forward) for motor2 (right side)
# GPIO pin 13 is connected to IN2 (backward) for motor2 (right side)
# The enable pin (ENA) is hard-wired to 5V for full speed.
# motor = Motor(forward=14, backward=15)
# motor2 = Motor(forward=12, backward=13)

SPEED = 0.5
TURN_TIME = 1  # seconds; adjust this value so that the pivot rotates 90°
camera = Camera()
camera.initCamera()
thread = Thread(target=camera.start_detection, args=(True,))


def main():
    # Start the camera thread.
    thread.start()
    while camera.isRedLineDetected == False:
        time.sleep(1)


    demo()




def demo():

    print("Motor Control Script: Running timed sequence")
    
    # Run forward for 5 seconds.
    # (Forward: left wheel physical forward via motor.forward(),
    #  right wheel physical forward via motor2.backward())
    print("Running forward for 5 seconds...")
    # motor.forward(speed=SPEED)
    # motor2.backward(speed=SPEED)
    # time.sleep(5)
    # motor.stop()
    # motor2.stop()
    # time.sleep(1)
    
    # Run backward for 5 seconds.
    # (Backward: left wheel physical backward via motor.backward(),
    #  right wheel physical backward via motor2.forward())
    print("Running backward for 5 seconds...")
    # motor.backward(speed=SPEED)
    # motor2.forward(speed=SPEED)
    # time.sleep(5)
    # motor.stop()
    # motor2.stop()
    # time.sleep(1)
    
    # --- First pivot: Turn right 90° and return ---
    # To pivot right (clockwise), we want:
    #   left wheel: physical forward  (motor.forward())
    #   right wheel: physical backward (motor2.forward())
    print("Turning right 90°...")
    # motor.forward(speed=SPEED)
    # motor2.forward(speed=SPEED)
    # time.sleep(TURN_TIME)
    # motor.stop()
    # motor2.stop()
    # time.sleep(1)
    
    # Now, return to the original orientation by pivoting left 90°.
    # To pivot left (counterclockwise), we want:
    #   left wheel: physical backward (motor.backward())
    #   right wheel: physical forward  (motor2.backward())
    print("Returning to original orientation from right turn...")
    # motor.backward(speed=SPEED)
    # motor2.backward(speed=SPEED)
    # time.sleep(TURN_TIME)
    # motor.stop()
    # motor2.stop()
    # time.sleep(1)
    
    # --- Second pivot: Turn left 90° and return ---
    # To pivot left (counterclockwise), we use the same command as above:
    print("Turning left 90°...")
    # motor.backward(speed=SPEED)
    # motor2.backward(speed=SPEED)
    # time.sleep(TURN_TIME)
    # motor.stop()
    # motor2.stop()
    # time.sleep(1)
    
    # Return to original orientation by pivoting right 90°.
    print("Returning to original orientation from left turn...")
    # motor.forward(speed=SPEED)
    # motor2.forward(speed=SPEED)
    # time.sleep(TURN_TIME)
    # motor.stop()
    # motor2.stop()
    # time.sleep(1)
    
    print("Sequence complete.")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting program.")
        motor.stop()
        motor2.stop()
