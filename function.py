import sys
from PyQt5.QtWidgets import *

class MyWidget(QWidget):
    def __init__(self):
        super(MyWidget, self).__init__()

        self.setFixedSize(1000, 500)
        self.button = QPushButton("change")
        self.button.clicked.connect(self.change_layout)

        self.stack1 = QWidget()
        self.stack2 = QWidget()

        self.stack1UI()
        self.stack2UI()

        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack2)

        layout = QGridLayout(self)
        layout.addWidget(self.Stack, 1, 0, 1, 5)
        layout.addWidget(self.button, 2, 4)

        self.setLayout(layout)

    def change_layout(self):
        i = self.Stack.currentIndex()
        if i == 1:
            self.Stack.setCurrentIndex(0)
        else:
            self.Stack.setCurrentIndex(1)

    def stack1UI(self):
        layout = QFormLayout()
        layout.addRow("Name", QLineEdit())
        layout.addRow("Address", QLineEdit())
        self.stack1.setLayout(layout)

    def stack2UI(self):
        layout = QFormLayout()
        sex = QHBoxLayout()
        sex.addWidget(QRadioButton("Male"))
        sex.addWidget(QRadioButton("Female"))
        layout.addRow(QLabel("Sex"), sex)
        layout.addRow("Date of Birth", QLineEdit())
        self.stack2.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())
