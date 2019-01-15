from time import sleep

from threading import Thread

from camera import Camera


class Experiment:
    def __init__(self, cam_num):
        self.cam_num = cam_num
        self.cam = None
        self.last_frame = None

    def initialize_camera(self):
        self.cam = Camera(cam_num=self.cam_num)
        self.cam.initialize()

    def acquire_frame(self):
        self.last_frame = self.cam.get_frame()

    def acquire_movie(self, num_frames):
        self.movie_thread = Thread(target=self.cam.acquire_movie, args=(num_frames,))
        self.movie_thread.start()

    def save_frame(self):
        pass

    def save_movie(self):
        pass

    def finalize(self):
        pass

    def __str__(self):
        return "Camera Experiment for cam {}".format(self.cam_num)


if __name__ == "__main__":
    exp = Experiment(0)
    exp.initialize_camera()
    exp.acquire_frame()
    print(exp.last_frame)

    exp.acquire_movie(100)
    while exp.movie_thread.is_alive():
        print('Acquiring movie...')
        sleep(0.3)