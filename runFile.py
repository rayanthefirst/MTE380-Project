



# from driver.drive import *
from camera.camera import Camera
from threading import Thread



cam = Camera(camera_id=0)
cam.start_detection(display=True)
cameraProcess = Thread(target=cam.start_detection, kwargs={"display": True})
cameraProcess.start()

kp = 0
ki = 0
kd = 0

p_out = kp * cam.curr_error
i_out = ki * cam.integral
d_out = kd * cam.derivative
output = p_out + i_out + d_out


print (output)


