# 엘레파츠 pi-cam kit 
# picam_switch.py
# QT app 전체화면 + GPIO 스위치 촬영 예제
# 본 예제는 app_capture2.py 예제 기반으로 제작(수정)되었습니다
# 원본 : https://github.com/raspberrypi/picamera2/blob/main/apps/app_capture2.py

from PyQt5 import QtCore
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QPushButton, QVBoxLayout, QWidget)

from picamera2 import Picamera2
from picamera2.previews.qt import QGlPicamera2
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

# GPIO 설정 / 스위치 핀 풀업
GPIO.setmode(GPIO.BCM)
GPIO.setup(camera_sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# 사진 저장 경로
save_dir = "/home/pi/Pictures/"

picam2 = Picamera2()

# preview 설정
preview_config = picam2.create_preview_configuration(main={"size": (Preview_width, Preview_height)},lores={"size": (window_width, window_height)}, display="lores")
picam2.configure(preview_config)

# capture 설정
capture_config = picam2.create_still_configuration(main={"size": (cam_width, cam_height)})


app = QApplication([])

# 스위치  촬영 함수 
def button_clicked(channel):

    now = datetime.now()
    timeStr = now.strftime("%Y%m%d-%H%M%S")
    picam2.switch_mode_and_capture_file(capture_config, save_dir+"picam_"+timeStr+".jpg")


# keep_ar=True : 화면 비율 고정, keep_ar=False : 채우기
qpicamera2 = QGlPicamera2(picam2, width=window_width, height=window_height, keep_ar=True)

window = QWidget()

# 함수 호출 이벤트 설정
GPIO.add_event_detect(camera_sw, GPIO.FALLING, callback=button_clicked, bouncetime=1500)        # GPIO 스위치 이벤트

# 위젯 설정, 배치
layout_h = QHBoxLayout()

layout_h.addWidget(qpicamera2)
window.setWindowTitle("Qt Picamera2 App")
window.showFullScreen()
window.setLayout(layout_h)

# 시작
picam2.start()
window.show()
app.exec()

