from gpiozero import AngularServo
from time import sleep

# Define the servo on GPIO 3 (which corresponds to physical pin 5 on the Raspberry Pi)
servo = AngularServo(3, min_angle=0, max_angle=180)

def move_servo_90():
    print("Moving servo to 90 degrees")
    servo.angle = 90
    sleep(0.5)  # Allow time for the servo to reach the target position

# Move the servo
while True:
    move_servo_90()
