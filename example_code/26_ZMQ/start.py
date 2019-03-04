from multiprocessing import Queue, Process, Event
from time import sleep, time

from camera import Camera
from publisher import publisher
from subscribers import analyze_frames, save_movie, slow_subscriber
from threading import Thread

cam = Camera(0)
cam.initialize()

pub_queue = Queue()
stop_event = Event()
publisher_process = Process(target=publisher, args=(pub_queue, stop_event, 5555))
publisher_process.start()
analyzer_process = Process(target=analyze_frames, args=(5555, 'frame', stop_event))
analyzer_process.start()
frame = cam.get_frame()
saver_process = Process(target=save_movie, args=(5555, 'frame', frame.shape, frame.dtype))
saver_process.start()

slow_process = Process(target=slow_subscriber, args=(5555, 'frame'))
slow_process.start()

sleep(2)
camera_thread = Thread(target=cam.acquire_movie, args=(pub_queue,))
camera_thread.start()
t0 = time()
while time()-t0<5:
    print('Still acquiring')
    sleep(1)
cam.stop_movie = True
cam.close_camera()
pub_queue.put({'topic': 'frame', 'data': 'stop'})
camera_thread.join()
analyzer_process.join()
saver_process.join()
slow_process.join()
stop_event.set()
publisher_process.join()
print('Bye')