import zmq
from datetime import datetime

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")
msg = f"Now: {datetime.now()}"
print(f"Sending: {msg}")
socket.send(msg.encode('ascii'))
message = socket.recv()
print(f"Received: {message}")
# socket.send(b"stop")
# socket.recv()