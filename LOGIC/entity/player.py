from LOGIC.entity.entity2 import Entity

IMG_PLAYER = ":resources:/images/animated_characters/male_adventurer/maleAdventurer_idle.png"
PLAYER_SPEED = 400

class Player(Entity):
    def __init__(self, x, y, name_or_precise_type = None):
        self.hp = 100
        self.speed = PLAYER_SPEED
        super().__init__(x, y, name_or_precise_type, path_or_texture=IMG_PLAYER,  speed=self.speed, hp = self.hp)

        self.center_x = x
        self.center_y = y