from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

def button_pressed():
    print('Button Pressed')

app = QApplication([])
win = QMainWindow()
button = QPushButton('&Test')
button.clicked.connect(button_pressed)
win.setCentralWidget(button)
win.show()
app.exit(app.exec_())