import cv2 as cv
import numpy as np
import math
import time
import os

class Camera:
    def __init__(self, camera_id=0):
        print("Camera initialized")
        self.cap = cv.VideoCapture(camera_id)
        
        # Set resolution
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv.CAP_PROP_FPS, 30)

        # Define HSV range for red color – same as your original code
        # self.red_lower = np.array([0, 100, 100])
        # self.red_upper = np.array([10, 255, 255])
        # self.red_lower_2 = np.array([160, 100, 100])
        # self.red_upper_2 = np.array([180, 255, 255])
        self.red_lower = np.array([0, 0, 200])
        self.red_upper = np.array([180, 30, 255])
        self.red_lower_2 = np.array([0, 0, 200])
        self.red_upper_2 = np.array([180, 30, 255])
        
        self.isRedLineDetected = False
        self.angle= 0
        self.curr_error = 0

    def start_detection(self, display=False, video_filename=None):
        """
        Continuously capture frames and detect + track the red line contours.
        """
        # Check if a valid video filename is provided and exists
        if video_filename is not None and os.path.exists(video_filename):
            self.cap.release()  # release the live feed if open
            self.cap = cv.VideoCapture(video_filename)
            print(f"Reading from file: {video_filename}")
        else:
            print("Using live feed")
            
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
            kernel = np.ones((3,3), np.uint8)
            mask = cv.erode(mask, kernel, iterations=5)
            mask = cv.dilate(mask, kernel, iterations=9)
            cv.imshow("mask2", mask)


            # Step 3: Find contours in the cleaned-up mask
            contours, hierarchy = cv.findContours(
                mask.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE
            )

            # Step 4: If we found any contours, pick one and analyze it, if multiple pick the one closest to bottom of the screen
            if contours:
                self.isRedLineDetected = True

                if len(contours) == 1:
                    blackbox = cv.minAreaRect(contours[0])
                else:
                    candidates = []
                    for idx, cnt in enumerate(contours):
                        box = cv.minAreaRect(cnt)
                        (x_min, y_min), (w_min, h_min), angle = box
                        candidates.append((y_min, idx, x_min, y_min))

                    candidates = sorted(candidates, key=lambda x: x[0])
                    _, chosen_idx, x_min, y_min = candidates[-1]
                    blackbox = cv.minAreaRect(contours[chosen_idx])

                (x_min, y_min), (w_min, h_min), ang = blackbox

                # if ang < -45:
                #     ang = 90 + ang
                # if w_min < h_min and ang > 0:
                #     ang = (90 - ang) * -1
                # if w_min > h_min and ang < 0:
                #     ang = 90 + ang

                frame_center_x = frame.shape[1] // 2
                error = int(x_min - frame_center_x)

                ang = int(ang)

                # Draw the bounding box using np.int32 instead of np.int0
                box_pts = cv.boxPoints(blackbox)
                box_pts = np.int32(box_pts)

                if box_pts.size > 0:
                    cv.drawContours(frame, [box_pts], 0, (0, 0, 255), 2)

                cv.putText(frame, f"Angle: {ang}", (10, 40),
                           cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv.putText(frame, f"Error: {error}", (10, 80),
                           cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                cv.line(frame, (int(x_min), 0), (int(x_min), frame.shape[0]),
                        (255, 0, 0), 2)
                
                cv.line(frame, (frame_center_x, 0), (frame_center_x, frame.shape[0]),
                        (0, 255, 0), 2)
            else:
                self.isRedLineDetected = False

            if display:
                cv.imshow("Red Line Contour Tracking", frame)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv.destroyAllWindows()

    def record(self, filename="output.avi", duration=10, display=False):
        """
        Record a video from the camera for a specified duration (in seconds)
        and save it to the given filename.
        """

        filename = input("Enter output filename (e.g., output.avi): ").strip()
        if not filename:
            filename = "output.avi"
        # Get frame dimensions from the capture device
        width = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        fps = self.cap.get(cv.CAP_PROP_FPS) or 30  # default to 30 if FPS not available

        # Define the codec and create VideoWriter object
        fourcc = cv.VideoWriter_fourcc(*"XVID")
        writer = cv.VideoWriter(f"media/{filename}", fourcc, fps, (width, height))

        start_time = time.time()
        print(f"Recording started. Saving to {filename}")

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to capture frame")
                break

            writer.write(frame)

            if display:
                cv.imshow("Recording", frame)
                if cv.waitKey(1) & 0xFF == ord('q'):
                    print("Recording stopped by user.")
                    break

            if time.time() - start_time > duration:
                print("Recording completed by duration.")
                break

        writer.release()
        cv.destroyWindow("Recording")
