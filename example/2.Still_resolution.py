'''
# 엘레파츠 pi-cam kit
# 2. 간단 사진 촬영 테스트 예제
# 사진 촬영 1회 후 종료합니다.
# 사진의 해상도를 직접 설정할 수 있습니다. (카메라 지원 해상도 이내)
'''
from picamera2 import Picamera2

# 사진 사이즈 (카메라 성능 참조, PI camera 3 max 4608x2592)
cam_width = 4608
cam_height = 2592

# 사진 저장 경로
save_dir = "/home/pi/Pictures/"


picam2 = Picamera2()

# still 사진 해상도 설정하기
capture_config = picam2.create_still_configuration(main={"size": (cam_width, cam_height)},encode="main")
picam2.configure(capture_config)

picam2.start()

# svae_dirs 경로에 저장
picam2.capture_file(save_dir+"still.jpg")

picam2.stop()
