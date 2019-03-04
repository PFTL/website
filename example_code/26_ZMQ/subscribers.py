import h5py
from time import sleep
import numpy as np
import zmq


def save_movie(port, topic, frame_shape, dtype):
    f = h5py.File('movie.hdf5', 'w')
    dset = f.create_dataset("default", frame_shape+(1,), maxshape=frame_shape+(None,), dtype=dtype)
    context = zmq.Context()
    with context.socket(zmq.SUB) as socket:
        socket.connect(f"tcp://localhost:{port}")
        topic_filter = topic.encode('utf-8')
        socket.setsockopt(zmq.SUBSCRIBE, topic_filter)
        socket.setsockopt(zmq.SUBSCRIBE, ''.encode('utf-8'))
        i = 0
        while True:
            topic = socket.recv_string()
            data = socket.recv_pyobj()  # flags=0, copy=True, track=False)
            if isinstance(data, str):
                break
            dset[:,:,:,i] = data
            i += 1
            dset.resize(frame_shape+(i+1,))
        sleep(1)  # Gives enough time for the publishers to finish sending data before closing the socket
    f.flush()
    print(f'Acquired {i} frames')


def analyze_frames(port, topic, event):
    context = zmq.Context()
    with context.socket(zmq.SUB) as socket:
        socket.connect(f"tcp://localhost:{port}")
        topic_filter = topic.encode('utf-8')
        socket.setsockopt(zmq.SUBSCRIBE, topic_filter)
        socket.setsockopt(zmq.SUBSCRIBE, ''.encode('utf-8'))
        i = 0
        min = []
        max = []
        avg = []
        while True:
            topic = socket.recv_string()
            data = socket.recv_pyobj()  # flags=0, copy=True, track=False)
            if isinstance(data, str):
                break
            data = np.sum(data, 2)
            min.append(np.min(data))
            max.append(np.max(data))
            avg.append(np.mean(data))
            i+=1
    np.save('summary', np.array([min, max, avg]))
    print(f'Analysed {i} frames')


def slow_subscriber(port, topic):
    context = zmq.Context()
    with context.socket(zmq.SUB) as socket:
        socket.connect(f"tcp://localhost:{port}")
        socket.set_hwm(5)
        print(socket.get_hwm())
        topic_filter = topic.encode('utf-8')
        socket.setsockopt(zmq.RCVHWM, 5)
        socket.setsockopt(zmq.SUBSCRIBE, topic_filter)
        socket.setsockopt(zmq.SUBSCRIBE, ''.encode('utf-8'))
        i = 0
        while True:
            topic = socket.recv_string()
            data = socket.recv_pyobj()  # flags=0, copy=True, track=False)
            if isinstance(data, str):
                break
            i += 1
            sleep(.5)
            print(f'Slow {i}')
    print(f'Slow subscriber got {i} frames')