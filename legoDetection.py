import cv2
import numpy as np

# Initialize webcam
cap = cv2.VideoCapture(0)

# Get the webcam resolution
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Load and resize the reference image of LEGO man
lego_template = cv2.imread('lego.jpg', 0)
lego_template = cv2.resize(lego_template, (frame_width, frame_height))  # Resize to match video frame

# Initialize ORB feature detector
orb = cv2.ORB_create()

# Compute keypoints and descriptors for the template
kp1, des1 = orb.detectAndCompute(lego_template, None)

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

        # If enough matches are found, draw them
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
