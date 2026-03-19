from GAME.entity.item import Item


IMG_COIN = "GAME/textures/item/coin/coin.png"

class Coin(Item):
    type = "coin"
    path_or_texture = IMG_COIN
    scale = 1
    def __init__(self, x, y, **kwargs):
        super().__init__(x, y, path_or_texture = self.path_or_texture, scale=0.2)