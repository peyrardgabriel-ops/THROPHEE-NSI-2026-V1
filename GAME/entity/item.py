import math

from GAME.entity.entity import Entity

IMG_COIN = "GAME/textures/item/coin/coin.png"


class Item(Entity):
    type = "item"

    def __init__(self, x, y,
                path_or_texture = IMG_COIN,
                scale = 1,
                **kwargs):
        if isinstance(path_or_texture, list):
            path_or_texture = path_or_texture[0]
        super().__init__(x, y, path_or_texture= path_or_texture, character_scale=scale)
        