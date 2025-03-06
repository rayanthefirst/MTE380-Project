from camera.camera import Camera
from driver.drive import *
# camera = Camera()
# camera.initCamera()
# camera.start_detection()



# init()
# forward()
# time.sleep(2)
# stop()
# time.sleep(2)
# backward()
# time.sleep(2)



#!/usr/bin/env python3
import pigpio
import time

# Define motor control pins (GPIO numbers)
IN1 = 14  # Connected to IN1 on the L298N
IN2 = 15  # Connected to IN2 on the L298N

# Initialize pigpio and check connection
pi = pigpio.pi()
if not pi.connected:
    print("Could not connect to pigpio daemon!")
    exit()

# Set the motor control pins as outputs
pi.set_mode(IN1, pigpio.OUTPUT)
pi.set_mode(IN2, pigpio.OUTPUT)

def motor_forward():
    """Run motor forward (assumes 5V on ENA for 1000 RPM)"""
    pi.write(IN1, 1)
    pi.write(IN2, 0)

def motor_backward():
    """Run motor backward (assumes 5V on ENA for 1000 RPM)"""
    pi.write(IN1, 0)
    pi.write(IN2, 1)

def motor_stop():
    """Stop the motor"""
    pi.write(IN1, 0)
    pi.write(IN2, 0)

def main():
    try:
        while True:
            command = input("Enter command (1 = forward, 2 = backward, 0 = stop): ").strip()
            if command == "1":
                motor_forward()
                print("Motor running forward at 1000 RPM.")
            elif command == "2":
                motor_backward()
                print("Motor running backward at 1000 RPM.")
            elif command == "0":
                motor_stop()
                print("Motor stopped.")
            else:
                print("Invalid input. Please enter 1, 2, or 0.")
    except KeyboardInterrupt:
        print("Exiting program.")
    finally:
        motor_stop()
        pi.stop()

if __name__ == '__main__':
    main()
