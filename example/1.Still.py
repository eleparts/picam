'''
# 엘레파츠 pi-cam kit 
# 1. 간단 사진 촬영 테스트 예제
# 사진 촬영 1회 후 종료합니다.
'''
from picamera2 import Picamera2

# 사진 저장 경로
save_dir = "/home/pi/Pictures/"


picam2 = Picamera2()

# svae_dir 경로에 저장
picam2.start_and_capture_file(save_dir+"still.jpg")

picam2.stop()


