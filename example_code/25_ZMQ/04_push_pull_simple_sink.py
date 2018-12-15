import zmq

context = zmq.Context()
receiver = context.socket(zmq.PULL)
receiver.bind("tcp://*:5556")

ffts = []
for i in range(100):
    fft = receiver.recv_pyobj()
    ffts.append(fft)
    print('Received frame {}'.format(i))

print("Collected 100 FFT from the workers")