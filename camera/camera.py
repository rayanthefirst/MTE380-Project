import cv2 as cv
import numpy as np
import math
import time

class Camera:
    def __init__(self):
        # You can keep initCamera() if you prefer to call that separately
        # but I'll just do the capture initialization here for clarity.
        print("Camera initialized")
        self.cap = cv.VideoCapture(0)
        
        # Set resolution
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv.CAP_PROP_FPS, 30)

        # Define HSV range for red color – same as your original code
        self.red_lower = np.array([0, 100, 100])
        self.red_upper = np.array([10, 255, 255])
        self.red_lower_2 = np.array([160, 100, 100])
        self.red_upper_2 = np.array([180, 255, 255])
        
        self.isRedLineDetected = False
        self.x_last = 0
        self.y_last = 0

    def start_detection(self, display=False):
        """
        Continuously capture frames and detect + track the red line contours.
        """
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to capture frame")
                break

            # Optionally resize to a square if you want consistency
            frame = cv.resize(frame, (480, 480))

            # Convert BGR -> HSV
            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

            # Step 1: Create a mask for red pixels
            mask1 = cv.inRange(hsv, self.red_lower, self.red_upper)
            mask2 = cv.inRange(hsv, self.red_lower_2, self.red_upper_2)
            mask = cv.bitwise_or(mask1, mask2)

            # Step 2: Morphological ops to clean up the mask
            # (Adjust iterations, kernel size if needed)
            kernel = np.ones((3,3), np.uint8)
            mask = cv.erode(mask, kernel, iterations=5)
            mask = cv.dilate(mask, kernel, iterations=9)

            # Step 3: Find contours in the cleaned-up mask
            contours, hierarchy = cv.findContours(
                mask.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE
            )

            # Step 4: If we found any contours, pick one and analyze it
            if contours:
                self.isRedLineDetected = True

                # If there's just one contour, use it
                if len(contours) == 1:
                    blackbox = cv.minAreaRect(contours[0])
                else:
                    # Otherwise, we pick the bottom-most or largest
                    # (the tutorial does a 'bottom-most' approach)
                    candidates = []
                    off_bottom = 0
                    for idx, cnt in enumerate(contours):
                        box = cv.minAreaRect(cnt)
                        (x_min, y_min), (w_min, h_min), angle = box
                        # We’ll look at the top-left corner of the box
                        # or just use the center’s y_min
                        # to figure out if it’s near the bottom
                        candidates.append((y_min, idx, x_min, y_min))

                    # Sort by y_min (vertical position) ascending
                    candidates = sorted(candidates, key=lambda x: x[0])
                    # We'll take the bottom-most by picking the highest y_min
                    # which is the last in the sorted list
                    _, chosen_idx, x_min, y_min = candidates[-1]
                    blackbox = cv.minAreaRect(contours[chosen_idx])

                # Extract bounding box info
                (x_min, y_min), (w_min, h_min), ang = blackbox

                # For a "straight" rectangle, minAreaRect can have negative angles, etc.
                # The tutorial code tries to fix the angle for different shapes:
                if ang < -45:
                    ang = 90 + ang
                if w_min < h_min and ang > 0:
                    ang = (90 - ang) * -1
                if w_min > h_min and ang < 0:
                    ang = 90 + ang

                # Step 5: Compute an "error" from frame center for line-following
                frame_center_x = frame.shape[1] // 2  # half the width
                error = int(x_min - frame_center_x)

                # Convert angle to an integer for display
                ang = int(ang)

                # Draw the bounding box
                box_pts = cv.boxPoints(blackbox)
                box_pts = np.int8(box_pts)
                cv.drawContours(frame, [box_pts], 0, (0, 0, 255), 2)

                # Put debug info on the frame
                cv.putText(frame, f"Angle: {ang}", (10, 40),
                           cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv.putText(frame, f"Error: {error}", (10, 80),
                           cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                # Optionally draw a line from the top to the bottom
                cv.line(frame, (int(x_min), 0), (int(x_min), frame.shape[0]),
                        (255, 0, 0), 2)

            else:
                self.isRedLineDetected = False

            if display:
                cv.imshow("Red Line Contour Tracking", frame)

            # Break loop on 'q'
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv.destroyAllWindows()

