from gpiozero import Servo
from time import sleep

# Initialize servo on GPIO3 with pulse width calibration
servo = Servo(3, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)

# Move servo to 0° (minimum)
print("Moving servo to minimum (0 degrees)")
servo.min()
sleep(2)

# Move servo to 90° (middle)
print("Moving servo to middle (90 degrees)")
servo.mid()
sleep(2)

# Move servo to 180° (maximum)
print("Moving servo to maximum (180 degrees)")
servo.max()
sleep(2)

# Cleanup: Release the servo control
servo.value = None  
print("Servo released")
