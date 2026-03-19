from GAME.entity import Item

IMG_STICK = "GAME/textures/item/stick/stick.png"

class Stick(Item):
    type = "stick"
    path_or_texture = IMG_STICK
    def __init__(self, x, y, **kwargs):
        super().__init__(x, y, path_or_texture = self.path_or_texture)