from LOGIC.entity import Item

IMG_PLANK = "LOGIC/textures/item/plank/plank.png"

class Plank(Item):
    type = "plank"
    path_or_texture = IMG_PLANK
    def __init__(self, x, y):
        super().__init__(x, y, path_or_texture = self.path_or_texture)