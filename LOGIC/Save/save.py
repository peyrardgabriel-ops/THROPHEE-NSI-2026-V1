import os
import json

CHEMIN = os.path.dirname(__file__)
FICHIER = os.path.join(CHEMIN, "save.json")

default_data = {
    "player": {
        "player_x": 640,
        "player_y": 360
    },
    "inventory": {}
}

def save_file(data):
    with open(FICHIER, "w") as file:
        json.dump(data, file, indent=4, sort_keys=True)

def load_file():
    if not os.path.exists(FICHIER):
        with open(FICHIER, "w") as file:
            json.dump(default_data, file, indent=4, sort_keys=True)
        
    with open(FICHIER, "r") as file:
        data = json.load(file)
    return data


