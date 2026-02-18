import arcade
from LOGIC.textures.load_sheet import load_sheet

# Player
IMG_PLAYER = ":resources:/images/animated_characters/male_adventurer/maleAdventurer_idle.png"

# Ennemies
IMG_ZOMBIE = ":resources:/images/animated_characters/zombie/zombie_idle.png"
IMG_ROBOT = ":resources:/images/animated_characters/robot/robot_idle.png"

# Items
IMG_COIN = ":resources:/images/items/coinGold.png"


class Entity(arcade.Sprite):
    
    def __init__(self,
                    x: int | float, y:int | float,
                    name_or_precise_type:str | None = None,
                    path_or_texture = None,
                    character_scale = 1):
        
        super().__init__(path_or_texture= path_or_texture, scale= character_scale)

        # Position
        self.center_x = x
        self.center_y = y

        # Autres caractéristiques
        self.name_or_precise_type = name_or_precise_type 

# Ennemies
class Enemy(Entity):
    ALL_ENEMY = ["zombie", "robot"]
    def __init__(self, x, y, name_or_precise_type = None, path_or_texture=None):
        self.path_or_texture = path_or_texture
        super().__init__(x, y,
                        name_or_precise_type,
                        self.path_or_texture)
        


# Ennemis / robot
class Robot(Enemy):
    def __init__(self, x, y, name_or_precise_type=None, path_or_texture = None):
        super().__init__(x, y,
                        name_or_precise_type,
                        path_or_texture)
        
        TEXTURES = {"idle": "LOGIC.textures.enemy.robot.Robot_Idle.png",
                    "run": "LOGIC.textures.enemy.robot.Robot_run.png",
                    "shoot": "LOGIC.textures.enemy.robot.Robot_Shoot.png"}
        
        self.time_counter = 0
        self.frame_index = 0
        self.state = "IDLE"
        self.target_timer = 0

        self.idle_textures = load_sheet(TEXTURES["idle"], 6)
        self.run_textures = load_sheet(TEXTURES["run"], 4)
        self.shoot_textures = load_sheet(TEXTURES["shoot"], 8)

        if self.idle_textures:
            self.texture = self.idle_textures[0]

    def update_animation(self, delta_time=1/60):
        if self.state == "SHOOT":
            frames = self.shoot_textures
            speed = 0.10
        elif self.state == "RUN":
            frames = self.run_textures
            speed = 0.12
        else:
            frames = self.idle_textures
            speed = 0.18

        if not frames: return

        self.time_counter += delta_time
        if self.time_counter >= speed:
            self.time_counter = 0
            self.frame_index = (self.frame_index + 1) % len(frames)
            self.texture = frames[self.frame_index]

            if self.state == "SHOOT" and self.frame_index == 4:
                self.game.fire_bullet()

        if self.change_x < 0:
            self.scale_x = -1
        elif self.change_x > 0:
            self.scale_x = 1

# Ennemies / zombie
class Zombie(Enemy):
    def __init__(self, x, y, character_type, speed=None, hp=None, name_or_precise_type=None):
        super().__init__(x, y, character_type, speed, hp, name_or_precise_type)


# Joueur
class Player(Entity):
    def __init__(self, x, y, character_type, speed = None, hp = None, name_or_precise_type = None):
        super().__init__(x, y, character_type, speed, hp, name_or_precise_type)


# Items
class Item(Entity):
    def __init__(self, x, y, character_type, speed = None, hp = None, name_or_precise_type = None):
        super().__init__(x, y, character_type, speed, hp, name_or_precise_type)