import arcade

from LOGIC.inventory.inventory import Inventory
from LOGIC.entity.item_cls import Gear_wheel, Sword
from LOGIC.entity.item import Item


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
    def __init__(self, game, file):
        super().__init__()
        self.game = game
        self.file = file


        self.camera = arcade.camera.Camera2D()
        self.camera.position = self.window.width // 2, self.window.height // 2

        self.inventory = Inventory(file)

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
        if symbol == arcade.key.ESCAPE or symbol == arcade.key.E:
            self.back_to_game()
    
    


    # Fonctions non présentes de base dans arcade

    def get_item_class(self, name: str):
        for cls in Item.__subclasses__():
            if cls.type == name:
                return cls
        return None
    
    def place_item(self):
        
        for index, (item_name, number) in enumerate(self.inventory.inventory):
            item_class = self.get_item_class(item_name)
            if item_class:
                item = arcade.Sprite(path_or_texture=item_class.path_or_texture, scale=0.7)

                i = index % 10 + 2 
                j = index // 10 + 2 
                item.center_x = i * 100
                item.center_y = j * 100 

                self.item_list.append(item)

            
            quantity = arcade.Text(f"{number}", x= item.center_x-30 ,y= item.center_y-30, color=arcade.color.WHITE, font_size=14)
            self.text_list.append(quantity)


    def back_to_game(self):
        from LOGIC.logic import GameView
        self.game.switch_scene(GameView(self.game, save_file=self.file))

