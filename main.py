import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from chat import ChatWindow
import random
import datetime


class Window(QMainWindow):
    #ウィンド初期化
    def __init__(self):
        super(Window, self).__init__()

        self.initUI()
        self.acceptDrops()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(1500, 790, 300, 300)
        self.pixmap = QPixmap('izumi.png')
        self.sub_window = ChatWindow() #サブウィンド

        with open("data.txt", "r", encoding="utf-8") as f:
            text = f.read()
            self.sentence = text.split("\n")
        self.followMouse = False

    #UI初期化
    def initUI(self):
        self.resize(300, 300)
        self.label1 = QLabel("", self)
        self.label1.setStyleSheet("font: 18pt; color: black;")
        self.label = QLabel("", self)
        self.label.setFixedSize(200, 200)
        self.label.move(50, 40)
        self.pixmap = QPixmap('izumi.png')
        self.label.setPixmap(self.pixmap)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.quit()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.followMouse = True
            self.mouse_drag_pos = e.globalPos() - self.pos()
            e.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))
        elif e.button() == Qt.RightButton:
            self.menu(e)

    def mouseMoveEvent(self, e):
        if Qt.LeftButton and self.followMouse:
            self.move(e.globalPos() - self.mouse_drag_pos)
            e.accept()

    def mouseReleaseEvent(self, e):
        self.followMouse = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def quit(self):
        self.close()

    def menu(self, e):
        contextMenu = QMenu(self)
        timeAct = contextMenu.addAction("時間")
        memoAct = contextMenu.addAction("メモ")
        chatAct = contextMenu.addAction("チャット")
        quitAct = contextMenu.addAction("終了")
        action = contextMenu.exec_(self.mapToGlobal(e.pos()))
        if action == timeAct:
            self.time()
        elif action == chatAct:
            self.sub_window.initUI(mascot)
            self.sub_window.show()
        elif action == quitAct:
            self.quit()

    def talk(self):
        self.label1.setText(random.choice(self.sentence))
        self.label1.move(0, 0)
        self.label1.setStyleSheet("font: bold; background-color: white; color: black; "
                                  "border: 3px solid #1C3561;")
        self.label1.resize(300, 36)
        self.label1.setWordWrap(True)

    def time(self):
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.label1.setText(current_time)
        self.label1.move(0, 0)
        self.label1.setStyleSheet("font: bold; background-color: white; color: black; "
                                  "border: 3px solid #1C3561;")
        self.label1.resize(300, 36)
        self.label1.setWordWrap(True)


if __name__ == '__main__':
    App = QApplication(sys.argv)
    mascot = Window()
    mascot.show()
    sys.exit(App.exec())
