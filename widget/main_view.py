from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QWidget,QLayout,
    QFileDialog,QMessageBox
)

from PyQt6.QtGui import QPixmap, QImage, QIcon
from PyQt6.QtCore import QSize, Qt

class mainView(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("Cheating Detection")
        size = (1920,1080)
        self.setMinimumSize(*size)
        self.centralWidget()