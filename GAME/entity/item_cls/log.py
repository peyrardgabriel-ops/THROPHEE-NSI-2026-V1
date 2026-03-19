from GAME.entity import Item

IMG_LOG = "GAME/textures/item/log/log.png"

class Log(Item):
    type = "log"
    path_or_texture = IMG_LOG

    def __init__(self, x, y, **kwargs):
        super().__init__(x, y, path_or_texture = self.path_or_texture)