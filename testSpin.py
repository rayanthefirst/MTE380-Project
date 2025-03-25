from camera.camera import Camera
from driver.drive import stop
from gpiozero import Motor
import threading
from time import sleep

# Access motor pins directly
left_motor = Motor(forward=14, backward=15)
right_motor = Motor(forward=12, backward=13)

# Start red detection in a thread
cam = Camera(camera_id=0)
cameraThread = threading.Thread(target=cam.start_detection, kwargs={"display": False})
cameraThread.start()

print("Spinning in place (clockwise) until red line is detected...")

try:
    while not cam.isRedLineDetected:
        left_motor.backward(speed=0.1)
        right_motor.forward(speed=0.1)
        sleep(0.2)

    stop()
    print("Red line detected! Stopped.")

except KeyboardInterrupt:
    print("Interrupted. Stopping motors.")
    stop()

finally:
    stop()
