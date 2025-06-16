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
from tool import face_detection,camera,voice
from PyQt6.QtGui import QPixmap, QImage, QIcon
from PyQt6.QtCore import QSize, Qt, QThread
import cv2
import sys
import time
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
        self.camera_state = 0

        self.thread2 = QThread()
        self.voice = voice.CobraDemo(library_path=None,
        access_key="4H7XExZ76UQe2E4SFAM7vsItIZgSLrbmvA2A0psSaM/eLi9mvIPGgQ==",
        output_path=None,
        input_device_index=-1)
        self.voice.moveToThread(self.thread2)
        self.voice.voiceCapture.connect(self.process_voice)
        self.thread2.started.connect(self.voice.run)
        self.thread2.start()
        self.voice_state = 0

        
        self.cap = cv2.VideoCapture(0)

        self.create_total_widget()
        self.run()
    def create_total_widget(self):
        name_lb = QLabel(parent=self.total_widget)
        name_lb.move(20,20)
        name_lb.setStyleSheet("font-size: 96px;")
        name_lb.setText("HỆ THỐNG HỖ TRỢ CẢNH BÁO VI PHẠM")
        
        
        self.image_lb = QLabel(parent=self.total_widget)
        self.image_lb.setGeometry(200,200,800,800)
        name_lb = QLabel(parent=self.total_widget)
        name_lb.move(1200,200)
        name_lb.setStyleSheet("font-size: 60px;")
        name_lb.setText("CẢNH BÁO VI PHẠM")
        

        self.labels = []
        text = ["Đang tập trung","Không có ai trong camera","Có người khác trong camera","Đang nhìn sang hướng khác", "Đang buồn ngủ","Đang ngủ","Có tiếng nói gần đó"]
        for i in range(7):
            temp = QLabel(parent=self.total_widget)
            temp.move(1200,250+(i+1)*50)
            temp.setStyleSheet("font-size: 30px; color: blue;")
            temp.setText(text[i])
            temp.setDisabled(True)
            self.labels.append(temp)
        self.exit_bt = QPushButton(parent=self.total_widget)
        self.exit_bt.setText("Thoát")
        self.exit_bt.move(1200,900)
        self.exit_bt.clicked.connect(self.thoat)
        
    
    def thoat(self):

        self.cameraWorker.stop()
        self.thread.quit()
        self.thread.wait()
        
        self.thread2.quit()
        self.thread2.wait()
        
        sys.exit()
    
    def process_voice(self, state):
        print(state)
        if self.voice_state != state:
            
            if state == 1:
                self.labels[6].setStyleSheet("font-size: 30px; color: red;")
            else:
                self.labels[6].setStyleSheet("font-size: 30px; color: blue;")
            self.voice_state = state
            
    def processFrame(self, data):
        # Convert the frame to a format that Qt can use
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame, state = data
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        if state != self.camera_state:
            for i in self.labels:
                i.setStyleSheet("font-size: 30px; color: blue;")
            self.labels[state].setStyleSheet("font-size: 30px; color: red;")
            # if state == 1:
            #     text = current_time+": Không có ai trong camera"
            # elif state == 2:
            #     text = current_time+": Có người khác trong camera"
            # elif state == 3:
            #     text = current_time+": Đang nhìn sang hướng khác"
            # elif state == 4:
            #     text = current_time+": Đang buồn ngủ"
            # elif state == 5:
            #     text = current_time+": Đang ngủ"
            # else:
            #     text = "Đang tập trung"
            # self.message.setText(text+"\n"+self.message.toPlainText())
            self.camera_state = state
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

        

        
        
