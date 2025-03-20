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

prev_error = 0
dt = max(1 / cam.fps, 0.01)  # Prevent division by zero

max_error = cam.width / 2

# **New PID Gains**
kp = (MAX_SPEED / max_error) * 1.0  # Adjusted KP for smoother control
kd = 0.015  # Lower KD to reduce sudden braking

# **Speed Parameters**
MIN_SPEED_RATIO = 0.6  # Ensures the slow wheel is never too slow (60% of base speed)
MAX_SPEED_RATIO = 1.2  # Prevents over-speeding one wheel (120% of base speed)

while True:
    if cam.isRedLineDetected:
        curr_error = cam.curr_error

        if abs(curr_error) > error_threshold:
            print("Error large; adjusting turn.")

            # Compute PD terms
            derivative = (curr_error - prev_error) / dt if dt > 0 else 0

            p_out = kp * curr_error
            d_out = kd * derivative
            output = p_out + d_out  # No integral term

            # Scale output and limit how much one wheel can slow down
            speedDelta = min(MAX_SPEED * 0.3, abs(output))  # Reduce aggressiveness

            base_speed = MAX_SPEED * 0.8  # Lower base speed for better control
            speed_factor = 1 if curr_error > 0 else -1

            speed_left = base_speed * (1 + speed_factor * speedDelta)
            speed_right = base_speed * (1 - speed_factor * speedDelta)

            # **Ensure speed stays within limits**
            speed_left = max(MIN_SPEED_RATIO * base_speed, min(MAX_SPEED_RATIO * base_speed, speed_left))
            speed_right = max(MIN_SPEED_RATIO * base_speed, min(MAX_SPEED_RATIO * base_speed, speed_right))

            drive(speedLeft=speed_left, speedRight=speed_right)
        else:
            drive(speedLeft=(MAX_SPEED * 0.8), speedRight=(MAX_SPEED * 0.8), forward=True)
    else:
        stop()

    prev_error = curr_error  # Update previous error for next loop
