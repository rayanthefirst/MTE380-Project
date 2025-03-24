from camera.camera import Camera
from driver.drive import drive, stop, turn
from driver.servo import open_arms, close_arms

import cv2
import numpy as np
import threading
from time import sleep

# Start red line detection
cam = Camera(camera_id=0)
cameraThread = threading.Thread(target=cam.start_detection, kwargs={"display": False})
cameraThread.start()

# Simplified color thresholds (HSV)
blue_lower = np.array([100, 100, 50])
blue_upper = np.array([130, 255, 255])


video = cv2.VideoCapture(0)
error_threshold = 25
lego_grabbed = False

while True:
    # Red line following logic
    if not lego_grabbed and cam.isRedLineDetected:
        if abs(cam.curr_error) < error_threshold:
            print("Following red line: driving forward.")
            drive(forward=True)
        else:
            if cam.curr_error > 0:
                print("Red line to the right. Turning right.")
                turn(turn_right=True, error=abs(cam.curr_error))
            else:
                print("Red line to the left. Turning left.")
                turn(turn_right=False, error=abs(cam.curr_error))
    elif not lego_grabbed:
        print("Red line lost. Stopping.")
        stop()

    # LEGO detection via color presence (blue + white in same frame)
    ret, frame = video.read()
    if not ret:
        continue

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)

    has_blue = cv2.countNonZero(blue_mask) > 20

    if has_blue and not lego_grabbed:
        print("Blue and white detected in frame — initiating LEGO pickup.")
        stop()
        open_arms()
        sleep(1)
        close_arms()
        lego_grabbed = True
        print("LEGO picked up.")

    # Manual exit option
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
