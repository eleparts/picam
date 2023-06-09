'''
# 엘레파츠 pi-cam kit 
# 7.PIR 센서 연동 사진 반복 촬영 테스트 예제
# PIR 센서에 물체가 감지되면 사진을 촬영 합니다.
# ※ PIR 센서는 적외선을 측정해 감지 범위 내 적외선 값의 변화를 감지(물체 움직임 인식)하는 기능을 수행 합니다.
# 자동 종료되지 않으므로 예제를 실행한 터미널창에서 Ctrl + C 를 눌러 종료 합니다.
'''
import RPi.GPIO as GPIO
from picamera2 import Picamera2
from datetime import datetime
import time

# PIR 센서 출력 스위치 GPIO / Active HIGH
PIR_detect = 26

# 사진 저장 경로
save_dir = "/home/pi/Pictures/"


# GPIO / 풀다운
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_detect,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

picam2 = Picamera2()

# 사진 촬영 함수 사용을 위한 설정 함수
capture_config = picam2.create_still_configuration()
picam2.configure(capture_config)

picam2.start()

try:
    # PIR 센서 입력 대기 
    while True:

        if(GPIO.input(PIR_detect) == 1):        # PIR 센서 입력

            # PIR 감지-카메라 촬영 시점 조절을 위한 촬영 딜레이 / 필요에 따라 사용&수정
            # time.sleep(2) 

            # 연속 촬영을 위해 파일명에 날짜 추가, 문자열 작성
            now = datetime.now()
            timeStr = now.strftime("%Y%m%d-%H%M%S")

            # 사진 촬영, svae_dir 경로에 저장
            picam2.capture_file(save_dir+"still_"+timeStr+".jpg")

            while(GPIO.input(PIR_detect) == 1):    # 연속 촬영 방지, PIR 센서 OFF 대기
                time.sleep(0.1)

        time.sleep(0.1)

except KeyboardInterrupt:

    picam2.stop()
    GPIO.cleanup()

