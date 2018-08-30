import numpy as np

from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QApplication


class StartWindow(QMainWindow):
    def __init__(self, camera = None):
        super().__init__()
        self.camera = camera

        self.central_widget = QWidget()
        self.button_frame = QPushButton('Acquire Frame', self.central_widget)
        self.button_movie = QPushButton('Start Movie', self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.button_frame)
        self.layout.addWidget(self.button_movie)
        self.setCentralWidget(self.central_widget)

        self.button_frame.clicked.connect(self.update_image)

    def update_image(self):
        frame = self.camera.get_frame()
        print('Maximum in frame: {}, Minimum in frame: {}'.format(np.max(frame), np.min(frame)))

if __name__ == '__main__':
    app = QApplication([])
    window = StartWindow()
    window.show()
    app.exit(app.exec_())