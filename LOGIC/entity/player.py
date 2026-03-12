import arcade
import random

from LOGIC.entity.entity import Entity
from LOGIC.textures.load_sheet import load_sheet

MAP_WIDTH = 5000
MAP_HEIGHT = 5000

TEXTURES = {
    "idle": "LOGIC/textures/player/player_idle.png",
    "run": "LOGIC/textures/player/player_run.png"
}

idle_textures = load_sheet(TEXTURES["idle"], 1)
run_textures = load_sheet(TEXTURES["run"], 6)


class Player(Entity):

    PLAYER_SPEED = 400
    PLAYER_HP = 100

    def __init__(self, x: int | float, y: int | float,
                 name_or_precise_type=None,
                 path_or_texture=None):

        self.speed = self.PLAYER_SPEED
        self.hp = self.PLAYER_HP
        self.max_hp = self.PLAYER_HP

        
        self.key_pressed = set()

        self.time_counter = 0
        self.frame_index = 0
        self.state = "IDLE"

        super().__init__(
            x, y,
            name_or_precise_type=name_or_precise_type,
            path_or_texture=idle_textures[0] if idle_textures else None,
            speed=self.speed,
            hp=self.hp
        )

        self.center_x = x
        self.center_y = y

        if idle_textures:
            self.texture = idle_textures[0]


    def update_animation(self, delta_time=1 / 60):

        # Déterminer l'état selon le mouvement
        if self.change_x != 0 or self.change_y != 0:
            self.state = "RUN"
        else:
            self.state = "IDLE"

        # Choix des frames selon l'état
        if self.state == "RUN":
            frames = run_textures
            speed = 0.10
        else:
            frames = idle_textures
            speed = 0.2

        if not frames:
            return

        self.time_counter += delta_time
        if self.time_counter >= speed:
            self.time_counter = 0
            self.frame_index = (self.frame_index + 1) % len(frames)
            self.texture = frames[self.frame_index]

        # Flip horizontal
        if self.change_x < 0:
            self.scale_x = -1
        elif self.change_x > 0:
            self.scale_x = 1



    def update(self, delta_time=1/60):
        self.update_animation(delta_time)
        self.move(delta_time)

        # Application du mouvement
        self.center_x += self.change_x
        self.center_y += self.change_y


    def move(self, delta_time=1/60):
        """Set the change_x and change_y with the values presents in the self.key_press set"""
        self.change_x = 0
        self.change_y = 0
        if arcade.key.Z in self.key_pressed and not arcade.key.S in self.key_pressed:
            self.change_y = self.speed * delta_time
        if arcade.key.S in self.key_pressed and not arcade.key.Z in self.key_pressed:
            self.change_y = - self.speed * delta_time
        if arcade.key.D in self.key_pressed and not arcade.key.Q in self.key_pressed:
            self.change_x = self.speed * delta_time
        if arcade.key.Q in self.key_pressed and not arcade.key.D in self.key_pressed:
            self.change_x = - self.speed * delta_time
        

    