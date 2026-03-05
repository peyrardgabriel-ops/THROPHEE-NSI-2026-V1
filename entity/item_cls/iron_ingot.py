from LOGIC.entity import Item

IMG_COIN = ":resources:/images/items/coinGold.png"

class IronIngot(Item):
    type = "iron ingot"
    path_or_texture = IMG_COIN
    def __init__(self, x, y, **kwargs):
        super().__init__(x, y, path_or_texture = self.path_or_texture)