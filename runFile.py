
# from gpiozero import Motor, RotaryEncoder
# from time import sleep

# #!/usr/bin/env python3

# # Set up the first motor and encoder
# motor1 = Motor(forward=13, backward=12)
# encoder1 = RotaryEncoder(a=9, b=10, max_steps=100)

# # Set up the second motor and encoder
# motor2 = Motor(forward=14, backward=15)
# encoder2 = RotaryEncoder(a=17, b=18, max_steps=100)

# SPEED = 0.25

# def main():
#     try:
#         while True:
#             # Read the encoder positions
#             print("Encoder 1 steps:", encoder1.steps)
#             print("Encoder 2 steps:", encoder2.steps)
            
#             # Control the first motor
#             if encoder1.steps < 50:
#                 motor1.forward(speed=SPEED)
#             else:
#                 motor1.backward(speed=SPEED)
            
#             # Control the second motor
#             if encoder2.steps < 50:
#                 motor2.forward(speed=SPEED)
#             else:
#                 motor2.backward(speed=SPEED)
                
#             sleep(3)
#     except KeyboardInterrupt:
#         print("Stopping the motors...")
#     finally:
#         motor1.stop()
#         motor2.stop()

# if __name__ == '__main__':
#     main()



# from camera.camera import Camera



# cam = Camera()
# cam.start_detection(display=True, video_filename="media/test.avi")
# cam.record("test.avi", 1000, False)





from driver.drive import determine_constants


determine_constants()
