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
from PyQt6.QtCore import QSize, Qt, QThread, QTimer, QTime
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
        self.total_widget.setStyleSheet("background-color:#2b2b2b;")
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

        #create a time countdown
        self.remaining_minutes = 25
        self.learning_time = 1
        self.timer = QTimer()
        self.timer.timeout.connect(self.time_countdown)
        self.timer.start(60000)
        self.run()
    

    def create_total_widget(self):
        name_lb = QLabel(parent=self.total_widget)
        name_lb.move(20,20)
        name_lb.setStyleSheet("font-size: 96px; color:white;")
        name_lb.setText("Hệ thống hỗ trợ tập trung học tập")
        
        
        self.image_lb = QLabel(parent=self.total_widget)
        self.image_lb.setGeometry(200,200,800,800)
        right_panel = QVBoxLayout()


        self.pomodoro_label = QLabel("Chu kỳ Pomodoro: Giờ học")
        self.pomodoro_label.setStyleSheet("color: white; font-size: 50px;")
        right_panel.addWidget(self.pomodoro_label)

        self.time_label = QLabel("25 Phút")
        self.time_label.setStyleSheet("color: white; font-size: 80px; font-weight: bold;")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_panel.addWidget(self.time_label)

        self.warning_label = QLabel("Cảnh báo:")
        self.warning_label.setStyleSheet("color: white; font-size: 60px;")
        right_panel.addWidget(self.warning_label)

        self.labels = []
        text = ["Đang tập trung","Có tiếng nói gần đó"]
        for i in range(2):
            temp = QLabel()
            temp.move(1200,450+(i+1)*50)
            temp.setStyleSheet("font-size: 60px; color: blue;")
            temp.setText(text[i])
            temp.setDisabled(True)
            right_panel.addWidget(temp)
            self.labels.append(temp)
        right_panel.addStretch()
        right_widget = QWidget(parent=self.total_widget)
        right_widget.setLayout(right_panel)
        right_widget.setStyleSheet("background-color: #3c3f41; padding: 20px;")
        right_widget.setGeometry(1100,200,700,700)
        self.exit_button = QPushButton("Thoát",parent=self.total_widget)
        self.exit_button.setStyleSheet("background-color: red; color: white; font-size: 40px; padding: 6px;")
        self.exit_button.clicked.connect(self.close)
        self.exit_button.move(1700,900)
        self.exit_button.clicked.connect(self.thoat)

        
        
    
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
                self.labels[1].setStyleSheet("font-size: 30px; color: red;")
            else:
                self.labels[1].setStyleSheet("font-size: 30px; color: blue;")
            self.voice_state = state
            
    def processFrame(self, data):
        # Convert the frame to a format that Qt can use
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame, state = data
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        if state != self.camera_state:
            for i in self.labels:
                i.setStyleSheet("font-size: 60px; color: blue;")
            if state != 0:
                self.labels[0].setStyleSheet("font-size: 60px; color: red;")
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
    def time_countdown(self):
        self.remaining_minutes -= 1
        if self.remaining_minutes == 0:
            self.learning_time *= -1
            if self.learning_time == 1:

                self.remaining_minutes = 25
                self.pomodoro_label.setText("Chu kỳ Pomodoro: Giờ học")
                
            else:
                self.pomodoro_label.setText("Chu kỳ Pomodoro: Giờ nghỉ")
                self.remaining_minutes = 5
        self.time_label.setText(f"{self.remaining_minutes} Phút")
    

        
        
