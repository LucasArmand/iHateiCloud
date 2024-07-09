import json
import os
def write_setting(setting, value):
    settings_obj = get_settings_obj()
    with open("settings.txt", 'w') as file:
        settings_obj[setting] = value
        json.dump(settings_obj, file)


def get_settings_obj():
    tries = 3
    while tries > 0:
        try:
            with open("settings.txt", 'r') as file:
                return json.load(file)
        except:
            with open("settings.txt", "w") as file:
                file.write("{}")
    print("ERROR: Cannot read settings")
    return None


