from PyQt5.QtWidgets import QApplication, QMainWindow, \
    QPushButton, QVBoxLayout, QWidget

def button_pressed():
    print('Button Pressed')

app = QApplication([])
win = QMainWindow()
central_widget = QWidget()
button = QPushButton('Test', win)
button2 = QPushButton('Second Test', win)
# layout = QVBoxLayout(central_widget)
# layout.addWidget(button2)
# layout.addWidget(button)

# button.clicked.connect(button_pressed)
# button2.clicked.connect(button_pressed)
win.setCentralWidget(central_widget)
win.show()
app.exit(app.exec_())