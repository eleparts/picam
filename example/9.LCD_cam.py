'''
# 엘레파츠 pi-cam kit 
# 8.LCD + 스위치를 이용한 사진 반복 촬영 테스트 예제
# LCD에 미리보기를 출력하다가 스위치를 누르면 사진을 촬영 합니다.
# QTGL Preview(미리보기) 기능은 LCD가 없으면 실행되지 않습니다. LCD(모니터) 및 VNC 환경에서만 실행됩니다.
# 자동 종료되지 않으므로 예제를 실행한 창에서 Ctrl + C 를 눌러 종료 합니다.
'''
import RPi.GPIO as GPIO
from picamera2 import Picamera2, Preview
from libcamera import Transform, controls
from datetime import datetime
import time

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

# 사진 저장 경로
save_dir = "/home/pi/Pictures/"


# GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(camera_sw,GPIO.IN, pull_up_down=GPIO.PUD_UP)

# camera
picam2 = Picamera2()

# preview_configuration / 미리보기 설정
preview_config=picam2.create_preview_configuration(main={"size": (Preview_width, Preview_height)},lores={"size": (window_width, window_height)}, display="lores")
picam2.configure(preview_config)

# still_configuration / 촬영 사진 설정
capture_config = picam2.create_still_configuration(main={"size": (cam_width, cam_height)})

# Autofocus set (Raspberry Pi Camera Module 3 자동 초첨 조절(오토포커스) 기능 on)
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})

#picam2.start_preview(Preview.QTGL, 미리보기 창 설정)
picam2.start_preview(Preview.QTGL, x=0, y=1, width=window_width, height=window_height)

picam2.start()

try:
    while True:

        # 스위치가 눌릴 때까지 대기
        if(GPIO.input(camera_sw) == 0):     # 스위치 입력

            # 연속 촬영을 위해 파일명에 날짜 추가, 문자열 작성
            now = datetime.now()
            timeStr = now.strftime("%Y%m%d-%H%M%S")

            # 사진 촬영, svae_dir 경로에 저장
            picam2.switch_mode_and_capture_file(capture_config, save_dir+"picam_"+timeStr+".jpg")
            time.sleep(0.5)

        time.sleep(0.1)

except KeyboardInterrupt:

    picam2.stop()
    GPIO.cleanup()
