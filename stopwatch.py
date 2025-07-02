import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
from PyQt5.QtCore import QTimer, QTime

# Load the UI file
Ui_MainWindow, QtBaseClass = uic.loadUiType("C:/Users/SBA/stopWatch.ui")

class StopwatchApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Initialize variables
        self.timer = QTimer(self)
        self.time = QTime(0, 0, 0, 0)
        self.running = False

        # Connect signals to slots
        self.timer.timeout.connect(self.update_time)
        self.start_button.clicked.connect(self.start_stopwatch)
        self.stop_button.clicked.connect(self.stop_stopwatch)
        self.reset_button.clicked.connect(self.reset_stopwatch)

    def start_stopwatch(self):
        if not self.running:
            self.timer.start(1)  # Update every millisecond
            self.running = True

    def stop_stopwatch(self):
        if self.running:
            self.timer.stop()
            self.running = False

    def reset_stopwatch(self):
        self.timer.stop()
        self.running = False
        self.time.setHMS(0, 0, 0, 0)
        self.time_label.setText(self.time.toString("hh:mm:ss.zzz"))

    def update_time(self):
        self.time = self.time.addMSecs(1)
        self.time_label.setText(self.time.toString("hh:mm:ss.zzz"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StopwatchApp()
    window.show()
    sys.exit(app.exec_())
