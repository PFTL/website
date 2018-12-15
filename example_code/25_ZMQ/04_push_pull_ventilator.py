from time import sleep
import zmq
import cv2

context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.bind("tcp://*:5555")
cap = cv2.VideoCapture(0)
sleep(2)

sink = context.socket(zmq.REQ)
sink.connect('tcp://127.0.0.1:5557')
sink.send(b'')
s = sink.recv()

for i in range(100):
    ret, frame = cap.read()
    socket.send_pyobj(frame)
    print('Sent frame {}'.format(i))
