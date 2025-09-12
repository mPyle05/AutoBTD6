import keyboard,time,pyautogui

start = [1350,1500]

try:
    print("Running Heli program. Press ESC to stop.")
    i = 0
    time.sleep(2)  # Initial delay to switch to the game window
    while True:
        keyboard.press_and_release('2')
        time.sleep(1)  # Adjust delay as needed
        if i == 0:
            start[0] += 100
            start[1] += 100
            i += 1
        else:
            start[0] -= 100
            start[1] -= 100
            i = 0
            
        pyautogui.click()  
        pyautogui.moveTo(start[0], start[1], duration=1)
        pyautogui.click()
        time.sleep(0.5)

        if keyboard.is_pressed('esc'):
            print("Stopped.")
            break

except KeyboardInterrupt:
    print("Stopped by user.")
