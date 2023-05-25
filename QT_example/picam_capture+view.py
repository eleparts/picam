# 엘레파츠 pi-cam kit 
# picam_capture+view.py
# QT app 전체화면 + LCD 화면 터치 버튼 + 마지막 촬영 사진 확인 기능(추가 창, 전체화면) 추가 예제 
# 본 예제는 app_capture2.py 예제 기반으로 제작(수정)되었습니다
# 원본 : https://github.com/raspberrypi/picamera2/blob/main/apps/app_capture2.py
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from picamera2 import Picamera2, Preview
from picamera2.previews.qt import QGlPicamera2
from libcamera import Transform, controls
from datetime import datetime
import RPi.GPIO as GPIO

#------ 해상도 설정 -------
# LCD 해상도, [WaveShare] 4.3inch DSI LCD : 800x480
window_width = 800
window_height = 480

# 미리보기용 (lores stream)해상도 설정, 2304x1296 권장 / 최대 해상도 설정 시 버퍼 용량 부족 문제 발생
# LCD 해상도(main stream)보다 커야 하며, 사진 해상도와 비율이 다른 경우 촬영 사진과 다른 이미지가 표시될 수 있습니다.
# 임의의 값 설정 시 카메라가 지원하는 해상도로 변경됩니다.
Preview_width = 2304
Preview_height = 1296

# 촬영 사진 해상도 4608*2592 (Raspberry Pi Camera Module 3)
cam_width = 4608
cam_height = 2592
#--------------------

# 사진 촬영 스위치 GPIO
camera_sw = 21

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(camera_sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# 사진 저장 경로
save_dir = "/home/pi/Pictures/"

# viewer 초기 이미지(No img)
imgname = "./eleparts.png" #"/usr/share/plymouth/themes/pix/splash.png"

picam2 = Picamera2()

# preview_configuration / 미리보기 설정
preview_config = picam2.create_preview_configuration(main={"size": (Preview_width, Preview_height)},lores={"size": (window_width, window_height)}, display="lores")
picam2.configure(preview_config)

# capture_config / 촬영 사진 설정
capture_config = picam2.create_still_configuration(main={"size": (cam_width, cam_height)})

# Autofocus set (Raspberry Pi Camera Module 3 자동 초첨 조절(오토포커스) 기능 on)
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})

app = QApplication([])

# 버튼 클릭(촬영) 및 종료(버튼 LOCK 해제) 함수 
def capture_clicked(channel):
    capture_button.setEnabled(False)
    GPIO.remove_event_detect(camera_sw)

    global imgname
    now = datetime.now()
    timeStr = now.strftime("%Y%m%d-%H%M%S")
    imgname = save_dir+"picam_"+timeStr+".jpg"
    picam2.switch_mode_and_capture_file(capture_config, imgname , signal_function=qpicamera2.signal_done)
    
def capture_done(job):
    picam2.wait(job)
    capture_button.setEnabled(True)
    GPIO.add_event_detect(camera_sw, GPIO.FALLING, callback=capture_clicked, bouncetime=1500)

def view_lastimg():     # 마지막으로 촬영한 사진 보기
    img_window.lastImgView()
    img_window.setWindowTitle("image_viewer")
    img_window.showFullScreen()
    img_window.show()

# 촬영 사진 확인용 viewer 구성 클래스
class imgWindow(QWidget):

    def __init__(self):
        super(imgWindow, self).__init__()
        self.setGeometry(0, 0, window_width, window_height)

        # viewer 창 구성 설정
        self.img_layout_h = QHBoxLayout()
        self.img_layout_v = QVBoxLayout()

        self.laststill = QLabel(self)

        self.closd_button = QPushButton("Close")
        self.closd_button.setMaximumHeight(window_height)

        self.img_layout_h.addWidget(self.laststill, 10)
        self.img_layout_h.addLayout(self.img_layout_v, 1)
        self.img_layout_v.addWidget(self.closd_button)

        self.setLayout(self.img_layout_h)

        self.closd_button.clicked.connect(self.closeViewer)

    def lastImgView(self):          # viewer 이미지(마지막 촬영 사진) 불러오기 구성
        global imgname
         
        self.pixmap = QPixmap(imgname)
        self.pixmap = self.pixmap.scaledToHeight(window_height*0.8)
        self.laststill.setScaledContents(True) 
        self.laststill.setPixmap(QPixmap(self.pixmap)) 

    def closeViewer(self):
        self.close()

# keep_ar=True : 화면 비율 고정, keep_ar=False : 채우기
qpicamera2 = QGlPicamera2(picam2, width=window_width, height=window_height, keep_ar=False)

capture_button = QPushButton("Capture")                 # 버튼 
capture_button.setMaximumHeight(window_height*2/3)      # 버튼 높이 조절 window_height = LCD 높이
viewer_button = QPushButton("Pic_view") 
viewer_button.setMaximumHeight(window_height/3)

window = QWidget()
img_window = imgWindow()

# 함수 호출 동작 설정
GPIO.add_event_detect(camera_sw, GPIO.FALLING, callback=capture_clicked, bouncetime=1500)   # GPIO 스위치 이벤트
capture_button.clicked.connect(capture_clicked)                                             # 화면 터치 
qpicamera2.done_signal.connect(capture_done)
viewer_button.clicked.connect(view_lastimg)

# 위젯 설정, 배치
layout_h = QHBoxLayout()
layout_v = QVBoxLayout()

layout_h.addWidget(qpicamera2, 10)
layout_h.addLayout(layout_v, 1)
layout_v.addWidget(capture_button)
layout_v.addWidget(viewer_button)

window.setWindowTitle("Qt Picamera2 App")
window.showFullScreen()
window.setLayout(layout_h)

# 시작
picam2.start()
window.show()
app.exec()

