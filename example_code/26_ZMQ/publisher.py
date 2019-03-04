import zmq
from time import sleep


def publisher(queue, event, port):
    """ Simple method that starts a publisher on the port 5555.

    :param multiprocessing.Queue queue: Queue of messages to be broadcast
    :param multiprocessing.Event event: Event to stop the publisher
    :param int port: port in which to broadcast data
    .. TODO:: The publisher's port should be determined in a configuration file.
    """
    port_pub = port
    context = zmq.Context()
    with context.socket(zmq.PUB) as socket:
        socket.bind("tcp://*:%s" % port_pub)
        while not event.is_set():
            while not queue.empty():
                data = queue.get()  # Should be a dictionary {'topic': topic, 'data': data}
                socket.send_string(data['topic'], zmq.SNDMORE)
                socket.send_pyobj(data['data'])
        sleep(0.005)  # Sleeps 5 milliseconds to be polite with the CPU
        sleep(1)  # Gives enough time to the subscribers to update their status
    print('Finished publisher')
