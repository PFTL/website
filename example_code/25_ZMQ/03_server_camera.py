from time import sleep
import zmq
import cv2

context = zmq.Context()
socket = context.socket(zmq.REP)
print('Binding to port 5555')
socket.bind("tcp://*:5555")
cap = cv2.VideoCapture(0)
sleep(1)

while True:
    message = socket.recv_string()
    if message == "read":
        ret, frame = cap.read()
        socket.send_pyobj(frame)
    if message == 'stop':
        socket.send_string('Stopping server')
        break