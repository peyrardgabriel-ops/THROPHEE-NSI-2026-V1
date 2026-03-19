from GAME.entity.item_cls.sword import Sword
from GAME.entity.item import Item
from GAME.textures.load_sheet import load_sheet


IMG_COIN = "GAME/textures/item/sword/fist.png"

texture = load_sheet(IMG_COIN, 6)

class Fist(Sword, Item):
    type = "fist sword"
    damage = 1
    scale_factor = 10
    path_or_texture = texture
    def __init__(self, x, y, gameview):
        super().__init__(x, y, gameview=gameview, texture = self.path_or_texture, damage=self.damage, scale=self.scale_factor)
    