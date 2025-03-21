
from camera.camera import Camera
from threading import Thread
from driver.drive import *

cam = Camera(camera_id=0)
cameraProcess = Thread(target=cam.start_detection, kwargs={"display": False})
cameraProcess.start()

error_threshold = 50

while True:
    if cam.isRedLineDetected:
        if abs(cam.curr_error) < error_threshold:
            # If error is small, drive forward.
            print("Error small; driving forward.")
            drive(forward=True)
        else:
            # print("Error large; adjusting turn.")
            # Calculate turn angle proportional to the error (limit to 30° maximum).
            if cam.curr_error > 0:
                # If error is positive, the red line is to the right.
                print("Red line detected to the right.")
                turn(turn_right=True, error=abs(cam.curr_error))
            else:
                # If error is negative, the red line is to the left.
                print("Red line detected to the left.")
                turn(turn_right=False, error=abs(cam.curr_error))
    else:
        # No red detected; stop the motors.
        stop()


