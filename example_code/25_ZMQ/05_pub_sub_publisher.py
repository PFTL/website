from time import sleep
import zmq
import cv2

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")
cap = cv2.VideoCapture(0)
sleep(2)

i=0
topic = 'camera_frame'
while True:
    i += 1
    ret, frame = cap.read()
    socket.send_string(topic, zmq.SNDMORE)
    socket.send_pyobj(frame)
    print('Sent frame {}'.format(i))
