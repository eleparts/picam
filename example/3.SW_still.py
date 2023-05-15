'''
# 엘레파츠 pi-cam kit 
# 3.스위치를 이용한 사진 촬영 테스트 예제
# 스위치를 누르면 사진을 촬영 후 종료합니다.
'''
import RPi.GPIO as GPIO
from picamera2 import Picamera2
import time

# 사진 촬영 스위치 GPIO / Active LOW
camera_sw = 21

# 사진 저장 경로
save_dir = "/home/pi/Pictures/"


# GPIO / camera_sw 핀 풀업
GPIO.setmode(GPIO.BCM)
GPIO.setup(camera_sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)

picam2 = Picamera2()

# 스위치가 눌릴 때까지 대기, 스위치가 눌리면 반복문 (대기)종료
while(GPIO.input(camera_sw) == 1):    
    time.sleep(0.1)

# svae_dir 경로에 저장
picam2.start_and_capture_file(save_dir+"still.jpg")

picam2.stop()
GPIO.cleanup()