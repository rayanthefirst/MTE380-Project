from camera.camera import Camera
from threading import Thread
cam = Camera(camera_id=0)
cameraProcess = Thread(target=cam.start_detection, kwargs={"display": True})
cameraProcess.start()

# print(cam.)