from GAME.entity.item_cls.sword import Sword
from GAME.entity.item import Item
from GAME.textures.load_sheet import load_sheet

IMG_SWORD = "GAME/textures/item/sword/iron sword.png"

texture = load_sheet(IMG_SWORD, 6)

class IronSword(Sword, Item):
    damage = 7
    scale_factor = 2
    type = "iron sword"
    path_or_texture = texture
    def __init__(self, x, y, gameview):
        super().__init__(x, y, texture = self.path_or_texture, damage=self.damage, gameview=gameview)
       
    