import cv2, numpy as np, pyautogui, time, pytesseract
from PIL import Image
from pathlib import Path

# tell pytesseract exactly where Tesseract lives on disk:
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Region where the "round" text lives: (x, y, width, height)
roundRegion = (2240, 135, 335, 75)
# Region where the "selected" tower lives: (x, y, width, height)
selectedRegion = (2557,213,200,150)  


def screen_scaling(paths):
    main_size = (3200, 2000)
    # main_size = (3200, 1000)
    current_size = pyautogui.size()    

    prop = (int(current_size[0] / main_size[0]), int(current_size[1] / main_size[1]))
    if prop == (1,1):
        print("No scaling needed")
        return
    else:
        file_path = Path("{}_{}X{}.png".format(paths[0][:-4],str(prop[0]),str(prop[1])))
        if file_path.is_file():
            return prop

    for path in paths:
        img = Image.open(path)
        # print(type(img))
        resized_img = img.resize([(img.size[0] * prop[0]), (img.size[1] * prop[1])])
        newPath = "{}_{}X{}.png".format(path[:-4],str(prop[0]),str(prop[1]))
        resized_img.save(newPath)
    return prop



def find(template_path, threshold=0.8,area=False):
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    h, w = template.shape[:2]
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    if max_val >= threshold:
        return (int(max_loc[0] + w/2), int(max_loc[1] + h/2))
    return None

def tower_selected(timeout=2,upgrade=False):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if upgrade:
            if find("img/sell.png"):
                    return True
        else:
            if find("img/close.png", area=selectedRegion):
                return True
    return False
    

def click(imagePath, timeout=5, delay=0.25, confidence=0.8):
    deadline = time.time() + timeout
    while time.time() < deadline:
        loc = find(imagePath, confidence)
        if loc:
            pyautogui.click(loc)
            time.sleep(delay)
            return True
    return False


def read_round():
    x, y, w, h = roundRegion
    pil = pyautogui.screenshot(region=(x, y, w, h))
    frame = cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 1) Equalize contrast
    eq = cv2.equalizeHist(gray)

    # 2) Fixed threshold: anything very bright → white
    _, thr = cv2.threshold(eq, 200, 255, cv2.THRESH_BINARY)

    # 3) Close small gaps in the white outline
    #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    #closed = cv2.morphologyEx(thr, cv2.MORPH_CLOSE, kernel, iterations=2)

    # 4) Erode just a little to shave off stray edge‑noise
    #eroded = cv2.erode(closed, kernel, iterations=1)

    # 5) Invert: digits become black on white
    final = cv2.bitwise_not(thr)

    # save for inspection
    #cv2.imwrite("round_debug_processed.png", np.hstack([gray, eq, thr, closed, eroded, final]))

    # OCR
    cfg = r'--psm 7 -c tessedit_char_whitelist=0123456789/'
    text = pytesseract.image_to_string(final, config=cfg)
    return text.strip()

def current_round():
    text = read_round()
    if "/" in text:
        try:
            return int(text.split("/")[0])
        except ValueError:
            pass
    return None
