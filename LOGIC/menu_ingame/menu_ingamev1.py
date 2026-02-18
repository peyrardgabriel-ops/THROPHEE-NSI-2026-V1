import arcade
import os

MENU_IMAGE = os.path.join(os.path.dirname(__file__), "menu_ingame.jpg")


class ButtonSprite(arcade.Sprite):
    def __init__(self, center_x, center_y, width, height, color, text):
        # Création d'une texture simple pour le sprite
        texture = arcade.make_soft_square_texture(width, color, outer_alpha=color[3])
        super().__init__(texture, scale=1.0)
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.label = arcade.Text(text=self.text,
                                    x = self.center_x,
                                    y = self.center_y,
                                    color = arcade.color.BLACK,
                                    font_size= 20,
                                    anchor_x="center",
                                    anchor_y="center")

        

class InGameMenu(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

        # Sprite du menu
        self.menu_sprite = arcade.Sprite(MENU_IMAGE, scale=1.0)
        self.menu_sprite.center_x = self.window.width // 2
        self.menu_sprite.center_y = self.window.height // 2
        self.menu_list = arcade.SpriteList()
        self.menu_list.append(self.menu_sprite)

        # Boutons
        self.button_list = arcade.SpriteList()
        button_width = 300
        button_height = 60
        spacing = 20
        y_start = self.window.height // 2 + 50

        # Crée chaque bouton comme sprite
        names = ["JOUER", "PARAMETRES", "QUITTER"]
        for i, name in enumerate(names):
            y = y_start - i * (button_height + spacing)
            btn = ButtonSprite(
                center_x=self.window.width // 2,
                center_y=y,
                width=button_width,
                height=button_height,
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
                    self.window.show_view(self.game_view)
                elif btn.text == "PARAMETRES":
                    print("Paramètres (pas encore là, t'as qu'à coder !!)")
                elif btn.text == "QUITTER":
                    arcade.close_window()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.game_view) 