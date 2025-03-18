
from camera.camera import Camera
from threading import Thread
from time import sleep
from driver.drive import *
cam = Camera(camera_id=0)
cameraProcess = Thread(target=cam.start_detection, kwargs={"display": False})
cameraProcess.start()
Kp = 1
Ka = 1
error_threshold = 10

while True:
    if cam.isRedLineDetected:
        print("Red line detected")
        
        if abs(cam.curr_error) < error_threshold:
            print("Error small; driving forward.")
            # If error is small, drive forward.
            drive(forward=True)
        else:
            print("Error large; adjusting turn.")
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
            print("HELLLOOOOO")
    # else:
    #     # No red detected; stop the motors.
    #     stop()
    sleep(0.5)





