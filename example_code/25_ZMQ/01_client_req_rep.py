import zmq

context = zmq.Context()
print("Connecting to Server on port 5555")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")
print('Sending Hello')
socket.send(b"Hello")
print('Waiting for answer')
message = socket.recv()
print(f"Received: {message}")