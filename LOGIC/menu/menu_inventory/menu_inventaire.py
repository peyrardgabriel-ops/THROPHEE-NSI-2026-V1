import arcade
import random

from LOGIC.inventory.inventory import Inventory
from LOGIC.entity.item_cls import *
from LOGIC.entity.item import Item
from LOGIC.logic import GameView



SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

class Case(arcade.Sprite):
    def __init__(self, center_x, center_y, width, height, color):
        texture = arcade.make_soft_square_texture(width, color, outer_alpha=color[3])
        super().__init__(texture, scale=1.0)
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height

class InventoryMenu(arcade.View):
    def __init__(self, game, file, inventory, gameview):
        super().__init__()
        self.game = game
        self.file = file


        self.camera = arcade.camera.Camera2D()
        self.camera.position = self.window.width // 2, self.window.height // 2

        self.inventory = inventory
        self.gameview = gameview

        case_width = 80
        case_height = 80
        self.case_list = arcade.SpriteList()
        self.item_list = arcade.SpriteList()
        self.text_list = []

        self.text = arcade.Text(f"Inventory",
                                x= self.window.width // 2 - 50,
                                y = self.window.height - 200,
                                color= arcade.color.BLACK,
                                font_size=40)
        self.text_list.append(self.text)

        

        # Dessin basique des cases d'inventaire
        for i in range(2,12):
            for j in range(2,4):
                x_case = i * 100 
                y_case = j * 100 

                case = Case(center_x=x_case, center_y=y_case, width=case_width, height=case_height, color= (100, 100, 100, 125))
                self.case_list.append(case)
        
        self.place_item()

    def on_draw(self):
        self.camera.use()
        self.clear()
        self.case_list.draw()
        self.item_list.draw()
        for texts in self.text_list:
            texts.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE or symbol == arcade.key.A:
            self.back_to_game()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            for item in self.item_list:
                if (item.center_x - item.width / 2 <= x <= item.center_x + item.width / 2 and
                    item.center_y - item.height / 2 <= y <= item.center_y + item.height / 2):
                    self.drop_item(item.name)

        self.item_list.clear()
        self.text_list.clear()
        self.text_list.append(self.text)
        self.place_item()
                    
                    

    


    # Fonctions non présentes de base dans arcade

    def get_item_class(self, name: str):
        for cls in Item.__subclasses__():
            if cls.type == name:
                return cls
        return None
    
    def place_item(self):
        
        for index, (item_name, number) in enumerate(self.inventory.inventory):
            item_class = self.get_item_class(item_name)
            i = index % 10 + 2 
            j = index // 10 + 2 
            x = i * 100
            y = j * 100 

            if item_class:
                item = arcade.Sprite(path_or_texture=item_class.path_or_texture, scale=0.7)
                item.center_x = x
                item.center_y = y
                item.name = item_name
                self.item_list.append(item)

            
            quantity = arcade.Text(f"{number}", x= x-30 ,y= y-30, color=arcade.color.WHITE, font_size=14)
            self.text_list.append(quantity)

    
    def drop_item(self, item:str):
        """Create a item at the coordonates x,y and store it in the self.item_list"""
        item_class = self.get_item_class(item)
        if item_class == None:
            raise ValueError(f"Item inconnu : {item}")
        self.inventory.remove_from_inventory(item)
        x = random.randint(-100, 100) + self.gameview.player.center_x
        y = random.randint(-100, 100) + self.gameview.player.center_y
        new_item = item_class(x=x, y=y)
        self.gameview.item_list.append(new_item)
        


    def back_to_game(self):
        self.window.show_view(self.gameview)

