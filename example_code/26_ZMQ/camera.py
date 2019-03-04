import numpy as np
import cv2


class Camera:
    def __init__(self, cam_num):
        self.cam_num = cam_num
        self.cap = None
        self.last_frame = np.zeros((1,1))

    def initialize(self):
        self.cap = cv2.VideoCapture(self.cam_num)

    def get_frame(self, queue=None):
        ret, self.last_frame = self.cap.read()
        return self.last_frame

    def acquire_movie(self, queue):
        self.stop_movie = False
        while not self.stop_movie:
            queue.put({'topic': 'frame', 'data':self.get_frame()})

    def set_brightness(self, value):
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, value)

    def get_brightness(self):
        return self.cap.get(cv2.CAP_PROP_BRIGHTNESS)

    def close_camera(self):
        self.cap.release()

    def __str__(self):
        return 'OpenCV Camera {}'.format(self.cam_num)


if __name__ == '__main__':
    from time import sleep, time
    from multiprocessing import Process
    import multiprocessing as mp

    mp.set_start_method('spawn')

    cam = Camera(0)
    cam.initialize()
    movie_process = Process(target=cam.acquire_movie)
    movie_process.start()
    t0 = time()
    while time() - t0 < 10:
        # print(f'Total frames: {len(cam.movie)}')
        sleep(0.5)
    movie_process.terminate()
    cam.close_camera()