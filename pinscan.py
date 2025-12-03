#!/usr/bin/env python3
import time
import RPi.GPIO as GPIO

# 후보 핀들 (17 말고도 몇 개 같이 체크)
PINS = [4, 17, 18, 22, 23, 24, 27]

GPIO.setmode(GPIO.BCM)
for p in PINS:
    GPIO.setup(p, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("센서 앞에서 움직이거나 멀리 가보면서 값 변화를 보자")
print("Ctrl+C 로 종료")

try:
    while True:
        states = []
        for p in PINS:
            v = GPIO.input(p)
            states.append(f"{p}:{v}")
        print(" | ".join(states), end="\r")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n종료")
finally:
    GPIO.cleanup()