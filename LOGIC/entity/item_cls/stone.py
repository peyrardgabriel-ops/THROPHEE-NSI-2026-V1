from LOGIC.entity import Item

IMG_STONE = "LOGIC/textures/item/stone/stone.png"

class Stone(Item):
    type = "stone"
    path_or_texture = IMG_STONE

    def __init__(self, x, y, **kwargs):
        super().__init__(x, y, path_or_texture = self.path_or_texture)