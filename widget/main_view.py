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
        
        self.total_widget = QWidget()
        self.centralWidget(self.total_widget)
        
    def create_total_widget(self):
        name_lb = QLabel(parent=self.total_widget)
        name_lb.setGeometry(20,20)
        name_lb.setText("HE THONG HO TRO CANH BAO VI PHAM")
        
        
        self.image_lb = QLabel(parent=self.total_widget)
        self.image_lb.setGeometry(20,200)
        
        
