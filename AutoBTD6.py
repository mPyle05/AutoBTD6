import tower,image,maps,time,configparser,pyautogui,keyboard
cfg = configparser.ConfigParser()

##Current screen resolution (3200x2000)
##Current game resolution Full screen (3200x2000)

roundCompleted = set()
gameStatus = None
currentMap = None
  


def check_game_status():
    global gameStatus

    if image.find(fr"img\play.png"):
        gameStatus = "home"
    elif image.find(fr"img\expert.png"):
        gameStatus = "map_selection"
    elif image.find(fr"img\upgrades.png"):
        gameStatus = "game_started"
    elif image.find(fr"img\collect.png"):
        gameStatus = "collection"

def parse_upgrade_string(upgrade_str):
    return [int(upgrade_str[0]), int(upgrade_str[1]), int(upgrade_str[2])]

def round_matches(section, round_num):
    if section.isdigit():
        return int(section) == round_num
    elif '-' in section:
        start, end = map(int, section.split('-'))
        return start <= round_num <= end
    return False

def gameplay():
    global roundCompleted
    global currentMap
    global gameStatus

    cfg.read(fr'gameplans\{currentMap}.ini')

    while True:
        
        if image.find(fr"img\level_up.png"):
            image.click(fr"img\level_up.png",)

        if (maps.victory() or maps.defeat()):
            gameStatus = "home"
            roundCompleted.clear()
            return False
        
        round_num = image.current_round()
        #print(f"Current round: {round_num}")

        for section in cfg.sections():
            if not round_matches(section, round_num) or round_num in roundCompleted:
                continue

            actions = dict(cfg[section])
            print(f"[Round {round_num}] Actions:", actions)

            i = 1
            while True:
                place_key   = f"place{i}"
                upgrade_key = f"upgrade{i}"

                if place_key in actions:
                    tower_name, x, y = actions[place_key].split(',')
                    x, y = int(x), int(y)
                    print(f"[Round {round_num}] Placing {tower_name} at ({x}, {y})")
                    tower.place(x, y, tower_name)
                    time.sleep(0.5)

                if upgrade_key in actions:
                    ux, uy, upgrade_str = actions[upgrade_key].split(',')
                    ux, uy = int(ux), int(uy)
                    upgrades = parse_upgrade_string(upgrade_str)

                    for path_index, times in enumerate(upgrades):
                        char = {0:r',', 1:r'.', 2:r'/'}[path_index]
                        for _ in range(times):
                            tower.upgrade(ux,uy,char)
                            time.sleep(0.3)

                if place_key not in actions and upgrade_key not in actions:
                    break
                

                i += 1

            if "start" in actions:
                keyboard.send("space")
                time.sleep(0.25)
                keyboard.send("space")
                time.sleep(0.25)

            roundCompleted.add(round_num)

def collection():
    global gameStatus

    image.click(fr"img\collect.png")

    while True:  
        if image.find(fr"img\lowestTier.png"):
            image.click(fr"img\lowestTier.png")
        if image.find(fr"img\midTier.png"):
            image.click(fr"img\midTier.png")
        if image.find(fr"img\insta.png"):
            image.click(fr"img\insta.png")
        if image.find(fr"img\continue.png"):
            image.click(fr"img\continue.png")
        if image.find(fr"img\back.png"):
            image.click(fr"img\back.png")
            gameStatus = "home"
            return True
    


def main():

    
    # image.screen_scaling()

    while True:
        global gameStatus
        global currentMap

        check_game_status()

        print(f"Current game status: {gameStatus}")
        print(f"Current map: {currentMap}")

        match gameStatus:
            case "home":
                image.click(r"img\play.png")
            case "map_selection":
                #currentMap = maps.startCollection("july4th")
                currentMap = maps.start_game("dark_castle", "hard", "impoppable")
                gameStatus = "game_started"
            case "game_started":
                gameplay()
            case "veteran_lvl_up":
                image.click(r"img\level_up.png")
            case "collection":
                collection()
            case _:
                print("Unknown state")

        time.sleep(.2)  

if __name__ == "__main__":
   main()