import RPi.GPIO as GPIO
import time

# Configuration
servo_pin = 18         # GPIO pin number (using BCM numbering)
frequency = 50         # Servo PWM frequency in Hz

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# Create PWM instance with the desired frequency
pwm = GPIO.PWM(servo_pin, frequency)
pwm.start(2.5)  # Starting duty cycle (2.5% for 0 degrees on many servos)

def set_angle(angle):
    # Convert the angle to duty cycle:
    # duty_cycle = (angle / 18) + 2.5 is a common conversion formula
    duty_cycle = (angle / 18.0) + 2.5
    pwm.ChangeDutyCycle(duty_cycle)

try:
    while True:
        print("Moving servo to 90 degrees")
        set_angle(90)
        time.sleep(0.5)
        print("Moving servo back to 0 degrees")
        set_angle(0)
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    GPIO.cleanup()
