import arcade

# Player
IMG_PLAYER = ":resources:/images/animated_characters/male_adventurer/maleAdventurer_idle.png"

# Ennemies
IMG_ZOMBIE = ":resources:/images/animated_characters/zombie/zombie_idle.png"
IMG_ROBOT = ":resources:/images/animated_characters/robot/robot_idle.png"

# Items
IMG_COIN = ":resources:/images/items/coinGold.png"


class Entity(arcade.Sprite):
    ALL_ENEMY = ["zombie", "robot"]
    def __init__(self,
                    x: int | float,
                    y:int | float,
                    character_type:str,
                    speed:int = None,
                    hp:int = None,
                    name_or_precise_type:str | None = None):
        
        # Récupère la texture du Sprite 
        match character_type:
            case "player":
                self.path_or_texture  = IMG_PLAYER
                self.character_scale = 1.0
            case "enemy":
                self.character_scale = 1.0
                self.detection_range = 800
                self.drop_loot = "bone"
                match name_or_precise_type:
                    case "zombie":
                        self.drop_loot = "rooten flesh"
                        self.path_or_texture = IMG_ZOMBIE
                    case "robot":
                        self.drop_loot = "gear wheel"
                        self.path_or_texture = IMG_ROBOT
                    case _:
                        self.path_or_texture = self.path_or_texture = IMG_ZOMBIE
            case "item":
                self.path_or_texture = IMG_COIN
                self.character_scale = 1
            case _:
                self.path_or_texture = None


        super().__init__(path_or_texture=self.path_or_texture, scale=self.character_scale)

        # Position
        self.center_x = x
        self.center_y = y

        # Autres caractéristiques
        self.hp = hp
        self.character_type = character_type
        self.speed = speed
        self.name_or_precise_type = name_or_precise_type 