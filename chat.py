from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.acceptDrops()
        self.setFixedSize(400, 600)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setGeometry(1450, 430, 400, 600)

    def initUI(self, mainwindow):
        self.setWindowTitle("Chat Room")
        self.mainwindow = mainwindow #メインウィンドを渡す
        mainwindow.hide()

        chat = QLineEdit()
        history = QTextEdit()
        send = QPushButton('Send')
        grid = QGridLayout()
        grid.addWidget(history, 0, 0, 1, 4)
        grid.addWidget(chat, 1, 0)
        grid.addWidget(send, 1, 3)
        self.setLayout(grid)

    def closeEvent(self, e):
        self.mainwindow.show()
        e.accept()

