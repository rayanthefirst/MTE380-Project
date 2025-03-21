
from camera.camera import Camera
from threading import Thread
from driver.drive import *
from utils import scale_input
import time

# SPEED IS RESTRICTED BETWEEN 0 AND 1
# From voltage test
MAX_SPEED = 0.2
speedScalar = 2

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
# dt = 0.32
max_error = cam.width/2
max_derivative = cam.width / dt
# max_derivative = cam.width/dt

kp = ((MAX_SPEED / speedScalar) / max_error) 
ki = 0
kd = ((MAX_SPEED / speedScalar)  / max_derivative)

max_der = 0

while True:
    if cam.isRedLineDetected:
        prev_error = curr_error
        curr_error = cam.curr_error

        if abs(curr_error) > error_threshold:
            # print("Error large; adjusting turn.")
            integral += curr_error * dt
            derivative = (curr_error - prev_error) / dt
            max_der = max(derivative, max_der)

            print("max der", max_der)

            p_out = kp * curr_error
            print("p_out", p_out)
            i_out = ki * integral
            print("i_out", i_out)
            d_out = kd * derivative
            print("d_out", d_out)
            output = p_out + i_out + d_out
            print("output" , output)
            # Scale output to voltage
            speedDelta = min(MAX_SPEED / speedScalar, abs(output))
            # speedDelta = abs(output)
            print("speedDelts", speedDelta)


            # Adjust PID Speed for right and left
            if curr_error > 0:
                # If error is positive, turn right
                speed_left = (MAX_SPEED/speedScalar) + speedDelta
                speed_right = (MAX_SPEED/speedScalar) - speedDelta
            else:
                # If error is negative, turn left
                speed_left = (MAX_SPEED/speedScalar) - speedDelta
                speed_right = (MAX_SPEED/speedScalar) + speedDelta
            # print("Speed left: ", speed_left)
            # print("Speed right: ", speed_right)

            drive(speedLeft=speed_left, speedRight=speed_right)
            
        else:
            while not cam.isRedLineDetected:
                if curr_error > 0:
                    # If error is positive, turn right
                    drive(speedLeft=(MAX_SPEED/(speedScalar*2)), speedRight=0, forward=True)

                else:
                    # If error is negative, turn left
                    drive(speedLeft=0, speedRight=(MAX_SPEED/(speedScalar * 2)), forward=True)
                # Reset PID values


            integral = 0
            derivative = 0
            # If error is small, drive forward.
            drive(speedLeft=(MAX_SPEED/speedScalar), speedRight=(MAX_SPEED/speedScalar), forward=True)
        
    else:
        # No red detected; stop the motors.

        stop()