from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

app = QApplication([])
win = QMainWindow()
button = QPushButton('&Test')
win.setCentralWidget(button)
win.show()
app.exit(app.exec_())