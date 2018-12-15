import zmq
import numpy as np
from random import random

worker_id = random()

context = zmq.Context()
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://localhost:5555")

sender = context.socket(zmq.PUSH)
sender.connect("tcp://localhost:5556")

for i in range(100):
    print(i)
    image = receiver.recv_pyobj()
    fft = np.fft.fft2(image)
    sender.send_pyobj(fft)
