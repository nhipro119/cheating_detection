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
    QFileDialog,QMessageBox,
    QTextEdit, QGraphicsPixmapItem
)
from tool import face_detection,camera
from PyQt6.QtGui import QPixmap, QImage, QIcon
from PyQt6.QtCore import QSize, Qt, QThread
import cv2

class mainView(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("Cheating Detection")
        size = (1920,1080)
        self.setMinimumSize(*size)
        
        self.total_widget = QWidget()
        self.setCentralWidget(self.total_widget)
        
        self.thread = QThread()
        self.cameraWorker = camera.CameraWorker()
        self.cameraWorker.moveToThread(self.thread)
        self.cameraWorker.frameCaptured.connect(self.processFrame)
        self.thread.started.connect(self.cameraWorker.run)
        self.thread.start()


        self.detect_face = face_detection.Face_detector()
        self.cap = cv2.VideoCapture(0)

        self.create_total_widget()
        self.run()
    def create_total_widget(self):
        name_lb = QLabel(parent=self.total_widget)
        name_lb.move(20,20)
        name_lb.setText("HỆ THỐNG HỖ TRỢ CẢNH BÁO VI PHẠM")
        
        
        self.image_lb = QLabel(parent=self.total_widget)
        self.image_lb.setGeometry(200,200,900,900)
        
        self.message = QTextEdit(parent=self.total_widget)
        self.message.setGeometry(1200,200,500,500)

        self.exit_bt = QPushButton(parent=self.total_widget)
        self.exit_bt.setText("Thoát")
        self.exit_bt.move(1200,900)
        self.scenePixmapItem = None
    def processFrame(self, frame):
        # Convert the frame to a format that Qt can use
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        text,frame = self.detect_face.face_detect(frame)
        image = QImage(
            frame.data,
            frame.shape[1],
            frame.shape[0],
            QImage.Format.Format_BGR888,
        )
        pixmap = QPixmap.fromImage(image)
        self.image_lb.setPixmap(pixmap)
        # if self.scenePixmapItem is None:
        #     self.scenePixmapItem = QGraphicsPixmapItem(pixmap)
        #     self.scene.addItem(self.scenePixmapItem)
        #     self.scenePixmapItem.setZValue(0)
        #     self.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        # else:
        #     self.scenePixmapItem.setPixmap(pixmap)
    def stopCamera(self):
        self.cameraWorker.stop()
        self.thread.quit()
        self.thread.wait()
    def run(self):
        pass
        # while self.cap.isOpened():
        #     success, image = self.cap.read()
        #     text,image = self.detect_face.face_detect(image)
        #     w,h,ch = image.shape
        #     bytes_per_line = ch * w
        #     convert_to_Qt_format = QImage(image.data, 900, 900, bytes_per_line, QImage.Format.Format_RGB888)
        #     self.image_lb.setPixmap(QPixmap.fromImage(convert_to_Qt_format))

        

        
        
