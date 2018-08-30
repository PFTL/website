import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, \
    QPushButton, QVBoxLayout, QWidget

cap = cv2.VideoCapture(0)
def button_min_pressed():
    ret, frame = cap.read()
    print(np.min(frame))

def button_max_pressed():
    ret, frame = cap.read()
    print(np.max(frame))


app = QApplication([])
win = QMainWindow()
central_widget = QWidget()
button_min = QPushButton('Get Minimum', central_widget)
button_max = QPushButton('Get Maximum', central_widget)
button_min.clicked.connect(button_min_pressed)
button_max.clicked.connect(button_max_pressed)
layout = QVBoxLayout(central_widget)
layout.addWidget(button_min)
layout.addWidget(button_max)
win.setCentralWidget(central_widget)
win.show()
app.exit(app.exec_())
cap.release()
