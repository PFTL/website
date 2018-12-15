from datetime import datetime
import h5py
from time import sleep
import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")
socket.setsockopt(zmq.SUBSCRIBE, b'camera_frame')
sleep(2)


with h5py.File('camera_data.hdf5', 'a') as file:
    now = str(datetime.now())
    g = file.create_group(now)

    topic = socket.recv_string()
    frame = socket.recv_pyobj()

    x = frame.shape[0]
    y = frame.shape[1]
    z = frame.shape[2]

    dset = g.create_dataset('images', (x, y, z, 1), maxshape=(x, y, z, None))
    dset[:, :, :, 0] = frame
    i=0
    while True:
        i += 1
        topic = socket.recv_string()
        frame = socket.recv_pyobj()
        dset.resize((x, y, z, i+1))
        dset[:, :, :, i] = frame
        file.flush()
        print('Received frame number {}'.format(i))
        if i == 50:
            break
