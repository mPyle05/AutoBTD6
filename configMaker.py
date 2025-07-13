import pyautogui
import keyboard
import configparser
import time
import image  # assuming you have image.current_round()

# Change this to your desired output file
OUTPUT_CONFIG = 'gameplans/auto_generated.ini'

# Initialize config parser and state
cfg = configparser.ConfigParser()
current_section = None
entry_counter = 0

# Load existing if any
try:
    cfg.read(OUTPUT_CONFIG)
except FileNotFoundError:
    pass


def start_section():
    global current_section, entry_counter
    round_num = image.current_round()
    if round_num is None:
        print("Could not determine current round. Make sure image.current_round() works.")
        return
    section = str(round_num)
    if section in cfg.sections():
        print(f"Section [{section}] already exists, appending to it.")
    else:
        cfg[section] = {}
        print(f"Started new section [{section}]")
    current_section = section
    entry_counter = 1


def record_place():
    global entry_counter
    if not current_section:
        print("No active section. Press F8 to start a new section")
        return
    x, y = pyautogui.position()
    tower = input("Enter tower name for placement: ").strip()
    key = f"place{entry_counter}"
    cfg[current_section][key] = f"{tower},{x},{y}"
    print(f"Added {key} = {tower},{x},{y} to section [{current_section}]")


def record_upgrade():
    global entry_counter
    if not current_section:
        print("No active section. Press F8 to start a new section")
        return
    x, y = pyautogui.position()
    upgrade_str = input("Enter upgrade string (e.g. 001 for paths): ").strip()
    key = f"upgrade{entry_counter}"
    cfg[current_section][key] = f"{x},{y},{upgrade_str}"
    print(f"Added {key} = {x},{y},{upgrade_str} to section [{current_section}]")
    entry_counter += 1


def finalize_section():
    if not current_section:
        print("No active section to finalize.")
        return
    # Optionally add a start flag
    #cfg[current_section]['start'] = 'true'
    with open(OUTPUT_CONFIG, 'w') as f:
        cfg.write(f)
    print(f"Saved config to {OUTPUT_CONFIG}")


# Hotkey bindings
def main():
    print("Config Recorder Active")
    print("F1: Start new round section")
    print("F5: Record placement at current mouse position")
    print("F6: Record upgrade at current mouse position")
    print("F10: Finalize section and save to file")
    print("Press F12 to exit.")

    keyboard.add_hotkey('F1', start_section)
    keyboard.add_hotkey('F5', record_place)
    keyboard.add_hotkey('F6', record_upgrade)
    keyboard.add_hotkey('F10', finalize_section)

    # wait until ESC
    keyboard.wait('F12')
    print("Exiting Config Recorder.")


if __name__ == '__main__':
    main()
 