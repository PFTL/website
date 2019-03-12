from PyQt5.QtWidgets import QApplication, QPushButton

app = QApplication([])

button = QPushButton('Press Me')
button.show()
button.clicked.connect(lambda x: print('Pressed!'))

app.exit(app.exec())

