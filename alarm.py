#ライブラリ
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QLocale, QDate, Qt, QTimer, QTime

date_index = QDate.currentDate()
date_index = date_index.toString("yyyyMMdd")

class AlarmWindow(QWidget):
    # ウィンド初期化
    def __init__(self):
        super(AlarmWindow, self).__init__()

        self.setFixedSize(1000, 500)

        self.button = QPushButton("change")
        self.button.clicked.connect(self.changeLayout)

        self.stack1 = QWidget() #画面1：日記/タスク
        self.stack2 = QWidget() #画面2：アラーム

        self.stack1UI()
        self.stack2UI()

        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack2)

        layout = QGridLayout(self)
        layout.addWidget(self.Stack, 0, 0, 1, 5)
        layout.addWidget(self.button, 3, 4)
        self.setLayout(layout)

    # 画面切り替え動作
    def changeLayout(self):
        i = self.Stack.currentIndex()
        if i == 1:
            self.Stack.setCurrentIndex(0)
        else:
            self.saveDiary()
            self.saveTask()
            self.Stack.setCurrentIndex(1)

    # 画面1UI
    def stack1UI(self):
        self.cal = QCalendarWidget(self)
        self.cal.setLocale(QLocale(QLocale.Japanese))
        self.cal.setGridVisible(True)
        self.cal.selectionChanged.connect(self.dateChange)
        self.cal.setSelectedDate(QDate.currentDate())

        self.diary = QTextEdit()

        self.input = QLineEdit()
        self.add = QPushButton("Add")
        self.add.clicked.connect(self.addTask)
        self.task = QListWidget()

        layout = QGridLayout()
        layout.addWidget(self.cal, 0, 0, 8, 4)
        layout.addWidget(self.diary, 0, 4, 3, 4)
        layout.addWidget(self.input, 4, 4, 1, 3)
        layout.addWidget(self.add, 4, 7)
        layout.addWidget(self.task, 5, 4, 3, 4)

        self.getDiary()
        self.getTask()
        self.dateChange()
        self.stack1.setLayout(layout)

    # ウィンドを閉じる時の動作
    def closeEvent(self, e):
        self.saveDiary()
        self.saveTask()
        self.saveAlarm()
        self.close()

    # 日付切り替え動作
    def dateChange(self):
        global date_index
        self.saveDiary()
        self.saveTask()
        d = self.cal.selectedDate()
        date_index = d.toString("yyyyMMdd")
        self.getDiary()
        self.getTask()

    # 日記を取得
    def getDiary(self):
        global date_index
        # ファイルの場所を取得
        d = date_index
        cwd = os.getcwd()
        cwd = cwd + "/calendar"
        p = cwd + "/diary" + d + ".txt"
        # ファイルを新しく作る、エラーは無視、最後にファイルを読み込む
        try:
            open(p, "x", encoding="utf-8")
        except:
            pass
        finally:
            # Read & write
            with open(p, "r+", encoding="utf-8") as file:
                data = file.read()
            self.diary.setPlainText(data)

    # 日記保存
    def saveDiary(self):
        global date_index
        # ファイルの場所を取得
        d = date_index
        cwd = os.getcwd()
        cwd = cwd + "/calendar"
        p = cwd + "/diary" + d + ".txt"
        # Overwrite
        with open(p, "w", encoding="utf-8") as file:
            file.write(self.diary.toPlainText())

    # タスクを取得
    def getTask(self):
        global date_index
        self.task.clear()
        # ファイルの場所を取得
        d = date_index
        cwd = os.getcwd()
        cwd = cwd + "/calendar"
        p = cwd + "/task" + d + ".txt"
        # ファイルを新しく作る、エラーは無視、最後にファイルを読み込む
        try:
            open(p, "x", encoding="utf-8")
        except:
            pass
        finally:
            with open(p, "r+", encoding="utf-8") as file:
                lines = [line.rstrip() for line in file]
            for line in lines:
                flg, name = line.split("&_sep_&")
                item = QListWidgetItem(name)
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                if flg == "1":
                    item.setCheckState(Qt.Checked)
                elif flg == "0":
                    item.setCheckState(Qt.Unchecked)
                self.task.addItem(item)

    # タスクを追加
    def addTask(self):
        global date_index
        # ファイルの場所を取得
        d = date_index
        cwd = os.getcwd()
        cwd = cwd + "/calendar"
        p = cwd + "/task" + d + ".txt"
        text = self.input.text()
        # 最後に追加
        with open(p, "a", encoding="utf-8") as file:
            file.write("0&_sep_&" + text + "\n")
        self.input.setText("")
        self.getTask()

    # タスクを保存
    def saveTask(self):
        global date_index
        all_task = ""
        # アイテムごとにチェック
        for i in range(self.task.count()):
            item = self.task.item(i)
            if item.checkState() == Qt.Checked:
                all_task = all_task + "1&_sep_&" + item.text() + "\n"
            elif item.checkState() == Qt.Unchecked:
                all_task = all_task + "0&_sep_&" + item.text() + "\n"
        # ファイルの場所を取得
        d = date_index
        cwd = os.getcwd()
        cwd = cwd + "/calendar"
        p = cwd + "/task" + d + ".txt"
        # Overwrite
        with open(p, "w", encoding="utf-8") as file:
            file.write(all_task)
        self.getTask()

    # 画面2UI
    def stack2UI(self):
        self.alarm_list = []
        self.on_alarm = []
        cwd = os.getcwd()
        cwd = cwd + "/calendar"
        p = cwd + "/alarm.txt"
        try:
            with open(p, "r+", encoding="utf-8") as file:
                lines = [line.rstrip() for line in file]
            self.alarm_list = lines[0].split(" ")
            self.on_alarm = lines[1].split(" ")
        finally:
            pass

        self.time = QLabel()
        self.time.setAlignment(Qt.AlignCenter)

        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime.currentTime())
        self.time_edit.setDisplayFormat("hh:mm")

        self.add_alarm = QPushButton("Add")
        self.add_alarm.clicked.connect(self.addAlarm)

        self.Frame = QGroupBox()
        self.FrameHorizontalLayout = QHBoxLayout(self.Frame)
        self.ListWidget = QListWidget(self.Frame)
        self.ListWidget.setSpacing(11)
        self.ListWidget.setStyleSheet(
            "QListWidget { background: palette(window); border: none;}"
            "QListWidget::item {"
            "border-style: solid;"
            "border-width:1px;"
            "border-color:  black;"
            "margin-right: 30px;"
            "}"
            "QListWidget::item:hover {"
            "border-color: blue;"
            "}")
        self.FrameHorizontalLayout.addWidget(self.ListWidget)

        self.layout2 = QGridLayout(self)
        self.layout2.addWidget(self.time, 0, 0, 8, 4)
        self.layout2.addWidget(self.time_edit, 0, 4, 1, 3)
        self.layout2.addWidget(self.add_alarm, 0, 7, 1, 1)
        self.layout2.addWidget(self.Frame, 1, 4, 7, 4)
        self.getAlarmList()
        self.stack2.setLayout(self.layout2)

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

    # 時計を表示
    def showTime(self):
        current_time = QTime.currentTime()
        label_time = current_time.toString("hh:mm:ss")
        self.time.setText(label_time)

    def getAlarmList(self):
        for i in range(len(self.alarm_list)):
            self.item = QListWidgetItem()
            self.item_widget = QWidget()
            self.line_text = QLabel(self.alarm_list[i])
            self.line_push_button = QPushButton("Off")
            self.line_push_button.setObjectName("switch " + str(i))
            self.line_push_button.setCheckable(True)
            if self.alarm_list[i] in self.on_alarm:
                self.line_push_button.setChecked(True)
                self.line_push_button.setText("On")
            self.line_push_button.clicked.connect(self.clicked)
            self.delete_button = QPushButton("X")
            self.delete_button.setObjectName("del " + str(i))
            self.delete_button.clicked.connect(self.delAlarm)
            self.item_layout = QHBoxLayout()
            self.item_layout.addWidget(self.line_text)
            self.item_layout.addWidget(self.line_push_button)
            self.item_layout.addWidget(self.delete_button)
            self.item_widget.setLayout(self.item_layout)
            self.item.setSizeHint(self.item_widget.sizeHint())
            self.ListWidget.addItem(self.item)
            self.ListWidget.setItemWidget(self.item, self.item_widget)

    def clicked(self):
        sender = self.sender()
        push_button = self.findChild(QPushButton, sender.objectName())
        t, i = push_button.objectName().split(" ")
        i = int(i)
        if push_button.isChecked():
            push_button.setText("On")
            self.alarmOn(i)
        else:
            push_button.setText("Off")
            self.alarmOff(i)

    def alarmOn(self, i):
        time_str = self.alarm_list[i]
        self.on_alarm.append(time_str)

    def alarmOff(self, i):
        time_str = self.alarm_list[i]
        try:
            self.on_alarm.remove(time_str)
        except:
            pass

    def addAlarm(self):
        t = self.time_edit.time().toString()
        t = t[:-3]
        self.alarm_list.append(t)
        self.ListWidget.clear()
        self.getAlarmList()

    def delAlarm(self):
        sender = self.sender()
        push_button = self.findChild(QPushButton, sender.objectName())
        t, i = push_button.objectName().split(" ")
        i = int(i)
        self.alarmOff(i)
        self.alarm_list.pop(i)
        self.ListWidget.clear()
        self.getAlarmList()

    def saveAlarm(self):
        data = ""
        for i in self.alarm_list:
            data = data + i + " "
        data = data + "\n"
        for i in self.on_alarm:
            data = data + i + " "
        data = data + "\n"
        cwd = os.getcwd()
        cwd = cwd + "/calendar"
        p = cwd + "/alarm.txt"
        try:
            with open(p, "w", encoding="utf-8") as file:
                file.write(data)
        finally:
            pass