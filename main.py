from camera.camera import Camera
from driver.drive import drive, stop, turn, left_motor, right_motor
from driver.servo import open_arms, close_arms

import cv2
import numpy as np
import threading
from time import sleep

cam = Camera(camera_id=0)
cameraThread = threading.Thread(target=cam.start_detection, kwargs={"display": False})
cameraThread.start()

blue_lower = np.array([100, 100, 50])
blue_upper = np.array([130, 255, 255])
green_lower = np.array([40, 50, 50])
green_upper = np.array([90, 255, 255])

target_mask = cv2.imread("blueTarget.png", cv2.IMREAD_GRAYSCALE)
target_mask = cv2.resize(target_mask, (100, 100))
_, target_mask = cv2.threshold(target_mask, 127, 255, cv2.THRESH_BINARY)

error_threshold = 25
lego_grabbed = False
dropoff_done = False

while True:
    if cam.latest_frame is None:
        continue

    frame = cam.latest_frame.copy()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    if not lego_grabbed:
        # ----- Red line following logic -----
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

        # ----- LEGO detection -----
        blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
        resized_blue_mask = cv2.resize(blue_mask, (100, 100))
        match_score = cv2.matchTemplate(resized_blue_mask, target_mask, cv2.TM_CCOEFF_NORMED)[0][0]

        if match_score > 0.45:
            print(f"Blue shape match detected (score: {match_score:.2f})")
            stop()
            sleep(1)
            close_arms()
            lego_grabbed = True
            cam.isRedLineDetected = False

            print("Rotating in place until red line is found...")
            while not cam.isRedLineDetected:
                left_motor.forward(speed=0.155)
                right_motor.forward(speed=0.080)
                sleep(0.5)

            stop()
            print("Red line reacquired. Resuming line following.")

        else:
            print(f"No shape match (score: {match_score:.2f})")

    elif lego_grabbed and not dropoff_done:
        # ----- GREEN drop-off logic -----
        green_mask = cv2.inRange(hsv, green_lower, green_upper)
        has_green = cv2.countNonZero(green_mask) > 0

        if has_green:
            print("Green detected! Executing drop-off sequence...")
            stop()
            sleep(1)
            drive(forward=True)
            sleep(1.5)
            stop()
            open_arms()
            sleep(1)
            drive(forward=False)
            sleep(1.5)
            stop()
            close_arms()
            sleep(1)
            dropoff_done = True
            cam.isRedLineDetected = False

            print("Rotating to reacquire red line...")
            while not cam.isRedLineDetected:
                left_motor.forward(speed=0.155)
                right_motor.forward(speed=0.080)
                sleep(0.5)

            stop()
            print("Red line reacquired. Resuming.")

    elif lego_grabbed and dropoff_done:
        # ----- Resume red line logic after drop-off -----
        if cam.isRedLineDetected:
            if abs(cam.curr_error) < error_threshold:
                drive(forward=True)
            else:
                turn(turn_right=(cam.curr_error > 0), error=abs(cam.curr_error))
        else:
            stop()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
