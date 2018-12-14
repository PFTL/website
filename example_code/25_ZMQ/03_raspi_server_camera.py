from time import sleep
import numpy as np
import zmq
import picamera
from picamera import PiCamera

context = zmq.Context()
socket = context.socket(zmq.REP)
print('Binding to port 5555')
socket.bind("tcp://*:5555")
camera = picamera.PiCamera()
sleep(1)

while True:
    message = socket.recv_string()
    if message == "read":
        camera.resolution = (320, 240)
        output = np.empty((240, 320, 3), dtype=np.uint8)
        camera.capture(output, 'rgb')
        socket.send_pyobj(output)
    if message == 'stop':
        socket.send_string('Stopping server')
        break