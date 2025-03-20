



# from driver.drive import *
from camera.camera import Camera
from threading import Thread
import tkinter as tk



cam = Camera(camera_id=0)
cameraProcess = Thread(target=cam.start_detection, kwargs={"display": True})
cameraProcess.start()
def tune_pid():
    def submit():
        nonlocal kp, ki, kd
        kp = scale_kp.get()
        ki = scale_ki.get()
        kd = scale_kd.get()
        root.destroy()

    kp, ki, kd = 0.0, 0.0, 0.0

    root = tk.Tk()
    root.title("Tune PID Controller Parameters")

    tk.Label(root, text="Kp:").grid(row=0, column=0, padx=5, pady=5)
    scale_kp = tk.Scale(root, from_=0, to=10, resolution=0.1, orient=tk.HORIZONTAL)
    scale_kp.grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(root, text="Ki:").grid(row=1, column=0, padx=5, pady=5)
    scale_ki = tk.Scale(root, from_=0, to=10, resolution=0.1, orient=tk.HORIZONTAL)
    scale_ki.grid(row=1, column=1, padx=5, pady=5)
    
    tk.Label(root, text="Kd:").grid(row=2, column=0, padx=5, pady=5)
    scale_kd = tk.Scale(root, from_=0, to=10, resolution=0.1, orient=tk.HORIZONTAL)
    scale_kd.grid(row=2, column=1, padx=5, pady=5)
    
    button = tk.Button(root, text="Apply", command=submit)
    button.grid(row=3, column=0, columnspan=2, pady=10)

    root.mainloop()
    return kp, ki, kd

kp, ki, kd = tune_pid()

p_out = kp * cam.curr_error
i_out = ki * cam.integral
d_out = kd * cam.derivative
output = p_out + i_out + d_out


print (output)


