from camera.camera import Camera
from driver.drive import drive, stop
import threading
from time import sleep

# Start the camera detection thread
cam = Camera(camera_id=0)
cameraThread = threading.Thread(target=cam.start_detection, kwargs={"display": True})
cameraThread.start()

print("Spinning in place until red line is detected...")

try:
    while not cam.isRedLineDetected:
        drive(forward=True)  # Both wheels in opposite directions (defined in drive.py)
        sleep(0.2)  # Small delay to reduce CPU usage

    stop()
    print("Red line detected! Stopping spin.")

except KeyboardInterrupt:
    print("Interrupted. Stopping motors.")
    stop()

finally:
    stop()
