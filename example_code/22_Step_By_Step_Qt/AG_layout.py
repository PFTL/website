from PyQt5.QtWidgets import QApplication, QMainWindow, \
    QPushButton, QVBoxLayout, QWidget

app = QApplication([])
win = QMainWindow()
central_widget = QWidget()
button2 = QPushButton('Second Test', central_widget)
button = QPushButton('Test', central_widget)
layout = QVBoxLayout(central_widget)
layout.addWidget(button2)
layout.addWidget(button)
win.setCentralWidget(central_widget)
win.show()
app.exit(app.exec_())