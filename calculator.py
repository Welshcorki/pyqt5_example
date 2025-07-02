import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt
from PyQt5 import uic

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("C:/Users/SBA/github/pyqt5_example/calc_1.ui", self)

        # Connect button signals to slots
        self.btn_0.clicked.connect(self.button_clicked)
        self.btn_1.clicked.connect(self.button_clicked)
        self.btn_2.clicked.connect(self.button_clicked)
        self.btn_3.clicked.connect(self.button_clicked)
        self.btn_4.clicked.connect(self.button_clicked)
        self.btn_5.clicked.connect(self.button_clicked)
        self.btn_6.clicked.connect(self.button_clicked)
        self.btn_7.clicked.connect(self.button_clicked)
        self.btn_8.clicked.connect(self.button_clicked)
        self.btn_9.clicked.connect(self.button_clicked)
        self.btn_dot.clicked.connect(self.button_clicked)

        self.btn_add.clicked.connect(self.button_clicked)
        self.btn_sub.clicked.connect(self.button_clicked)
        self.btn_mul.clicked.connect(self.button_clicked)
        self.btn_div.clicked.connect(self.button_clicked)

        self.btn_eq.clicked.connect(self.calculate)
        self.btn_c.clicked.connect(self.clear_all)
        self.btn_ce.clicked.connect(self.clear_entry)
        self.btn_backspace.clicked.connect(self.backspace)

        self.show()

    def button_clicked(self):
        button = self.sender()
        current_text = self.display.text()

        if current_text == "0":
            self.display.setText(button.text())
        else:
            self.display.setText(current_text + button.text())

    def calculate(self):
        try:
            # Replace symbols for eval
            text = self.display.text().replace("×", "*").replace("÷", "/")
            result = eval(text)
            self.display.setText(str(result))
        except Exception as e:
            self.display.setText("Error")

    def clear_all(self):
        self.display.setText("0")

    def clear_entry(self):
        self.display.setText("0")

    def backspace(self):
        current_text = self.display.text()
        if len(current_text) > 1:
            self.display.setText(current_text[:-1])
        else:
            self.display.setText("0")

    def keyPressEvent(self, event):
        key = event.key()
        text = event.text()

        if Qt.Key_0 <= key <= Qt.Key_9:
            if self.display.text() == "0":
                self.display.setText(text)
            else:
                self.display.setText(self.display.text() + text)
        elif key in [Qt.Key_Plus, Qt.Key_Minus, Qt.Key_Asterisk, Qt.Key_Slash]:
            self.display.setText(self.display.text() + text)
        elif key in [Qt.Key_Return, Qt.Key_Enter]:
            self.calculate()
        elif key == Qt.Key_Backspace:
            self.backspace()
        elif key == Qt.Key_Escape:
            self.clear_all()
        elif key == Qt.Key_Period:
            if '.' not in self.display.text():
                self.display.setText(self.display.text() + '.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    sys.exit(app.exec_())
