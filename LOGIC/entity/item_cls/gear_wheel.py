from LOGIC.entity import Item

IMG_GEAR_WHEEL = "LOGIC/textures/item/gear_wheel/gear_wheel.png"

class Gear_wheel(Item):
    type = "gear wheel"
    path_or_texture = IMG_GEAR_WHEEL

    def __init__(self, x, y, **kwargs):
        super().__init__(x, y, path_or_texture = self.path_or_texture)