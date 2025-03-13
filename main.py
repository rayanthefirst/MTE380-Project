from gpiozero import AngularServo
from time import sleep

# Define the servo on GPIO 3 (which corresponds to physical pin 5 on the Raspberry Pi)
servo = AngularServo(2, min_angle=0, max_angle=180, min_pulse_width=0.0006, max_pulse_width=0.0024)

def move_servo_90():
    print("Moving servo to 90 degrees")
    servo.angle = 90
    sleep(3)  # Allow time for the servo to reach the target position
    servo.angle = 0  # Reset the servo to 0 degrees
    sleep(3)
# Move the servo
while True:
    move_servo_90()
