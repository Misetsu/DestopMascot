from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import time
from clock import Clock

text = ""

class ChatWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()
        self.acceptDrops()
        self.setFixedSize(400, 600)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setGeometry(1450, 430, 400, 600)
        self.time_window = Clock()
        self.COMMAND = {
            "/time": self.handle_time,
            "/openTimeWin": self.handle_openTimeWin,
            "/help": self.handle_help
        }

    def initUI(self):
        self.input = QLineEdit()
        self.history = QTextEdit()
        send = QPushButton("Send", self)
        send.clicked.connect(self.get_input)
        grid = QGridLayout()
        grid.addWidget(self.history, 0, 0, 1, 4)
        grid.addWidget(self.input, 1, 0)
        grid.addWidget(send, 1, 3)
        self.setLayout(grid)

    def hide(self, mainwindow):
        self.setWindowTitle("Chat Room")
        self.mainwindow = mainwindow  # メインウィンドを渡す
        mainwindow.hide()

    def closeEvent(self, e):
        self.mainwindow.show()
        e.accept()

    def get_input(self):
        global text
        text = self.input.text()
        self.get_response()
        self.input.setText("")

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Enter:
            self.get_input()

    def get_response(self):
        global text
        if text.startswith("/"):
            command = text.split()[0]
            if command in self.COMMAND:
                self.COMMAND[command]()
            else:
                self.history.setText(self.history.toPlainText()
                                     + command + " というコマンドなんてないよ\n/help で一覧見な\n")
        else:
            response = self.get_ai()
            self.history.setText(self.history.toPlainText() + response + "\n")

    def handle_time(self):
        t = time.localtime()
        ct = time.strftime("%H:%M", t)
        self.history.setText(self.history.toPlainText() + "今は" + ct
                             + "\n時計の画面開く？\n/openTimeWin で開けるよ\n")

    def handle_openTimeWin(self):
        self.time_window.show()
        self.close()

    def handle_help(self):
        self.history.setText(self.history.toPlainText() + "コマンド一覧：\n/time：現在時刻をチェック\n"
                             + "/openTimeWin：時間ウィンドを開く\n/help：これ")

    def get_ai(self):
        response = "AIまだないよ\nコマンド打ってな"
        return response
