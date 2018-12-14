from time import sleep
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

print('Binding to port 5555')
message = socket.recv()
print(f"Received request: {message}")
sleep(1)
socket.send(b"Message Received")