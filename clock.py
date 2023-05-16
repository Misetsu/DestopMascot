from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer, QTime, QSize
from PyQt5.QtGui import *

class Clock(QDialog):
    def __init__(self, *args, **kwargs):
        super(Clock, self).__init__(*args, **kwargs)
        self.setObjectName('Custom_Dialog')
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setGeometry(1450, 710, 400, 100)
        self.setStyleSheet(Stylesheet)
        self.initUi()

    def initUi(self):
        # Important: this widget is used as background and rounded corners.
        self.widget = QWidget(self)
        self.widget.setObjectName('Custom_Widget')
        layout = QVBoxLayout(self)
        layout.addWidget(self.widget)

        # Add user interface to widget
        layout = QGridLayout(self.widget)
        layout.addItem(QSpacerItem(40, 20), 0, 0)
        close = QPushButton("r", self)
        close.clicked.connect(self.accept)
        close.setObjectName("closeButton")
        alarm = QPushButton("a", self)
        alarm.setObjectName("alarmButton")
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont('Arial', 30))
        layout.addWidget(self.label, 0, 0, 2, 1)
        layout.addWidget(close, 0, 1)
        layout.addWidget(alarm, 1, 1)
        self.setLayout(layout)
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

    def showTime(self):
        current_time = QTime.currentTime()
        label_time = current_time.toString("hh:mm:ss")
        self.label.setText(label_time)

    def sizeHint(self):
        return QSize(400, 100)

Stylesheet = """
#Custom_Widget {
    background: #CCC;
    border-radius: 20px;
    opacity: 100;
    border: 3px solid #1c3561;                   
}
#closeButton {
    min-width: 36px;
    min-height: 36px;
    max-width: 36px;
    max-height: 36px;
    font-family: "Webdings";
    qproperty-text: "r";
    border-radius: 10px;
}
#closeButton:hover {
    color: #ccc;
    background: red;
}
#alarmButton {
    min-width: 36px;
    min-height: 36px;
    max-width: 36px;
    max-height: 36px;
    font-family: "Webdings";
    qproperty-text: "r";
    border-radius: 10px;
}
#alarmButton:hover {
    color: #ccc;
    background: #1c3561;
}
"""