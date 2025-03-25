from camera.camera import Camera
from driver.drive import drive, stop, turn, left_motor, right_motor
from driver.servo import open_arms, close_arms

import cv2
import numpy as np
import threading
from time import sleep

# Start red line detection in a separate thread
cam = Camera(camera_id=0)
cameraThread = threading.Thread(target=cam.start_detection, kwargs={"display": False})
cameraThread.start()

# HSV threshold for blue and green
blue_lower = np.array([100, 100, 50])
blue_upper = np.array([130, 255, 255])
green_lower = np.array([40, 50, 50])
green_upper = np.array([80, 255, 255])

# Load target shape masks
blue_target_mask = cv2.imread("blueTarget.png", cv2.IMREAD_GRAYSCALE)
blue_target_mask = cv2.resize(blue_target_mask, (100, 100))
_, blue_target_mask = cv2.threshold(blue_target_mask, 127, 255, cv2.THRESH_BINARY)

green_target_mask = cv2.imread("greenTarget.png", cv2.IMREAD_GRAYSCALE)
green_target_mask = cv2.resize(green_target_mask, (100, 100))
_, green_target_mask = cv2.threshold(green_target_mask, 127, 255, cv2.THRESH_BINARY)

error_threshold = 25
lego_grabbed = False

while True:
    # Red line following logic
    if cam.isRedLineDetected:
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
    else:
        print("Red line lost. Stopping.")
        stop()

    # Use shared frame for detection
    if cam.latest_frame is None:
        continue

    frame = cam.latest_frame.copy()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # --- BLUE Target Detection ---
    if not lego_grabbed:
        blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
        resized_blue = cv2.resize(blue_mask, (100, 100))
        blue_score = cv2.matchTemplate(resized_blue, blue_target_mask, cv2.TM_CCOEFF_NORMED)[0][0]

        if blue_score > 0.45:
            print(f"Blue shape match detected (score: {blue_score:.2f})")
            stop()
            sleep(1)
            close_arms()
            lego_grabbed = True

            cam.isRedLineDetected = False
            print("Rotating until red line is found...")
            while not cam.isRedLineDetected:
                left_motor.forward(speed=0.155)
                right_motor.forward(speed=0.080)
                sleep(0.5)
            stop()
            print("Red line reacquired. Resuming.")

        else:
            print(f"No blue match (score: {blue_score:.2f})")

    # --- GREEN Target Detection ---
    if lego_grabbed:
        green_mask = cv2.inRange(hsv, green_lower, green_upper)
        resized_green = cv2.resize(green_mask, (100, 100))
        green_score = cv2.matchTemplate(resized_green, green_target_mask, cv2.TM_CCOEFF_NORMED)[0][0]

        if green_score > 0.105:
            print(f"Green shape match detected (score: {green_score:.2f})")
            stop()
            sleep(0.5)

            print("Driving forward to drop location...")
            drive(forward=True)
            sleep(1.5)  # Increased from 1 to 2 seconds
            stop()
            sleep(0.5)

            print("Dropping LEGO...")
            open_arms()
            sleep(0.5)

            print("Backing up...")
            drive(forward=False)
            sleep(1.5)  # Adjust as needed
            stop()

            close_arms()
            lego_grabbed = False

            print("Drop-off complete. Waiting to reacquire red line naturally...")


        else:
            print(f"No green match (score: {green_score:.2f})")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
