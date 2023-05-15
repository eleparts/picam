'''
# 엘레파츠 pi-cam kit 
# 6.스위치를 이용한 사진 반복 촬영 테스트 예제
# 스위치를 누르면 사진을 촬영 합니다.
# 자동 종료되지 않으므로 예제를 실행한 터미널창에서 Ctrl + C 를 눌러 종료 합니다.
'''
import RPi.GPIO as GPIO
from picamera2 import Picamera2
from datetime import datetime
import time

# 사진 촬영 스위치 GPIO / Active LOW
camera_sw = 21

# 사진 저장 경로
save_dir = "/home/pi/Pictures/"


# GPIO / 풀업
GPIO.setmode(GPIO.BCM)
GPIO.setup(camera_sw,GPIO.IN, pull_up_down=GPIO.PUD_UP)

picam2 = Picamera2()

# 사진 촬영 함수 사용을 위한 설정 함수
capture_config = picam2.create_still_configuration()
picam2.configure(capture_config)

picam2.start()

try:
    # 스위치가 눌릴 때까지 대기
    while True:

        if(GPIO.input(camera_sw) == 0):     # 스위치 입력

            # 연속 촬영을 위한 파일명에 날짜 추가
            now = datetime.now()
            timeStr = now.strftime("%Y%m%d-%H%M%S")

            # svae_dir 경로에 저장
            picam2.capture_file(save_dir+"still_"+timeStr+".jpg")
            time.sleep(0.5)

        time.sleep(0.1)

except KeyboardInterrupt:

    picam2.stop()
    GPIO.cleanup()

