'''
# 엘레파츠 pi-cam kit 
# 5.PIR 센서 + 부저 연동 사진 촬영 예제 
# PIR 센서에 물체가 감지되면 부저로 알리고 사진을 촬영 후 종료합니다.
'''
import RPi.GPIO as GPIO
from picamera2 import Picamera2
import time

# GPIO 핀
PIR_detect = 26     # PIR 센서 출력 스위치 GPIO / Active HIGH
buzzer = 19         # 부저 출력 GPIO

# 사진 저장 경로
save_dir = "/home/pi/Pictures/"


# GPIO / PIR = IN & 풀다운 / 부저 OUT & LOW 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_detect, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.output(buzzer, GPIO.LOW)

picam2 = Picamera2()

# PIR 센서에서 신호가 올 때까지 대기, 신호가 오면 반복문 (대기)종료
while(GPIO.input(PIR_detect) == 0): 
    time.sleep(0.1)


# 부저를 0.1초 짧게 울림
GPIO.output(buzzer, GPIO.HIGH)
time.sleep(0.1)
GPIO.output(buzzer, GPIO.LOW)

# 사진 촬영, svae_dir 경로에 사진 저장
picam2.start_and_capture_file(save_dir+"still.jpg")

picam2.stop()
GPIO.cleanup()
