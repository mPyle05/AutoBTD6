import keyboard
import time

try:
    print("Pressing '1' repeatedly. Press ESC to stop.")
    while True:
        keyboard.press_and_release('1')
        time.sleep(0.5)  # Adjust delay as needed

        if keyboard.is_pressed('esc'):
            print("Stopped.")
            break

except KeyboardInterrupt:
    print("Stopped by user.")
