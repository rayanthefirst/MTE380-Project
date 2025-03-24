
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
        left_pos = left_servo.value  # range: -1 (min) to 1 (max)
        right_pos = right_servo.value
        print(f"Left Servo: {left_pos} | Right Servo: {left_pos}")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nMonitoring stopped.")