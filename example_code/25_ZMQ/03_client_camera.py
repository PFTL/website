import zmq
import numpy as np
import matplotlib.pyplot as plt
import cv2

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")
socket.send_string('read')
image = socket.recv_pyobj()
print(np.min(image))
print(np.max(image))
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.show()
socket.send_string('stop')
print(socket.recv_string())