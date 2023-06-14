#ライブラリ
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from datetime import datetime
from clock import Clock
from memo import MemoWindow
import alarm


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
        self.setWindowTitle("Chat Room")
        self.time_window = Clock()
        self.memo_window = MemoWindow()
        self.alarm_window = alarm.AlarmWindow()
        #コマンドラインを定義
        self.COMMAND = {
            "/time": self.handle_time,
            "/openTime": self.handle_openTime,
            "/openCalendar": self.handle_openCalendar,
            "/openAlarm": self.handle_openAlarm,
            "/openMemo": self.handle_openMemo,
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
                             + "\n時計の画面開く？\n/openTime で開けるよ\n")

    #/openTimeのコマンド動作
    def handle_openTime(self):
        self.time_window.show()
        self.close()

    # /openCalendarのコマンド動作
    def handle_openCalendar(self):
        self.alarm_window.Stack.setCurrentIndex(0)
        self.alarm_window.show()
        self.close()

    # /openAlarmのコマンド動作
    def handle_openAlarm(self):
        self.alarm_window.Stack.setCurrentIndex(1)
        self.alarm_window.show()
        self.close()

    # /openMemoのコマンド動作
    def handle_openMemo(self):
        self.memo_window.show()
        self.close()

    #/helpのコマンド動作
    def handle_help(self):
        self.history.setText(self.history.toPlainText() + "コマンド一覧：\n/time：現在時刻をチェック\n"
                             + "/openTime：時間ウィンドを開く\n"
                             + "/openCalendar：日記とタスクウィンドを開く\n"
                             + "/openAlarm：アラームウィンドを開く\n"
                             + "/openMemoメモ機能を開く\n"
                             + "/help：これ\n以上！\n")

    #AIで返事を取得
    def get_ai(self):
        response = "AIまだないよ\nコマンド打ってな"
        return response
