from camera.camera import Camera
from threading import Thread
from driver.drive import *

# SPEED IS RESTRICTED BETWEEN 0 AND 1
MAX_SPEED = 0.2

# From straight line test
error_threshold = 50

cam = Camera(camera_id=0)
cameraProcess = Thread(target=cam.start_detection, kwargs={"display": False})
cameraProcess.start()

integral = 0
derivative = 0
curr_error = 0
prev_error = 0
dt = 1 / cam.fps  # Time step based on camera frame rate

max_error = cam.width / 2

# PID Gains
kp = MAX_SPEED / max_error  # Proportional gain
ki = 0  # Keeping integral disabled for now
kd = 0.01  # Small derivative gain (tune this value)

while True:
    if cam.isRedLineDetected:
        prev_error = curr_error
        curr_error = cam.curr_error

        if abs(curr_error) > error_threshold:
            print("Error large; adjusting turn.")

            # Compute PID terms
            derivative = (curr_error - prev_error) / dt

            p_out = kp * curr_error
            d_out = kd * derivative
            output = p_out + d_out  # No integral term yet

            # Scale output to voltage
            speedDelta = min(MAX_SPEED / 2, abs(output))

            # Adjust PID Speed for right and left
            if curr_error > 0:
                # If error is positive, turn right
                speed_left = (MAX_SPEED / 2) + speedDelta
                speed_right = (MAX_SPEED / 2) - speedDelta
            else:
                # If error is negative, turn left
                speed_left = (MAX_SPEED / 2) - speedDelta
                speed_right = (MAX_SPEED / 2) + speedDelta

            drive(speedLeft=speed_left, speedRight=speed_right)
        else:
            derivative = 0
            drive(speedLeft=(MAX_SPEED / 2), speedRight=(MAX_SPEED / 2), forward=True)
    else:
        # No red detected; stop the motors.
        stop()
