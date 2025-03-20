
from camera.camera import Camera
from threading import Thread
from driver.drive import *
from utils import scale_input

# SPEED IS RESTRICTED BETWEEN 0 AND 1
# From voltage test
MAX_SPEED = 0.6

# From straight line test
error_threshold = 50

cam = Camera(camera_id=0)
cameraProcess = Thread(target=cam.start_detection, kwargs={"display": True})
cameraProcess.start()

integral = 0
derivative = 0
curr_error = 0
prev_error = 0
dt = 1/cam.fps

max_error = cam.width/2
max_derivative = cam.width/dt

kp = 10^-5
ki = 0
kd = 0

while True:
    if cam.isRedLineDetected:
        prev_error = curr_error
        curr_error = cam.curr_error

        if abs(curr_error) > error_threshold:
            print("Error large; adjusting turn.")
            integral += curr_error * dt
            derivative = (curr_error - prev_error) / dt

            p_out = kp * curr_error
            i_out = ki * integral
            d_out = kd * derivative
            output = p_out + i_out + d_out

            # Scale output to voltage
            speedDelta = min(MAX_SPEED / 2, scale_input(output, max_error))

            # Adjust PID Speed for right and left
            if curr_error > 0:
                # If error is positive, turn right
                speed_left = (MAX_SPEED/2) + speedDelta
                speed_right = (MAX_SPEED/2) - speedDelta
            else:
                # If error is negative, turn left
                speed_left = (MAX_SPEED/2) - speedDelta
                speed_right = (MAX_SPEED/2) + speedDelta
            print("Speed left: ", speed_left)
            print("Speed right: ", speed_right)

            drive(speedLeft=speed_left, speedRight=speed_right)
            
        else:
            integral = 0
            derivative = 0
            # If error is small, drive forward.
            drive(speedLeft=(MAX_SPEED/2), speedRight=(MAX_SPEED/2), forward=True)
            print('speed left: ', (MAX_SPEED/2))    
        
    else:
        # No red detected; stop the motors.
        stop()