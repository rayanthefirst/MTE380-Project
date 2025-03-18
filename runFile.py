
from camera.camera import Camera
from threading import Thread
import time
cam = Camera(camera_id=0)
cameraProcess = Thread(target=cam.start_detection, kwargs={"display": True})


while True:
    print(cam.angle)
    print(cam.curr_error)
    time.sleep(3)








