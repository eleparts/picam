'''
# 엘레파츠 pi-cam kit 
# 3. 사진 촬영 간단 테스트 예제
# 스위치를 누르면 사진을 촬영 후 종료합니다.
'''
import RPi.GPIO as GPIO
from picamera2 import Picamera2
import datetime
import time

# 사진 촬영 스위치 GPIO / Active LOW
camera_sw = 21

# GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(camera_sw,GPIO.IN, pull_up_down=GPIO.PUD_UP)

picam2 = Picamera2()

# 스위치가 눌릴 때까지 대기
while(GPIO.input(camera_sw) == 1):    
    time.sleep(0.1)


# 현재 경로에 저장
# picam2.start_and_capture_file("still.jpg")

# /home/pi/Pictures 경로에 저장
picam2.start_and_capture_file("/home/pi/Pictures/still.jpg")

picam2.stop()

GPIO.cleanup()