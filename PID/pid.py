# pid.py
import time

class PID:
    def __init__(self, kp, ki, kd, target=0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.target = target
        self.integral = 0
        self.prev_error = 0
        self.last_time = None

    def compute(self, current):
        error = self.target - current
        current_time = time.time()
        dt = (current_time - self.last_time) if self.last_time else 0.1
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt if dt > 0 else 0
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.prev_error = error
        self.last_time = current_time
        return output

        
