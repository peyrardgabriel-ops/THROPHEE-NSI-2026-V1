import arcade
from LOGIC.entity.entity2 import Entity


class Enemy(Entity):
    enemy_list = arcade.SpriteList()
    def __init__(self, x, y,
                name_or_precise_type = None,
                path_or_texture=None,
                detection_range : int = 300,
                speed : int = None,
                hp : int = 100,
                damage : int = 10,
                bullet_list = None):
        self.path_or_texture = path_or_texture
        self.bullet_list = arcade.SpriteList()
        
       

        super().__init__(x, y,
                        name_or_precise_type,
                        self.path_or_texture)
        