import pyautogui
import numpy as np
import time

# 1850,236 1955,953
REGION = (1850, 236, 105, 717)  # cropped fishing meter
# rgb(0, 174, 255)
FISH_COLOR = np.array([0,174,255])  # replace with your RGB
FISH_TOL = 25


def get_fish_y(img):
    arr = np.array(img)

    diff = np.abs(arr - FISH_COLOR)
    mask = np.all(diff < FISH_TOL, axis=2)

    ys = np.where(mask)[0]

    if len(ys) < 10:
        return None

    return int(np.mean(ys))


def get_bar_center(img):
    arr = np.array(img)

    white = (arr[:,:,0] > 230) & (arr[:,:,1] > 230) & (arr[:,:,2] > 230)
    ys = np.where(white)[0]

    if len(ys) < 20:
        return None

    top = np.percentile(ys, 10)
    bottom = np.percentile(ys, 90)

    return int((top + bottom) / 2)

def color_present(img, TARGET, TOL=20):
    arr = np.array(img)
    diff = np.abs(arr - TARGET)
    mask = np.all(diff < TOL, axis=2)
    return np.any(mask)

def catchFish():
    holding = False
    last_fish_y = None
    while True:
        img = pyautogui.screenshot(region=REGION)

        fish_y = get_fish_y(img)
        bar_y = get_bar_center(img)

        if fish_y is None or bar_y is None:
            # print("caught fish")
            # return
            continue
        
        # estimate fish velocity
        if last_fish_y is None:
            velocity = 0
        else:
            velocity = fish_y - last_fish_y

        last_fish_y = fish_y

        # prediction helps stay centered
        predicted = fish_y + velocity * 2

        error = predicted - bar_y

        if error < -5:
            if not holding:
                pyautogui.mouseDown()
                holding = True
        elif error > 5:
            if holding:
                pyautogui.mouseUp()
                holding = False

        time.sleep(0.01)


def continueGame():
    castColor = np.array([255,162,0])
    reelColor = np.array([173, 191, 195])
    buttonRegion = (1904,1157,1,58)
    img = pyautogui.screenshot(region=buttonRegion)
    if color_present(img,castColor):
        pyautogui.mouseDown()
        time.sleep(0.05)
        pyautogui.mouseUp()
        reelImg = pyautogui.screenshot(region=buttonRegion)
        while not color_present(reelImg,reelColor):
            reelImg = pyautogui.screenshot(region=buttonRegion)
            time.sleep(0.01)
        catchFish()
    pyautogui.click()


print("Start game in 3 seconds...")
time.sleep(3)

while True:
    # continueGame()
    catchFish()