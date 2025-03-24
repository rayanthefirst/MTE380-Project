import cv2
import numpy as np
from driver.servo import open_arms, close_arms
from driver.drive import stop
from time import sleep

# Initialize webcam
cap = cv2.VideoCapture(0)

# Get the webcam resolution
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Load and resize the reference image of LEGO man
lego_template = cv2.imread('legoMan.jpg', 0)
lego_template = cv2.resize(lego_template, (frame_width, frame_height))

# Initialize ORB feature detector
orb = cv2.ORB_create()

# Compute keypoints and descriptors for the template
kp1, des1 = orb.detectAndCompute(lego_template, None)

lego_grabbed = False  # Flag to prevent repeated grabbing

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect features in the current frame
    kp2, des2 = orb.detectAndCompute(gray, None)

    # Use BFMatcher to find the best matches
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    if des2 is not None:
        matches = bf.match(des1, des2)
        matches = sorted(matches, key=lambda x: x.distance)

        # If enough matches are found and LEGO hasn't been grabbed yet
        if len(matches) > 10 and not lego_grabbed:
            print("LEGO detected with sufficient matches.")

            stop()
            open_arms()
            sleep(1)
            close_arms()
            lego_grabbed = True
            print("pickup done.")

            matched_frame = cv2.drawMatches(lego_template, kp1, frame, kp2, matches[:10], None, flags=2)
            cv2.imshow("LEGO Man Detection", matched_frame)

            print("Press Q to quit or Ctrl+C to stop.")
        else:
            if len(matches) > 10:
                matched_frame = cv2.drawMatches(lego_template, kp1, frame, kp2, matches[:10], None, flags=2)
                cv2.imshow("LEGO Man Detection", matched_frame)
            else:
                cv2.imshow("LEGO Man Detection", frame)
    else:
        cv2.imshow("LEGO Man Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
