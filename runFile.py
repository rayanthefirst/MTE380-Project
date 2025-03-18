
from camera.camera import Camera
from threading import Thread
from time import sleep
from driver.drive import *
cam = Camera(camera_id=1)
# cam.start_detection(display=True)
cameraProcess = Thread(target=cam.start_detection, kwargs={"display": False})
cameraProcess.start()
Kp = 0.1
Ka = 0.1
error_threshold = 10

while True:
    if cam.isRedLineDetected:
        if abs(cam.curr_error) < error_threshold:
            # If error is small, drive forward.
            drive(forward=True)
        else:
            # Calculate turn angle proportional to the error (limit to 30° maximum).
            turn_angle = min(30, Kp * abs(cam.curr_error))
            if cam.curr_error > 0:
                # If error is positive, the red line is to the right.
                # Turn right to adjust.
                pivot_turn(turn_right=True, degree=turn_angle)
            else:
                # If error is negative, the red line is to the left.
                # Turn left to adjust.
                pivot_turn(turn_right=False, degree=turn_angle)
    else:
        # No red detected; stop the motors.
        stop()
    sleep(0.5)





