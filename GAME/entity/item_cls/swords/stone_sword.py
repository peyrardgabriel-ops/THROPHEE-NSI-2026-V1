from GAME.entity.item_cls.sword import Sword
from GAME.entity.item import Item
from GAME.textures.load_sheet import load_sheet

IMG_SWORD = "GAME/textures/item/sword/stone sword.png"

sword_texture = load_sheet(IMG_SWORD, 6)

class StoneSword(Sword, Item):
    damage = 4
    scale_factor = 2
    type = "stone sword"
    path_or_texture = sword_texture
    def __init__(self, x, y, gameview):
        super().__init__(x, y, texture = self.path_or_texture, damage=self.damage, gameview=gameview)
        
