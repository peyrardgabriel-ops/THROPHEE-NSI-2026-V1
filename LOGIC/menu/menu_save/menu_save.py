import arcade
import os

from LOGIC.menu.button_sprite import ButtonSprite
from LOGIC.Save.save import delete_file

MENU_IMAGE = os.path.join(os.path.dirname(__file__), "menu_pause.jpg")


class MenuSave(arcade.View):
    def __init__(self, game):
        super().__init__()

        self.game = game

        # Sprite du menu
        self.menu_sprite = arcade.Sprite(MENU_IMAGE, scale=1.0)
        self.menu_sprite.center_x = self.window.width // 2
        self.menu_sprite.center_y = self.window.height // 2
        self.menu_list = arcade.SpriteList()
        self.menu_list.append(self.menu_sprite)

        # Boutons
        self.button_list = arcade.SpriteList()
        self.button_width = 300
        self.button_height = 60
        spacing = 30
        y_start = self.window.height // 2 + 20

        # Crée chaque bouton comme sprite
        # A gauche
        names = ["SAVE-1", "SAVE-2", "SAVE-3"]
        for i, name in enumerate(names):
            y = y_start - i * (self.button_height + spacing) + 100
            btn = ButtonSprite(
                center_x=self.window.width // 2 - 200,
                center_y=y,
                width=self.button_width,
                height=self.button_height,
                color=(255, 255, 255, 180),  # blanc semi-transparent
                text=name
            )
            self.button_list.append(btn)

        # A droite
        del_names = ["Delete 1 ?", "Delete 2 ?", "Delete 3 ?"]
        for i, name in enumerate(del_names):
            y = y_start - i * (self.button_height + spacing) + 100
            btn = ButtonSprite(
                center_x=self.window.width // 2 + 200,
                center_y=y,
                width=self.button_width,
                height=self.button_height,
                color=(255, 255, 255, 180),  # blanc semi-transparent
                text=name
            )
            self.button_list.append(btn)
        
        # Au centre
        btn = ButtonSprite(
                center_x=self.window.width // 2,
                center_y=200,
                width=self.button_width,
                height=self.button_height,
                color=(255, 255, 255, 180),  # blanc semi-transparent
                text="BACK"
            )
        self.button_list.append(btn)

        
        # Caméra
        self.camera = arcade.camera.Camera2D()
        self.camera.position = self.window.center_x, self.window.center_y

    def on_draw(self):
        self.camera.use()
        self.clear()
        self.menu_list.draw()
        self.button_list.draw()
        # Dessiner le texte sur les boutons
        for btn in self.button_list:
            btn.label.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        # Vérifie quel bouton est cliqué
        for btn in self.button_list:
            if (btn.center_x - btn.width / 2 <= x <= btn.center_x + btn.width / 2 and
                btn.center_y - btn.height / 2 <= y <= btn.center_y + btn.height / 2):
                if btn.text == "SAVE-1":
                    self.show_game("save1.json")
                elif btn.text == "SAVE-2":
                    self.show_game("save2.json")
                elif btn.text == "SAVE-3":
                    self.show_game("save3.json")
                elif btn.text == "BACK":
                    self.show_start()

                elif btn.text == "Delete 1 ?":
                    delete_file("save1.json")
                elif btn.text == "Delete 2 ?":
                    delete_file("save2.json")
                elif btn.text == "Delete 3 ?":
                    delete_file("save3.json")
    
    def on_mouse_motion(self, x, y, dx, dy):

        for btn in self.button_list:
            condition = (btn.center_x - btn.base_width / 2 <= x <= btn.center_x + btn.base_width / 2 and 
            btn.center_y - btn.base_height / 2 <= y <= btn.center_y + btn.base_height / 2)
            
            if condition:
            
                btn.width = btn.base_width + 10
                btn.height = btn.base_height + 10
            else:
                
                btn.width = self.button_width
                btn.height = self.button_height



    def show_game(self, file):
        from LOGIC.logic import GameView
        self.game.switch_scene(GameView(self.game, save_file=file))
    

    def show_start(self):
        from LOGIC.menu.menu_start.menu_start import MenuStart
        self.game.switch_scene(MenuStart(self.game))