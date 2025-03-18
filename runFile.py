
from camera.camera import Camera
from threading import Thread
from time import sleep
from driver.drive import *
cam = Camera(camera_id=0)
cameraProcess = Thread(target=cam.start_detection, kwargs={"display": True})
cameraProcess.start()
Kp = 1
Ka = 1
error_threshold = 50

# while True:
#     if cam.isRedLineDetected:
#         print("Red line detected")
        
#         if abs(cam.curr_error) < error_threshold:
#             print("Error small; driving forward.")
#             # If error is small, drive forward.
#             drive(forward=True)
#         else:
#             print("Error large; adjusting turn.")
#             # Calculate turn angle proportional to the error (limit to 30° maximum).
#             if cam.curr_error > 0:
#                 # If error is positive, the red line is to the right.
#                 # Turn right to adjust.
#                 turn(turn_right=True, error=abs(cam.curr_error))
#             else:
#                 # If error is negative, the red line is to the left.
#                 # Turn left to adjust.
#                 turn(turn_right=False, error=abs(cam.curr_error))
#     else:
#         # No red detected; stop the motors.
#         stop()
#     sleep(0.5)






# drive(forward=False)
turn(turn_right=True, error=80)
sleep(2)




