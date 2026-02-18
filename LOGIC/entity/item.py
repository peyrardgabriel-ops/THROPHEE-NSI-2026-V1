from LOGIC.entity.entity2 import Entity

IMG_COIN = ":resources:/images/items/coinGold.png"

class Item(Entity):
    def __init__(self, x, y,
                name_or_precise_type = None,
                path_or_texture = IMG_COIN):
        super().__init__(x, y, name_or_precise_type=name_or_precise_type, path_or_texture= path_or_texture)

class Gear_wheel(Item):
    def __init__(self, x, y, name_or_precise_type=None):
        super().__init__(x, y, name_or_precise_type)