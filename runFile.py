from gpiozero import Servo
from time import sleep

# from driver.drive import sigmoid
# from camera.camera import Camera
# from threading import Thread
# import time

# cam = Camera(camera_id=0)
# cameraProcess = Thread(target=cam.start_detection, kwargs={"display": True})
# cameraProcess.start()


# kp, ki, kd = 1, 1, 1



# while True:


#     p_out = kp * cam.curr_error
#     i_out = ki * cam.integral
#     d_out = kd * cam.derivative
#     output = p_out + i_out + d_out

#     print("p_out: ", p_out) 
#     print("i_out: ", i_out)
#     print("d_out: ", d_out)
#     print (output) 
#     print("sigmoid: ", sigmoid(output))
#     time.sleep(1)



servo = Servo(20)

servo.min()
sleep(3)
servo.mid()
sleep(3)
servo.max()
sleep(3)