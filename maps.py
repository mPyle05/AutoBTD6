import image
import pyautogui
import configparser
import time

cfg = configparser.ConfigParser()
cfg.read('config.ini')

maps = {
    key: [int(x) for x in value.split(',')]
    for key, value in cfg['Map'].items()
}

advanced_loc = (1836, 1817)
expert_loc = (2300, 1831)
map_start_loc = (810, 487)
map_loc_offset = (800, 600)


easy_loc = (984, 900)
med_loc = (1621, 900)
hard_loc = (2224, 900)


def find_collection_map(collection_img_path):
    pg_num = 1
    pyautogui.click(advanced_loc)
    time.sleep(0.1)
    pyautogui.click(expert_loc)
    time.sleep(0.1)

    map_loc = image.find(collection_img_path)
    if not map_loc:
        pyautogui.click(expert_loc)
        time.sleep(0.1)
        map_loc = image.find(collection_img_path)
        pg_num = 2
    
    if not map_loc:
        return None

    # Calculate row and column
    dx = map_loc[0] - map_start_loc[0]
    dy = map_loc[1] - map_start_loc[1]
    col = round(dx / map_loc_offset[0]) + 1
    row = round(dy / map_loc_offset[1]) +1

    map_num = col + (row - 1)*3

    coords = [pg_num, map_num]

    # Reverse lookup map name
    for name, val in maps.items():
        if val == coords:
            return name
               
    return None  # No map matched



def start_game(map_name, cata, mode, collection=False):
    

    if collection:
        map_name = find_collection_map(collection)
        cata = "hard"
        mode = "impoppable"



    else:
        map_data = maps[map_name]
        click_loc = list(map_start_loc)
        pyautogui.click(advanced_loc)
        time.sleep(0.1)

        for i in range(map_data[0]):
            pyautogui.click(expert_loc)
            time.sleep(0.1)

    map_data = maps[map_name]
    click_loc = list(map_start_loc)
    
    if map_data[1] < 4:
        click_loc[0] += map_loc_offset[0] * (map_data[1] - 1)
    else:
        click_loc[1] += map_loc_offset[1]
        click_loc[0] += map_loc_offset[0] * (map_data[1] - 4)

    pyautogui.click(click_loc)

    image.click(fr"modes\{cata}.png")
    image.click(fr"modes\{mode}.png")
    image.click(fr"modes\ok.png",10)
    
    return map_name
    

def startCollection(collection):
    return start_game("quad", "hard", "impoppable", fr"img\{collection}.png")

def victory():
    if image.find(fr"img\insta.png"):
        image.click(fr"img\insta.png")
        time.sleep(0.5)
    if image.find(fr"img\victory.png"):
        image.click(fr"img\next.png")
        image.click(fr"img\home.png")
        return True
    else:
        return False

def defeat():
    if image.find(fr"img\defeat.png"):
        image.click(fr"img\home.png")
        return True
    else:
        return False
    

victory()