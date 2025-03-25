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

# HSV threshold for blue
blue_lower = np.array([100, 100, 50])
blue_upper = np.array([130, 255, 255])

# Load the target shape (your bullseye top arc image)
target_mask = cv2.imread("blueTarget.png", cv2.IMREAD_GRAYSCALE)
target_mask = cv2.resize(target_mask, (100, 100))
_, target_mask = cv2.threshold(target_mask, 127, 255, cv2.THRESH_BINARY)

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

    # Use shared frame for LEGO detection
    if cam.latest_frame is None or lego_grabbed:
        continue

    frame = cam.latest_frame.copy()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)

    # Resize to match the target mask size
    resized_blue_mask = cv2.resize(blue_mask, (100, 100))

    # Compare with target shape
    match_score = cv2.matchTemplate(resized_blue_mask, target_mask, cv2.TM_CCOEFF_NORMED)[0][0]

    if match_score > 0.50:
        print(f"Blue shape match detected (score: {match_score:.2f})")
        stop()
        sleep(1)
        close_arms()
        lego_grabbed = True

        # Force red line detection to false to ensure spin loop triggers
        cam.isRedLineDetected = False

        print("Rotating in place until red line is found...")
        while not cam.isRedLineDetected:
            left_motor.forward(speed=0.2)
            right_motor.forward(speed=0.1)
            sleep(0.1)

        stop()
        print("Red line reacquired. Resuming line following.")

    else:
        print(f"No shape match (score: {match_score:.2f})")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
