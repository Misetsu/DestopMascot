import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QLocale
from datetime import datetime

class MyWidget(QWidget):
    # ウィンド初期化
    def __init__(self):
        super(MyWidget, self).__init__()

        self.setFixedSize(1000, 500)
        self.button = QPushButton("change")
        self.button.clicked.connect(self.changeLayout)

        self.stack1 = QWidget() #画面1
        self.stack2 = QWidget() #画面2

        self.stack1UI()
        self.stack2UI()

        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack2)

        layout = QGridLayout(self)
        layout.addWidget(self.Stack, 2, 0, 1, 5)
        layout.addWidget(self.button, 3, 4)
        self.setLayout(layout)

    # 画面切り替え動作
    def changeLayout(self):
        i = self.Stack.currentIndex()
        if i == 1:
            self.Stack.setCurrentIndex(0)
        else:
            self.Stack.setCurrentIndex(1)

    # 画面1UI
    def stack1UI(self):
        self.cal = QCalendarWidget(self)
        self.cal.setLocale(QLocale(QLocale.Japanese))
        self.cal.setGridVisible(True)
        self.cal.selectionChanged.connect(self.dateChange)

        self.tasklist = QListWidget()

        layout = QHBoxLayout()
        layout.addWidget(self.cal, 2)
        layout.addWidget(self.tasklist, 2)

        self.stack1.setLayout(layout)

    def dateChange(self):
        pass

    # 画面2UI
    def stack2UI(self):
        self.memolist = QListWidget()
        self.getSummary()
        self.memolist.itemClicked.connect(self.changeMemo)

        self.memopad = QTextEdit()

        self.add = QPushButton("Add")
        self.add.clicked.connect(self.addMemo)
        self.save = QPushButton("Save")
        self.save.clicked.connect(self.saveMemo)
        self.delete = QPushButton("Delete")
        self.delete.clicked.connect(self.deleteMemo)

        layout = QGridLayout()
        layout.addWidget(self.add, 0, 5)
        layout.addWidget(self.save, 0, 6)
        layout.addWidget(self.delete, 0, 7)
        layout.addWidget(self.memolist, 1, 0, 1, 3)
        layout.addWidget(self.memopad, 1, 3, 1, 5)
        self.stack2.setLayout(layout)

    # メモの目次を取得
    def getSummary(self):
        # ファイルの場所を取得
        summary = []
        cwd = os.getcwd()
        cwd = cwd + "/memo"
        l = [f for f in os.listdir(cwd) if f.endswith(".txt")]
        for i in l:
            p = cwd + "/" + i
            # Read only
            with open(p, "r") as file:
                first_line = file.readline().strip('\n') # 1行目
            summary.append(first_line)
        # 更新
        self.memolist.clear()
        self.memolist.addItems(summary)

    # 表示するメモをかえる
    def changeMemo(self):
        # ファイルの場所を取得
        i = int(self.memolist.currentRow())
        cwd = os.getcwd()
        cwd = cwd + "/memo"
        l = [f for f in os.listdir(cwd) if f.endswith(".txt")]
        p = cwd + "/" + l[i]
        # Read & write
        with open(p, "r+") as file:
            data = file.read()
        self.memopad.setPlainText(data)

    # メモを追加
    def addMemo(self):
        # ファイルの場所を取得
        t = datetime.now()
        ct = t.strftime("%Y%m%d%H%M%S")
        name = "memo" + ct + ".txt"
        cwd = os.getcwd()
        cwd = cwd + "/memo"
        p = cwd + "/" + name
        try:
            open(p, "x")
            l = [f for f in os.listdir(cwd) if f.endswith(".txt")]
            for i in range(len(l)):
                if l[i].endswith(name):
                    break
            self.memolist.setCurrentRow(i)
            self.changeMemo()
        finally:
            self.getSummary()
            self.memolist.setCurrentRow(i)

    # メモを保存
    def saveMemo(self):
        # ファイルの場所を取得
        i = int(self.memolist.currentRow())
        cwd = os.getcwd()
        cwd = cwd + "/memo"
        l = [f for f in os.listdir(cwd) if f.endswith(".txt")]
        p = cwd + "/" + l[i]
        # Overwrite
        with open(p, "w") as file:
            file.write(self.memopad.toPlainText())
        # 更新
        self.getSummary()
        self.memolist.setCurrentRow(i)
        self.changeMemo()

    # メモを削除
    def deleteMemo(self):
        # ファイルの場所を取得
        i = int(self.memolist.currentRow())
        cwd = os.getcwd()
        cwd = cwd + "/memo"
        l = [f for f in os.listdir(cwd) if f.endswith(".txt")]
        p = cwd + "/" + l[i]
        # ファイルがあるかチェック
        if os.path.exists(p):
            os.remove(p)
        # 更新
        self.getSummary()
        self.memolist.setCurrentRow(0)
        self.changeMemo()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())
