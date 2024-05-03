import sys
from PyQt6.QtWidgets import QApplication
from app import App


def __init__():

    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    __init__()
