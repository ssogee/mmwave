#!/usr/bin/env python3
import serial, time

ser = serial.Serial('/dev/serial0', 115200, timeout=1)

def send(cmd, data=[]):
    frame = bytearray([0xAA, 0x55, cmd, len(data)])
    frame.extend(data)
    checksum = sum(frame) & 0xFF
    frame.append(checksum)
    ser.write(frame)
    time.sleep(0.05)
    print(f"CMD=0x{cmd:02X}, DATA={data}, CHECKSUM=0x{checksum:02X}")

print("=== Enter config mode ===")
send(0x09)

# -----------------------------
# Custom Setting (너가 원하는 값)
# -----------------------------

# 1) 거리 설정 (min=20cm, max=200cm)
send(0x05, [0x00, 20])    # Min dist = 20cm
send(0x05, [0x00, 200])   # Max dist = 200cm

# 2) 민감도 낮게 (둔하게)
send(0x06, [20])  # 0~100

# 3) Presence hold (1초)
send(0x07, [1])

# 4) Absence timeout (1초)
send(0x08, [1])

# 5) Motion threshold = 50 (중간)
send(0x10, [50])

print("=== Exit config mode ===")
send(0x0A)

print("All config sent.")