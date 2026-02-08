import arcade
import json
import os
from LOGIC.menu_ingame.menu_ingamev1 import InGameMenu

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "j'ai vrm pas d'idée"

CHEMIN = os.path.dirname(__file__)
FICHIER = os.path.join(CHEMIN, "save.json")





class GameView(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        # Recupère les données 
        self.data = self.load_game()
        

        # Mouvement 
        self.x = self.data["player"]["player_x"]
        self.y = self.data["player"]["player_y"]
        self.speed = 500
        self.direction = {
            "right":False,
            "left":False,
            "up":False,
            "down":False
        }

        self.inventory = self.data["inventory"]
        self.stuff_to_save = {
            "inventory" : self.inventory,
            "player":{
                "player_x": self.x,
                "player_y": self.y
            }
        }
        

    def on_draw(self) -> None:
        self.clear()


        arcade.draw_circle_filled(center_x=self.x, center_y=self.y, radius=30,color=arcade.color.AO)

        #test
        arcade.draw_text(text=f"x = {self.x:.2f} -- y = {self.y:.2f}", x = 10, y= SCREEN_HEIGHT-10, color=arcade.color.WHITE)

        

    def on_update(self, delta_time:float) -> None:

        #partie mouvement 
        if self.direction["right"]:
            self.x += self.speed * delta_time
        if self.direction["left"]:
            self.x -= self.speed * delta_time
        if self.direction["up"]:
            self.y += self.speed * delta_time
        if self.direction["down"]:
            self.y -= self.speed * delta_time
            
        self.stuff_to_save["player"]["player_x"] = self.x
        self.stuff_to_save["player"]["player_y"] = self.y


    def on_key_press(self, symbol:int, modifiers:int) -> None:

        #mouvement
        if symbol == arcade.key.D:
            self.direction["right"] = True
        if symbol == arcade.key.Q:
            self.direction["left"] = True
        if symbol == arcade.key.Z:
            self.direction["up"] = True
        if symbol == arcade.key.S:
            self.direction["down"] = True
        
        if symbol == arcade.key.ESCAPE:
            menu = InGameMenu(self)
            self.window.show_view(menu)
    
    def on_key_release(self, symbol:int, modifiers:int) -> None:
        
        #mouvement
        if symbol == arcade.key.D:
            self.direction["right"] = False
        if symbol == arcade.key.Q:
            self.direction["left"] = False
        if symbol == arcade.key.Z:
            self.direction["up"] = False
        if symbol == arcade.key.S:
            self.direction["down"] = False

    # Creation de l'inventaire
    def add_to_inventory(self, item:str, number_of_item=1):
        """
        Docstring for add_to_inventory
        
        :param item: l'item que l'on veut rajouter à l'inventaire
        :param number_of_item: nombre de fois que l'on veut rajouter cet item a l'inventaire
        """

        if not item in self.inventory.keys():
            self.inventory[item] = 0
        self.inventory[item] += number_of_item
        
    def save_game(self):
        """
        Save the variable self.stuff_to_save in the file save.json
        """
        with open(FICHIER, "w") as file:
            json.dump(self.stuff_to_save, file,  indent=2, sort_keys=True)

    def load_game(self):
        """
        Load the variable data from the file save.json
        """
        data = {}
        
        if not os.path.exists(FICHIER):
            open(FICHIER, "w").close()
        
        
        with open(FICHIER, "r") as file:
            data = json.load(file)
        return data




