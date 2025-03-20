# from driver.drive import *
from camera.camera import Camera
from threading import Thread
import time

cam = Camera(camera_id=0)
cameraProcess = Thread(target=cam.start_detection, kwargs={"display": True})
cameraProcess.start()


kp, ki, kd = 1, 1, 1



while True:


    p_out = kp * cam.curr_error
    i_out = ki * cam.integral
    d_out = kd * cam.derivative
    output = p_out + i_out + d_out


    print (output) 
    time.sleep(1)

