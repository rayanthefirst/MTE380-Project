from camera.camera import Camera
from driver.drive import left_motor, right_motor, stop
import threading
from time import sleep

# Start camera red line detection
cam = Camera(camera_id=0)
cameraThread = threading.Thread(target=cam.start_detection, kwargs={"display": False})
cameraThread.start()

print("Spinning in place (clockwise) until red line is detected...")

try:
    while not cam.isRedLineDetected:
        # In-place clockwise spin: left motor backward, right motor forward
        left_motor.forward(speed=0.2)
        right_motor.forward(speed=0.1)
        sleep(0.1)

    stop()
    print("Red line detected! Stopped.")

except KeyboardInterrupt:
    print("Interrupted. Stopping.")
    stop()

finally:
    stop()
