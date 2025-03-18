
from camera.camera import Camera
from threading import Thread
import time
cam = Camera(camera_id=0)
# cam.start_detection(display=True)
cameraProcess = Thread(target=cam.start_detection, kwargs={"display": True})
cameraProcess.start()

while True:
    print(cam.angle)
    print(cam.curr_error)
    time.sleep(3)








