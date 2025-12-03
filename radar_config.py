#!/usr/bin/env python3
import serial
import time

ser = serial.Serial('/dev/serial0', 115200, timeout=1)

def send(cmd, data):
    frame = bytearray([0xAA, 0x55, cmd, len(data)])
    frame.extend(data)
    checksum = sum(frame) & 0xFF
    frame.append(checksum)
    ser.write(frame)
    time.sleep(0.05)
    print(f"Sent CMD=0x{cmd:02X}, DATA={data}, CHECKSUM=0x{checksum:02X}")

# 감지 거리 줄이기 (min=20cm, max=200cm)
send(0x05, [0x00, 0x14])    # minDistance = 20cm
send(0x05, [0x00, 0xC8])    # maxDistance = 200cm

# 민감도 낮추기 (0~100)
send(0x06, [25])

# Presence 유지시간 (1초)
send(0x07, [1])

# 부재 판정 딜레이 (1초)
send(0x08, [1])

# Motion Threshold (조금 큰 움직임만 감지)
send(0x09, [50])

print("Configuration sent.")