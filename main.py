from gpiozero import DigitalOutputDevice
from time import sleep

# Define the GPIO pin (GPIO 3 corresponds to physical pin 5 on the Raspberry Pi)
servo_pin = DigitalOutputDevice(3)

def move_servo_90():
    print("Moving servo to 90 degrees")
    # Approximate a 90-degree pulse (1.5ms high signal)
    servo_pin.on()
    sleep(0.0015)  # 1.5ms pulse
    servo_pin.off()
    sleep(0.02)    # 20ms delay (standard servo refresh rate)

# Move the servo
move_servo_90()
