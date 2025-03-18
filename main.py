#!/usr/bin/env python3
import time
import cv2 as cv
import numpy as np

# Import the Camera class from your camera module.
# Ensure that the file "camera.py" is in the same directory or in your PYTHONPATH.
from camera.camera import Camera

# Import motor commands from your motor module.
# Ensure that the file "motor.py" (with the provided motor code) is in the same directory.
import driver.drive as motor

def main():
    # Initialize the motors.
    motor.init()
    
    # Create a Camera instance.
    cam = Camera()
    
    # Define control parameters.
    error_threshold = 10  # pixels; error less than this will cause the car to drive forward
    Kp = 0.1  # Proportional gain: degrees per pixel of error (adjust as needed)
    
    try:
        while True:
            # Capture a frame from the camera.
            ret, frame = cam.cap.read()
            if not ret:
                print("Failed to capture frame")
                break

            # Resize frame to a square (480x480) for consistency.
            frame = cv.resize(frame, (480, 480))
            
            # Convert the frame from BGR to HSV color space.
            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            
            # Step 1: Create masks for red pixels (red spans two hue ranges).
            mask1 = cv.inRange(hsv, cam.red_lower, cam.red_upper)
            mask2 = cv.inRange(hsv, cam.red_lower_2, cam.red_upper_2)
            mask = cv.bitwise_or(mask1, mask2)
            
            # Step 2: Clean up the mask with morphological operations.
            kernel = np.ones((3, 3), np.uint8)
            mask = cv.erode(mask, kernel, iterations=5)
            mask = cv.dilate(mask, kernel, iterations=9)
            
            # Step 3: Find contours in the mask.
            contours, hierarchy = cv.findContours(mask.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            
            # Initialize error and detection flag.
            error = 0
            cam.isRedLineDetected = False
            
            # If any red regions are detected...
            if contours:
                cam.isRedLineDetected = True
                
                # If there's only one contour, choose it; otherwise, select the bottom-most contour.
                if len(contours) == 1:
                    blackbox = cv.minAreaRect(contours[0])
                else:
                    candidates = []
                    for idx, cnt in enumerate(contours):
                        box = cv.minAreaRect(cnt)
                        (x_center, y_center), (w, h), angle = box
                        # Use the y-coordinate (vertical position) for candidate selection.
                        candidates.append((y_center, idx, x_center, y_center))
                    candidates = sorted(candidates, key=lambda x: x[0])
                    # Choose the candidate with the highest y value (i.e. bottom-most).
                    _, chosen_idx, x_center, y_center = candidates[-1]
                    blackbox = cv.minAreaRect(contours[chosen_idx])
                
                # Unpack the bounding box.
                (x_center, y_center), (w, h), ang = blackbox

                # Adjust the angle for consistency.
                if ang < -45:
                    ang = 90 + ang
                if w < h and ang > 0:
                    ang = (90 - ang) * -1
                if w > h and ang < 0:
                    ang = 90 + ang

                # Calculate error as the difference between the contour’s center and the frame center.
                frame_center_x = frame.shape[1] // 2
                error = int(x_center - frame_center_x)
                
                # Draw the bounding box on the frame.
                box_pts = cv.boxPoints(blackbox)
                box_pts = np.int32(box_pts)
                if box_pts.size > 0:
                    cv.drawContours(frame, [box_pts], 0, (0, 0, 255), 2)
                
                # Display angle and error information.
                cv.putText(frame, f"Angle: {int(ang)}", (10, 40),
                           cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv.putText(frame, f"Error: {error}", (10, 80),
                           cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                # Draw a vertical line at the detected x-coordinate.
                cv.line(frame, (int(x_center), 0), (int(x_center), frame.shape[0]), (255, 0, 0), 2)
            else:
                cam.isRedLineDetected = False
            
            # Display the processed frame.
            cv.imshow("Red Line Contour Tracking", frame)
            
            # --- Motor Control Logic ---
            if cam.isRedLineDetected:
                if abs(error) < error_threshold:
                    # If error is small, drive forward.
                    motor.forward()
                else:
                    # Calculate turn angle proportional to the error (limit to 30° maximum).
                    turn_angle = min(30, Kp * abs(error))
                    if error > 0:
                        # If error is positive, the red line is to the right.
                        # Turn right to adjust.
                        motor.turn_right(turn_angle)
                    else:
                        # If error is negative, the red line is to the left.
                        # Turn left to adjust.
                        motor.turn_left(turn_angle)
            else:
                # No red detected; stop the motors.
                motor.stop()
            # --------------------------------
            
            # Break the loop if the 'q' key is pressed.
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
            
            # Small delay for the control loop.
            time.sleep(0.1)
    finally:
        # Release the camera and close all windows.
        cam.cap.release()
        cv.destroyAllWindows()

if __name__ == '__main__':
    main()
