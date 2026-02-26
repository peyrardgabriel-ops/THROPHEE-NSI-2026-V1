import math

from LOGIC.entity.entity import Entity

IMG_COIN = ":resources:/images/items/coinGold.png"


class Item(Entity):
    type = "item"

    def __init__(self, x, y,
                path_or_texture = IMG_COIN):
        super().__init__(x, y, path_or_texture= path_or_texture)
        

class Printed_circuit(Item):
    type = "printed circuit"
    path_or_texture = IMG_COIN
    def __init__(self, x, y):
        super().__init__(x, y, path_or_texture = self.path_or_texture)
        


