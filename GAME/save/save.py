import os
import json
import arcade

MAP_WIDTH = 5000
MAP_HEIGHT = 5000

default_data = {
    "player": {
        "player_x": MAP_WIDTH // 2,
        "player_y": MAP_HEIGHT // 2
    },
    "inventory": {}
}

def save_file(data, file_to_save_in):
    """Save the (data) in the (file_to_save_in) """
    
    chemin = os.path.dirname(__file__)
    fichier = os.path.join(chemin, file_to_save_in)
    with open(fichier, "w") as file:
        json.dump(data, file, indent=4, sort_keys=True)


def load_file(file_to_load_from):
    """load the data stored in the (file_to_load_from)"""

    chemin = os.path.dirname(__file__)
    fichier = os.path.join(chemin, file_to_load_from)
    if not os.path.exists(fichier):
        with open(fichier, "w") as file:
            json.dump(default_data, file, indent=4, sort_keys=True)
        
    with open(fichier, "r") as file:
        data = json.load(file)
    return data


def delete_file(file_to_delete):
    chemin = os.path.dirname(__file__)
    fichier = os.path.join(chemin, file_to_delete)
    os.remove(fichier)
    load_file(file_to_delete)  


def sprite_list_to_dict(sprite_list):
    data = []
    if sprite_list:
        for sprite in sprite_list:
            data.append({"texture": sprite.texture,
            "center_x": sprite.center_x,
            "center_y": sprite.center_y,
            "scale": sprite.scale
            })
        return data


def dict_to_sprite_list(dict):
    sprite_list = arcade.SpriteList()
    for data in dict:
        sprite = arcade.Sprite(data["texture", data["scale"]])
        sprite.center_x = data["center_x"]
        sprite.center_y = data["center_y"]
        sprite_list.append(sprite)