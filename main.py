#ライブラリ
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from chat import ChatWindow
from clock import Clock
from memo import MemoWindow
from alarm import AlarmWindow


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
        self.chat_window = ChatWindow() #サブウィンド1
        self.time_window = Clock() #サブウィンド2
        self.memo_window = MemoWindow() #サブウィンド3
        self.alarm_window = AlarmWindow() #サブウィンド4

        self.followMouse = False

    #UI初期化
    def initUI(self):
        self.resize(300, 300)
        self.label = QLabel("", self)
        self.label.setFixedSize(200, 200)
        self.label.move(50, 40)
        self.pixmap = QPixmap('izumi.png')
        self.label.setPixmap(self.pixmap)

    #Escきーで終了
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.quit()

    #クリックイベント
    def mousePressEvent(self, e):
        #左クリックで移動
        if e.button() == Qt.LeftButton:
            self.followMouse = True
            self.mouse_drag_pos = e.globalPos() - self.pos()
            e.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))
        #右クリックでメニュー開く
        elif e.button() == Qt.RightButton:
            self.menu(e)

    #移動
    def mouseMoveEvent(self, e):
        if Qt.LeftButton and self.followMouse:
            self.move(e.globalPos() - self.mouse_drag_pos)
            e.accept()

    #クリック離す処理
    def mouseReleaseEvent(self, e):
        self.followMouse = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    #終了
    def quit(self):
        self.close()

    #メニュー
    def menu(self, e):
        contextMenu = QMenu(self)
        timeAct = contextMenu.addAction("時間")
        memoAct = contextMenu.addAction("メモ")
        chatAct = contextMenu.addAction("チャット")
        quitAct = contextMenu.addAction("終了")
        action = contextMenu.exec_(self.mapToGlobal(e.pos()))
        #動作
        if action == timeAct:
            self.time_window.show()
        elif action == chatAct:
            self.chat_window.hide_main(mascot)
            self.chat_window.show()
        elif action == memoAct:
            self.memo_window.show()
        elif action == quitAct:
            self.quit()


if __name__ == '__main__':
    App = QApplication(sys.argv)
    mascot = Window()
    mascot.show()
    sys.exit(App.exec())
