from LOGIC.entity.item_cls.sword import Sword
from LOGIC.entity.item import Item
from LOGIC.textures.load_sheet import load_sheet

IMG_SWORD = "LOGIC/textures/item/sword/stone sword.png"

class StoneSword(Sword, Item):
    damage = 4
    type = "stone sword"
    img_texture = load_sheet(IMG_SWORD, 6)
    path_or_texture = img_texture[1]
    def __init__(self, x, y, gameview):
        super().__init__(x, y, texture = self.path_or_texture, damage=self.damage, gameview=gameview)
