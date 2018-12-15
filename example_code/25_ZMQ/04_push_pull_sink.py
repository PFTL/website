import zmq
from time import time


context = zmq.Context()
receiver = context.socket(zmq.PULL)
receiver.bind("tcp://*:5556")

ventilator = context.socket(zmq.REP)
ventilator.bind('tcp://*:5557')
ventilator.recv()
ventilator.send(b"")

ffts = []
for i in range(100):
    fft = receiver.recv_pyobj()
    ffts.append(fft)
    print('Received frame {}'.format(i))

print(ffts)