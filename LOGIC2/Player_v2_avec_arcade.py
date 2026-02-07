import arcade
import json
import os
from LOGIC2.menu_ingame.menu_ingamev1 import InGameMenu

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FICHIER = os.path.join(os.path.dirname(__file__), "save.json")

class GameView(arcade.View):
    def __init__(self) -> None:
        super().__init__()
        self.data = self.load_game()
        self.x = self.data["player"]["player_x"]
        self.y = self.data["player"]["player_y"]
        self.speed = 500
        self.direction = {"right": False, "left": False, "up": False, "down": False}
        self.inventory = self.data["inventory"]
        self.stuff_to_save = {"inventory": self.inventory, "player": {"player_x": self.x, "player_y": self.y}}

    def on_draw(self) -> None:
        self.clear()
        arcade.draw_circle_filled(self.x, self.y, 30, arcade.color.AO)
        arcade.draw_text(f"x={self.x:.2f} y={self.y:.2f}", 10, SCREEN_HEIGHT-10, arcade.color.WHITE)

    def on_update(self, delta_time) -> None:
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

    def on_key_press(self, symbol, modifiers) -> None:
        if symbol == arcade.key.D: self.direction["right"] = True
        if symbol == arcade.key.Q: self.direction["left"] = True
        if symbol == arcade.key.Z: self.direction["up"] = True
        if symbol == arcade.key.S: self.direction["down"] = True
        if symbol == arcade.key.ESCAPE:
            menu = InGameMenu(self)
            self.window.show_view(menu)

    def on_key_release(self, symbol, modifiers) -> None:
        if symbol == arcade.key.D: self.direction["right"] = False
        if symbol == arcade.key.Q: self.direction["left"] = False
        if symbol == arcade.key.Z: self.direction["up"] = False
        if symbol == arcade.key.S: self.direction["down"] = False

    def save_game(self) -> None:
        with open(FICHIER, "w") as f:
            json.dump(self.stuff_to_save, f, indent=2)

    def load_game(self) -> None:
        if not os.path.exists(FICHIER):
            default_data = {"inventory": {}, "player": {"player_x": SCREEN_WIDTH//2, "player_y": SCREEN_HEIGHT//2}}
            with open(FICHIER, "w") as f:
                json.dump(default_data, f, indent=2)
            return default_data
        with open(FICHIER, "r") as f:
            return json.load(f)
