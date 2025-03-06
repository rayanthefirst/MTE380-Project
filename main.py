import cv2 as cv
import time
from camera.camera import Camera

# filepath: /C:/Users/rayan/Desktop/MTE 380 Project/main.py

import driver.drive as drive

# Threshold for considering that enough red is detected.
RED_THRESHOLD = 1000

def main():
    # Initialize GPIO for motors.
    drive.init()
    
    # Initialize and configure the camera.
    cam = Camera()
    cam.initCamera()

    while True:
        ret, frame = cam.cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        # Resize frame for consistency.
        frame = cv.resize(frame, (480, 480))

        # Convert frame to HSV.
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # Create masks for red color using camera's predefined ranges.
        mask1 = cv.inRange(hsv, cam.red_lower, cam.red_upper)
        mask2 = cv.inRange(hsv, cam.red_lower_2, cam.red_upper_2)
        mask = cv.bitwise_or(mask1, mask2)

        # Decide if a red line is present based on non-zero pixels in the mask.
        red_pixel_count = cv.countNonZero(mask)
        if red_pixel_count > RED_THRESHOLD:
            drive.forward()
        else:
            drive.stop()

        # Process frame for detection visualization.
        frame = cam.detect_red_line(frame)
        cv.imshow('Red Line Detection', frame)

        # Break loop on 'q' key press.
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cam.cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()