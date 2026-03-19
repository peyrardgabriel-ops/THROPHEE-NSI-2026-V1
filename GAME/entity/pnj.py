import random

from GAME.entity.entity import Entity



PNJ_HP = 20
PNJ_TEXTURES = {"woman": "GAME/textures/pnj/img_woman.png",
                "man": "GAME/textures/pnj/img_man.png"}

class Pnj(Entity):
    def __init__(self, x, y, trade=None):
        self.hp = PNJ_HP 
        texture = random.choice([PNJ_TEXTURES["man"], PNJ_TEXTURES["woman"]])

        super().__init__(x=x,
                         y=y,
                         path_or_texture=texture,
                         hp=self.hp)
        self.center_x = x
        self.center_y = y

    def trade(self, item_to_trade_for):
        ...