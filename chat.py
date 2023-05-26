#ライブラリ
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from datetime import datetime
from clock import Clock

text = "" #入力

class ChatWindow(QWidget):
    #ウィンドウ初期化
    def __init__(self):
        super().__init__()

        self.initUI()
        self.acceptDrops()
        self.setFixedSize(400, 600)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setGeometry(1450, 430, 400, 600)
        self.time_window = Clock()
        #コマンドラインを定義
        self.COMMAND = {
            "/time": self.handle_time,
            "/openTimeWin": self.handle_openTimeWin,
            "/help": self.handle_help
        }

    #UI初期化
    def initUI(self):
        self.input = QLineEdit()
        self.history = QTextEdit()
        self.history.setReadOnly(True)
        send = QPushButton("Send", self)
        send.clicked.connect(self.get_input)
        grid = QGridLayout()
        grid.addWidget(self.history, 1, 0, 1, 4)
        grid.addWidget(self.input, 2, 0)
        grid.addWidget(send, 2, 3)
        self.setLayout(grid)

    #メイン画面を隠す
    def hide_main(self, mainwindow):
        self.setWindowTitle("Chat Room")
        self.mainwindow = mainwindow  # メインウィンドを渡す
        mainwindow.hide()

    #閉じる
    def closeEvent(self, e):
        self.mainwindow.show()
        e.accept()

    #入力を取得
    def get_input(self):
        global text
        text = self.input.text()
        self.get_response()
        self.input.setText("")

    #Enterキーでチャット送る
    def keyPressEvent(self, e):
        if (e.key() == Qt.Key_Return) or (e.key() == Qt.Key_Enter):
            self.get_input()

    #返事を取得
    def get_response(self):
        global text
        #コマンドラインの場合
        if text.startswith("/"):
            command = text.split()[0]
            if command in self.COMMAND:
                self.COMMAND[command]()
            else:
                self.history.setText(self.history.toPlainText()
                                     + command + " というコマンドなんてないよ\n/help で一覧見な\n")
        #AIチャットの場合
        else:
            response = self.get_ai()
            self.history.setText(self.history.toPlainText() + response + "\n")

    #/Timeのコマンド動作
    def handle_time(self):
        t = datetime.now()
        ct = t.strftime("%Y年%m月%d日の%H時%M分")
        self.history.setText(self.history.toPlainText() + "今は" + ct
                             + "\n時計の画面開く？\n/openTimeWin で開けるよ\n")

    #/openTimeWinのコマンド動作
    def handle_openTimeWin(self):
        self.time_window.show()
        self.close()

    #/helpのコマンド動作
    def handle_help(self):
        self.history.setText(self.history.toPlainText() + "コマンド一覧：\n/time：現在時刻をチェック\n"
                             + "/openTimeWin：時間ウィンドを開く\n/help：これ\n")

    #AIで返事を取得
    def get_ai(self):
        response = "AIまだないよ\nコマンド打ってな"
        return response
