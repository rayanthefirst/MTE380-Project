from gpiozero import Servo
from time import sleep

# Define the servo pin (Change GPIO17 if using a different pin)
servo = Servo(3, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)

# Move servo to 90 degrees
servo.mid()  
print("Servo moved to 90 degrees")
sleep(2)  # Hold position for 2 seconds

# Cleanup
servo.value = None  # Release the servo
print("Servo released")
