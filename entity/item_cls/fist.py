from LOGIC.entity.item_cls.sword import Sword


IMG_COIN = ":resources:/images/items/coinGold.png"

class Fist(Sword):
    type = "fist sword"
    damage = 1
    path_or_texture = IMG_COIN
    def __init__(self, x, y, gameview):
        super().__init__(x, y, gameview=gameview, texture = self.path_or_texture, damage=self.damage)
    
    @staticmethod
    def get_damage():
        return 1