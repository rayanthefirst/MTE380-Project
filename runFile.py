#!/usr/bin/env python3
from gpiozero import Motor
import time

# Set up the motor.
# GPIO pin 14 is connected to IN1 (forward)
# GPIO pin 15 is connected to IN2 (backward)
# The enable pin (ENA) is hard-wired to 5V for full speed.
motor = Motor(forward=14, backward=15)
motor2 = Motor(forward=12, backward=13)

SPEED=0.5

def main():
    print("Motor Control Script")
    print("Commands:")
    print("  1: Run motor forward at ~1000 RPM")
    print("  2: Run motor backward at ~1000 RPM")
    print("  0: Stop motor")
    
    while True:
        cmd = input("Enter command (0, 1, 2): ").strip()
        if cmd == "1":
            print("Running motor forward...")
            motor.forward(speed=SPEED)  # Runs at full speed
            motor2.backward(speed=SPEED)
        elif cmd == "2":
            print("Running motor backward...")
            motor.backward(speed=SPEED)  # Runs at full speed in reverse
            motor2.forward(speed=SPEED)
        elif cmd == "0":
            print("Stopping motor...")
            motor.stop()
            motor2.stop()
        else:
            print("Invalid command. Please enter 0, 1, or 2.")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting program.")
        motor.stop()
