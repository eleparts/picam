'''
# 엘레파츠 pi-cam kit 
# 1-1. 사진 촬영 간단 테스트 예제
# 사진 촬영 1회 후 종료합니다.
'''

from picamera2 import Picamera2
import datetime


picam2 = Picamera2()

# 현재 경로에 저장
# picam2.start_and_capture_file("still.jpg")

# /home/pi/Pictures 경로에 저장
picam2.start_and_capture_file("/home/pi/Pictures/still.jpg")

picam2.stop()


