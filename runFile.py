
from camera.camera import Camera
from threading import Thread
cam = Camera(camera_id=0)
cameraProcess = Thread(target=cam.start_detection, args=(True,))


while True:
    print(cam.angle)
    print(cam.curr_error)








