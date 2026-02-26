import arcade
import os

from LOGIC.menu.button_sprite import ButtonSprite


MENU_IMAGE = os.path.join(os.path.dirname(__file__), "menu_pause.jpg")


class MenuPause(arcade.View):
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
        spacing = 20
        y_start = self.window.height // 2 + 50

        # Crée chaque bouton comme sprite
        names = ["JOUER", "PARAMETRES", "QUITTER"]
        for i, name in enumerate(names):
            y = y_start - i * (self.button_height + spacing)
            btn = ButtonSprite(
                center_x=self.window.width // 2,
                center_y=y,
                width=self.button_width,
                height=self.button_height,
                color=(255, 255, 255, 180),  # blanc semi-transparent
                text=name
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
                if btn.text == "JOUER":
                    self.load_game()
                elif btn.text == "PARAMETRES":
                    print("Paramètres (pas encore là, t'as qu'à coder !!)")
                elif btn.text == "QUITTER":
                    self.load_view()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.load_game()

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

    
    def load_view(self):
        from LOGIC.menu.menu_start.menu_start import MenuStart
        self.game.switch_scene(MenuStart(self.game))
    
    def load_game(self):
        from LOGIC.logic import GameView
        self.game.switch_scene(GameView(self.game, save_file="save1.json"))