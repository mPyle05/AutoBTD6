import image
import pyautogui
import configparser
import time
import keyboard

hero_Loc = (2900,478)  

cfg = configparser.ConfigParser()
cfg.read('config.ini')

hotkeys = dict(cfg['Hotkeys'])


def is_selected(): 
    if image.find("img/sell.png"): 
        return True
    else:
        return False


def place(x,y,tower):
    time.sleep(.1)
    if tower == "hero":
        pyautogui.click(hero_Loc)
    else:
        keyboard.send(hotkeys[tower])

    if image.tower_selected():
        pyautogui.click(x, y)
        return True
    else:
        print(f"Failed to place {tower} at ({x}, {y}).")
        return False


def upgrade(x,y,path):
    pyautogui.click(x, y)
    if not image.tower_selected(upgrade=True):
        print(f"Failed to select tower at ({x}, {y}).")
        return
    keyboard.send(path)
    time.sleep(.1)
    keyboard.send("escape")
    time.sleep(.1)

def sell(x,y):
    while True:
        if image.find("img/sell.png"):
            keyboard.send("backspace")
            break
        else:
            pyautogui.click(x,y)
            time.sleep(.2)
    
def remove(x,y):
    pyautogui.click(x, y)
    image.click("img/remove.png",5)
