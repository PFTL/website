from time import sleep
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
print('Binding to port 5555')
socket.bind("tcp://*:5555")

while True:
    message = socket.recv()
    print(f"Received request: {message}")
    sleep(1)
    socket.send(message)
    if message == b'stop':
        break