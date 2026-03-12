from LOGIC.entity.item_cls.sword import Sword
from LOGIC.entity.item import Item

IMG_SWORD = "LOGIC/textures/item/sword/wooden sword.png"

class WoodenSword(Sword, Item):
    damage = 3
    type = "wooden sword"
    path_or_texture = IMG_SWORD
    def __init__(self, x, y, gameview):
        super().__init__(x, y, texture = self.path_or_texture, damage=self.damage, gameview=gameview)

