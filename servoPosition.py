
from gpiozero import Servo
from signal import pause
import time


left_servo = Servo(26, min_pulse_width=0.0005, max_pulse_width=0.0025)
right_servo = Servo(20, min_pulse_width=0.0005, max_pulse_width=0.0025)


print("Monitoring servo positions... (press Ctrl+C or q in window to quit)")

try:
    while True:
        left_pos = left_servo.value  # range: -1 (min) to 1 (max)
        right_pos = right_servo.value
        print(f"Left Servo: {left_pos:.2f} | Right Servo: {right_pos:.2f}")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nMonitoring stopped.")