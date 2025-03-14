from gpiozero import Motor, RotaryEncoder
from time import sleep

#!/usr/bin/env python3

# Set up the motor (adjust the GPIO pins as needed for your hardware)
motor = Motor(forward=17, backward=18)

# Set up the rotary encoder (adjust the GPIO pins and max_steps as needed)
encoder = RotaryEncoder(a=22, b=23, max_steps=100)

def main():
    try:
        while True:
            # Read the encoder position (number of steps)
            print("Encoder steps:", encoder.steps)
            
            # Example control: run the motor forward until 50 steps, then reverse
            if encoder.steps < 50:
                motor.forward()
            else:
                motor.backward()
                
            sleep(0.1)
    except KeyboardInterrupt:
        print("Stopping the motor...")
    finally:
        motor.stop()

if __name__ == '__main__':
    main()