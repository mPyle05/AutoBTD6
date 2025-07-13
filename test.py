import pyautogui, time, sys

try:
    while True:
        x, y = pyautogui.position()
        sys.stdout.write(f"\rX: {x}   Y: {y}")
        sys.stdout.flush()
        time.sleep(0.05)
except KeyboardInterrupt:
    print("\nExited.")
