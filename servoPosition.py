
from gpiozero import Servo
from signal import pause
import time


left_servo = Servo(26)
right_servo = Servo(20)

left_servo.value = 0  # no command yet
right_servo.value = 0

print("Monitoring servo positions... (press Ctrl+C or q in window to quit)")

try:
    while True:
        left_input = input("Enter position for left servo (-1 to 1): ")
        right_input = input("Enter position for right servo (-1 to 1): ")
        try:
            left_pos = float(left_input)
            right_pos = float(right_input)
            if -1 <= left_pos <= 1 and -1 <= right_pos <= 1:
                left_servo.value = left_pos
                right_servo.value = right_pos
            else:
                print("Invalid input. Please enter values between -1 and 1.")

        except ValueError:
            print("Invalid input. Please enter numeric values.")

        left_pos = left_servo.value  # range: -1 (min) to 1 (max)
        right_pos = right_servo.value
        print(f"Left Servo: {left_pos} | Right Servo: {right_pos}")

        time.sleep(0.5)
except KeyboardInterrupt:
    print("\nMonitoring stopped.")