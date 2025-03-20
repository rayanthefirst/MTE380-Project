
from camera.camera import Camera
from threading import Thread
from driver.drive import *

cam = Camera(camera_id=0)
cameraProcess = Thread(target=cam.start_detection, kwargs={"display": False})
cameraProcess.start()

# From straight line test
error_threshold = 50

integral = 0
derivative = 0
curr_error = 0
prev_error = 0
dt = 1/cam.fps

kp = 0
ki = 0
kd = 0

while True:
    if cam.isRedLineDetected:
        prev_error = curr_error
        curr_error = cam.curr_error
        if abs(curr_error) > error_threshold:
            integral += curr_error * dt
            derivative = (curr_error - prev_error) / dt
            print("Error large; adjusting turn.")
            if curr_error > 0:
                # If error is positive, the red line is to the right.
                turn(turn_right=True, error=abs(curr_error), integral=integral, derivative=derivative)
            else:
                # If error is negative, the red line is to the left.
                turn(turn_right=False, error=abs(curr_error), integral=integral, derivative=derivative)
        else:
            integral = 0
            derivative = 0
            # If error is small, drive forward.
            drive(forward=True)
           
    else:
        # No red detected; stop the motors.
        stop()


