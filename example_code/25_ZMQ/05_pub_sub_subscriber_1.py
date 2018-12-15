from time import sleep
import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")
socket.setsockopt(zmq.SUBSCRIBE, b'camera_frame')
sleep(2)


i=0
while True:
    i += 1
    topic = socket.recv_string()
    frame = socket.recv_pyobj()
    print('Received frame number {}'.format(i))
