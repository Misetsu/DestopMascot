import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTime

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("List Item with button")
        self.setFixedSize(1000, 500)

        self.alarm_list = ["06:30", "07:00", "07:15"]
        self.on_alarm = []

        self.time = QLabel()

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

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.time, 0, 0, 8, 4)
        self.layout.addWidget(self.time_edit, 0, 4, 1, 3)
        self.layout.addWidget(self.add_alarm, 0, 7, 1, 1)
        self.layout.addWidget(self.Frame, 1, 4, 7, 4)
        self.getAlarmList()

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
        print(self.on_alarm)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = Window()
    widget.show()
    sys.exit(app.exec_())