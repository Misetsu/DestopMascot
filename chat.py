from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.acceptDrops()
        self.setFixedSize(400, 600)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setGeometry(1450, 430, 400, 600)

    def initUI(self):
        self.setWindowTitle("Chat Room")


