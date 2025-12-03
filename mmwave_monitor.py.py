#!/usr/bin/env python3
import time
import serial
import RPi.GPIO as GPIO

# ----- 설정 -----
SERIAL_PORT = "/dev/serial0"
BAUDRATE = 115200       # HMMD 기본값
OT2_PIN = 17            # BCM 번호 (물리 핀 11)

PRINT_INTERVAL = 0.2    # 초, 상태 출력 간격

# ----- 초기화 -----
GPIO.setmode(GPIO.BCM)
GPIO.setup(OT2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

ser = serial.Serial(
    SERIAL_PORT,
    BAUDRATE,
    timeout=0.05
)

def read_presence_gpio() -> bool:
    """OT2 핀에서 현재 사람 존재 여부 읽기 (True=있음, False=없음)."""
    return GPIO.input(OT2_PIN) == GPIO.HIGH

def read_uart_bytes() -> bytes:
    """UART에서 현재 들어온 바이트들 한 번에 읽기."""
    n = ser.in_waiting
    if n > 0:
        return ser.read(n)
    return b""

def main():
    print("HMMD mmWave Sensor monitor 시작")
    print(" - GPIO {pin} (OT2) 로 presence 읽기".format(pin=OT2_PIN))
    print(" - UART {port} @ {baud} 로 raw 데이터 읽기".format(
        port=SERIAL_PORT, baud=BAUDRATE
    ))
    print()

    last_presence = None
    last_print = 0.0

    try:
        while True:
            now = time.time()

            # 1) 현재 존재 여부 (OT2)
            presence = read_presence_gpio()

            # 2) UART 데이터 (디버깅용, hex로 보기)
            data = read_uart_bytes()
            hex_str = " ".join(f"{b:02X}" for b in data) if data else ""

            # 상태가 바뀌었거나, 일정 주기마다 한 번씩 출력
            if presence != last_presence or (now - last_print) > PRINT_INTERVAL:
                state = "🟢 감지됨 (PRESENT)" if presence else "⚪ 없음 (ABSENT)"
                ts = time.strftime("%H:%M:%S")

                if hex_str:
                    print(f"[{ts}] 상태: {state} | UART: {hex_str}")
                else:
                    print(f"[{ts}] 상태: {state}")

                last_presence = presence
                last_print = now

            time.sleep(0.02)

    except KeyboardInterrupt:
        print("\n종료합니다.")
    finally:
        ser.close()
        GPIO.cleanup()

if __name__ == "__main__":
    main()