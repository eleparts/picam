'''
# 엘레파츠 pi-cam kit
# 2. 사진 촬영 간단 테스트 예제
# 사진 촬영 1회 후 종료합니다.
# 사진의 해상도를 직접 설정할 수 있습니다. (카메라 지원 해상도 이내)
'''
from picamera2 import Picamera2

# 사진 사이즈 (카메라 성능 참조, PI camera 3 max 4608x2592)
cam_width = 4608
cam_height = 2592


picam2 = Picamera2()

# still 사진 해상도 설정하기
capture_config = picam2.create_still_configuration(main={"size": (cam_width, cam_height)},encode="main")
picam2.configure(capture_config)

picam2.start()

# /home/pi/Pictures 경로에 저장
picam2.capture_file("/home/pi/Pictures/still.jpg")

picam2.stop()
