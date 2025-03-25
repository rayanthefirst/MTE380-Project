import cv2 as cv
import numpy as np
import math
import time
import os

class Camera:
    def __init__(self, camera_id=0):
        print("Camera initialized")
        self.cap = cv.VideoCapture(camera_id)

        self.fps = 20
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 320)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 240)
        self.cap.set(cv.CAP_PROP_FPS, self.fps)

        # Define HSV ranges
        self.red_lower = np.array([0, 100, 100])
        self.red_upper = np.array([10, 255, 255])
        self.red_lower_2 = np.array([160, 100, 100])
        self.red_upper_2 = np.array([180, 255, 255])

        self.blue_lower = np.array([100, 100, 50])
        self.blue_upper = np.array([130, 255, 255])

        self.green_lower = np.array([40, 50, 50])
        self.green_upper = np.array([80, 255, 255])

        # State variables
        self.sees_blue = False
        self.sees_green = False
        self.isRedLineDetected = False
        self.curr_error = 0
        self.prev_error = 0
        self.angle = 0
        self.dt = 1 / self.fps
        self.latest_frame = None

    def start_detection(self, display=True, video_filename=None):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to capture frame")
                break

            self.latest_frame = frame.copy()
            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

            # --- BLUE DETECTION ---
            blue_mask = cv.inRange(hsv, self.blue_lower, self.blue_upper)
            self.sees_blue = cv.countNonZero(blue_mask) > 20

            # --- GREEN DETECTION ---
            green_mask = cv.inRange(hsv, self.green_lower, self.green_upper)
            self.sees_green = cv.countNonZero(green_mask) > 20

            # --- RED LINE DETECTION ---
            mask1 = cv.inRange(hsv, self.red_lower, self.red_upper)
            mask2 = cv.inRange(hsv, self.red_lower_2, self.red_upper_2)
            red_mask = cv.bitwise_or(mask1, mask2)

            contours, _ = cv.findContours(red_mask.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

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
                    candidates.sort(key=lambda x: x[0])
                    _, chosen_idx, x_min, y_min = candidates[-1]
                    blackbox = cv.minAreaRect(contours[chosen_idx])

                (x_min, y_min), (w_min, h_min), ang = blackbox

                if ang < -45:
                    ang = 90 + ang
                if w_min < h_min and ang > 0:
                    ang = (90 - ang) * -1
                if w_min > h_min and ang < 0:
                    ang = 90 + ang

                frame_center_x = frame.shape[1] // 2
                error = int(x_min - frame_center_x)
                self.prev_error = self.curr_error
                self.curr_error = error
                self.angle = int(ang)

                box_pts = cv.boxPoints(blackbox)
                box_pts = np.int32(box_pts)

                if box_pts.size > 0:
                    cv.drawContours(frame, [box_pts], 0, (0, 0, 255), 2)

                cv.putText(frame, f"Angle: {ang}", (10, 40), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv.putText(frame, f"Error: {error}", (10, 80), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                cv.line(frame, (int(x_min), 0), (int(x_min), frame.shape[0]), (255, 0, 0), 2)
                cv.line(frame, (frame_center_x, 0), (frame_center_x, frame.shape[0]), (0, 255, 0), 2)
            else:
                self.isRedLineDetected = False

            if display:
                cv.imshow("Red Line Contour Tracking", frame)
                cv.imshow("Blue Mask", blue_mask)
                cv.imshow("Green Mask", green_mask)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv.destroyAllWindows()

    def record(self, filename="output.avi", duration=10, display=False):
        filename = input("Enter the video filename (with extension, e.g. output.avi): ")
        if not filename:
            filename = "output.avi"

        width = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        fps = self.cap.get(cv.CAP_PROP_FPS) or 30

        fourcc = cv.VideoWriter_fourcc(*"XVID")
        writer = cv.VideoWriter(f"media/{filename}", fourcc, fps, (width, height))

        start_time = time.time()
        print(f"Recording started. Saving to {filename}")

        try:
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

        except KeyboardInterrupt:
            print("Recording stopped by user.")
        finally:
            writer.release()
            cv.destroyWindow("Recording")

if __name__ == "__main__":
    cam = Camera(camera_id=0)
    cam.start_detection(display=True)
