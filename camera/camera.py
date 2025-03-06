import cv2 as cv
import numpy as np
import math
import time

class Camera:
    def initCamera(self):
        print("Camera initialized")
        self.cap = cv.VideoCapture(0)
        
        # [*1] Set resolution
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)  # Set width to 640 pixels
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)  # Set height to 480 pixels
        self.cap.set(cv.CAP_PROP_FPS, 30)  # Set to 30 frames per second


        # Define HSV range for red color
        self.red_lower = np.array([0, 100, 100])
        self.red_upper = np.array([10, 255, 255])
        self.red_lower_2 = np.array([160, 100, 100])
        self.red_upper_2 = np.array([180, 255, 255])


    def start_detection(self, display=False):
        while True:
            # Capture Frame
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to capture frame")
                break

            # Resize frame for consistency
            frame = cv.resize(frame, (480, 480))

            # Detect red line
            redLineFrame = self.detect_red_line(frame)
            # in future we will have to change how we get the value of the redline
            return redLineFrame

             # Display the original frame with detected lines
            if display:
                cv.imshow('Red Line Detection', redLineFrame)

            # Break loop on user interrupt (e.g., 'q' key press)
            if cv.waitKey(1) & 0xFF == ord('q'):
                self.cap.release()
                cv.destroyAllWindows()
                return



            


    def detect_red_line(self, frame):
        # Convert to HSV color space
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # Create masks for red color
        mask1 = cv.inRange(hsv, self.red_lower, self.red_upper)
        mask2 = cv.inRange(hsv, self.red_lower_2, self.red_upper_2)
        mask = cv.bitwise_or(mask1, mask2)

        height, width, _ = frame.shape
        middle_x = width // 2
        lower_y = 0
        higher_y = height



        middleLine = np.array([[middle_x, lower_y, middle_x, higher_y]])
        cv.line(frame, (middleLine[0][0], middleLine[0][1]), (middleLine[0][2], middleLine[0][3]), (0, 255, 255), 2)

        # Apply mask to isolate red regions
        red_regions = cv.bitwise_and(frame, frame, mask=mask)

        # Convert the mask to grayscale for edge detection
        gray = cv.cvtColor(red_regions, cv.COLOR_BGR2GRAY)

        # Apply Canny edge detection
        edges = cv.Canny(gray, 50, 150)

        # Use HoughLinesP to detect line segments
        lines = cv.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)

        # Draw the detected lines on the original frame
        if len(lines) > 0:
            return True
        else:
            return False
        # if lines is not None:
        #     # print("Red line detected")
            
        #     for line in lines:
        #         # print("line", line, type(line))
        #         x1, y1, x2, y2 = line[0]  # Unpack line endpoints
        #         cv.line(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)  # Draw line in green


        #         frame = self.draw_angle(frame, line, middleLine)
        #         return True


        #         # print(ang)
        #         # time.sleep(2)


        #     # Compute angle between detected lines

        # else:
        #     return Fa
            # print("No red line detected")
            ...



        

        # return frame
    

    # def compute_angle(self, line1, line2):
    #     # Compute the angle of the detected line
        
    #     x1, y1, x2, y2 = line1[0]
    #     x3, y3, x4, y4 = line2[0]
    #     # Compute direction vectors for each line
    #     v1 = (x2 - x1, y2 - y1)
    #     v2 = (x4 - x3, y4 - y3)
        
    #     # Compute dot product and magnitudes
    #     dot = v1[0]*v2[0] + v1[1]*v2[1]
    #     mag1 = math.sqrt(v1[0]**2 + v1[1]**2)
    #     mag2 = math.sqrt(v2[0]**2 + v2[1]**2)
        
    #     # Calculate angle in radians then convert to degrees
    #     angle_rad = math.acos(dot / (mag1 * mag2))
    #     angle_deg = math.degrees(angle_rad)
    #     return angle_deg, v1, v2
    

    def draw_angle(self, frame, red_line, middle_line):
        # Unpack red line endpoints
        x1, y1, x2, y2 = red_line[0]
        # Get the x-coordinate of the vertical (middle) line
        middle_x = middle_line[0][0]
        
        # Compute the intersection point between the red line and the vertical line at x = middle_x
        if x2 != x1:
            slope = (y2 - y1) / (x2 - x1)
            inter_y = int(y1 + slope * (middle_x - x1))
        else:
            # If the red line is vertical, choose the midpoint of its y-values
            inter_y = (y1 + y2) // 2
        intersection = (middle_x, inter_y)
        
        # Compute the angle of the red line relative to the horizontal axis
        angle_red = math.degrees(math.atan2(y2 - y1, x2 - x1))
        # The vertical line is 90 degrees relative to the horizontal
        angle_vert = 90.0
        # Compute the absolute difference between the red line and vertical
        angle_diff = abs(angle_red - angle_vert)
        
        # For drawing the arc, define the arc to span from the smaller to larger angle value.
        start_angle = min(angle_red, angle_vert)
        end_angle = max(angle_red, angle_vert)
        
        # Draw an arc centered at the intersection point.
        # (30,30) is the radius for the arc – adjust as needed.
        cv.ellipse(frame, intersection, (30, 30), 0, start_angle, end_angle, (0, 0, 255), 2)
        
        # Draw a small circle at the intersection point for clarity.
        cv.circle(frame, intersection, 5, (0, 0, 255), -1)
        
        # Display the computed angle difference near the intersection point.
        cv.putText(frame, f"{angle_diff:.1f} deg", (intersection[0] + 10, intersection[1] - 10),
                cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        return frame

        









