'''
# 엘레파츠 pi-cam kit 
# 4. PIR 센서 연동 사진 촬영 예제
# PIR 센서에 물체가 감지되면 사진을 촬영 후 종료합니다.
'''
import RPi.GPIO as GPIO
from picamera2 import Picamera2
import time

# PIR 센서 출력 스위치 GPIO / Active HIGH
PIR_detect = 20

# 사진 저장 경로
save_dir = "/home/pi/Pictures/"

# GPIO / 풀다운
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_detect, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


picam2 = Picamera2()

# 스위치가 눌릴 때까지 대기
while(GPIO.input(PIR_detect) == 0):    
    time.sleep(0.1)

# /home/pi/Pictures 경로에 저장
picam2.start_and_capture_file(save_dir+"still.jpg")

picam2.stop()
