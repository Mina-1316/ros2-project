import sys
import threading
import time
from dataclasses import dataclass

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QMainWindow, QGridLayout, QLabel, QWidget

thread = None

@dataclass
class Keys:
    linear: float = 0.0
    angular: float = 0.0
    coord: tuple = (0, 0)
    text: str = ""

keyMappings = {
    Qt.Key_U: Keys(1.0, 45.0, (0, 0), 'U'),
    Qt.Key_I: Keys(1.0, 0.0, (0, 1), 'I'),
    Qt.Key_O: Keys(1.0, -45.0, (0, 2), 'O'),
    Qt.Key_J: Keys(0.0, 45.0, (1, 0), 'J'),
    Qt.Key_K: Keys(0.0, 0.0, (1, 1), 'K'),
    Qt.Key_L: Keys(0.0, -45.0, (1, 2), 'L'),
    Qt.Key_M: Keys(-1.0, 45.0, (2, 0), 'M'),
    Qt.Key_Comma: Keys(-1.0, 0.0, (2, 1), ','),
    Qt.Key_Period: Keys(-1.0, -45.0, (2, 2), '.'),
}


class KeyboardGui:
    QLABEL_KEYPRESS_STYLE = "color: white; background-color: blue;"
    QLABEL_KEYRELEASE_STYLE = "color: black; background-color: white;"

    def __init__(self):
        global thread
        self.app = None
        self.impl_ = None
        thread = threading.Thread(target=self.run)
        thread.start()

    def run(self):
        self.app = QApplication(sys.argv)
        self.impl_ = KeyboardGui.Impl()
        self.impl_.show()

        sys.exit(self.app.exec_())

    @property
    def linear_velocity(self):
        return self.impl_.linear_velocity

    @property
    def angular_velocity(self):
        return self.impl_.angular_velocity


    class Impl(QMainWindow):
        widgets = {}

        def __init__(self):
            super().__init__()
            self._linear_velocity = 0.0
            self._angular_velocity = 0.0

            self.setWindowTitle("Keyboard GUI")
            self.layout = QGridLayout()
            # Create a buttons with setting linear/angular velocity updates when pressed
            for key, value in keyMappings.items():
                label = QLabel(value.text)
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet(KeyboardGui.QLABEL_KEYRELEASE_STYLE)
                self.layout.addWidget(label, *value.coord)
                self.widgets[key] = label

            widget = QWidget()
            widget.setLayout(self.layout)
            self.setCentralWidget(widget)

        def keyPressEvent(self, event):
            if event.key() in self.widgets:
                self.widgets[event.key()].setStyleSheet(KeyboardGui.QLABEL_KEYPRESS_STYLE)
                self._linear_velocity = keyMappings[event.key()].linear
                self._angular_velocity = keyMappings[event.key()].angular

            elif event.key() == Qt.Key_Q:
                print("Q key pressed, closing the application")
                self.close()
                return
            else:
                self._linear_velocity = 0.0
                self._angular_velocity = 0.0

        def keyReleaseEvent(self, event):
            if event.key() in self.widgets:
                self.widgets[event.key()].setStyleSheet(KeyboardGui.QLABEL_KEYRELEASE_STYLE)

        @property
        def linear_velocity(self):
            return self._linear_velocity

        @property
        def angular_velocity(self):
            return self._angular_velocity

def main():
    sensor = KeyboardGui()
    print("Thread info: ", thread)
    for i in range(100):
        if threading.active_count() == 1:
            print("Keyboard GUI thread is closed")
            break
        time.sleep(1.0)
        print("Linear velocity: ", sensor.linear_velocity, "Angular velocity: ", sensor.angular_velocity)

    print("Thread info: ", thread)

if __name__ == "__main__":
    main()




