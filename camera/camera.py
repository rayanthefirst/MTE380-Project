import cv2 as cv
import numpy as np
import time

class Camera:
    def __init__(self, camera_id=0):
        print("Camera initialized")
        self.cap = cv.VideoCapture(camera_id)
        
        self.fps = 20
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 320)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 240)
        self.cap.set(cv.CAP_PROP_FPS, self.fps)

        self.red_lower = np.array([0, 100, 100])
        self.red_upper = np.array([10, 255, 255])
        self.red_lower_2 = np.array([160, 100, 100])
        self.red_upper_2 = np.array([180, 255, 255])

        self.isRedLineDetected = False
        self.angle = 0
        self.curr_error = 0
        self.prev_error = 0
        self.dt = 1 / self.fps

        self.latest_frame = None  # <--- NEW

    def start_detection(self, display=False, video_filename=None):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to capture frame")
                break

            self.latest_frame = frame.copy()  # <--- NEW

            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

            mask1 = cv.inRange(hsv, self.red_lower, self.red_upper)
            mask2 = cv.inRange(hsv, self.red_lower_2, self.red_upper_2)
            mask = cv.bitwise_or(mask1, mask2)

            contours, hierarchy = cv.findContours(
                mask.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE
            )

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
                ang = int(ang)
                self.angle = ang

                box_pts = cv.boxPoints(blackbox)
                box_pts = np.int32(box_pts)

                if box_pts.size > 0:
                    cv.drawContours(frame, [box_pts], 0, (0, 0, 255), 2)

                cv.putText(frame, f"Angle: {ang}", (10, 40),
                           cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv.putText(frame, f"Error: {error}", (10, 80),
                           cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                cv.line(frame, (int(x_min), 0), (int(x_min), frame.shape[0]), (255, 0, 0), 2)
                cv.line(frame, (frame_center_x, 0), (frame_center_x, frame.shape[0]), (0, 255, 0), 2)
            else:
                self.isRedLineDetected = False

            if display:
                cv.imshow("Red Line Contour Tracking", frame)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv.destroyAllWindows()
