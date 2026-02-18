import arcade

class Entity(arcade.Sprite):
    
    def __init__(self, x, y,
                name_or_precise_type = None,
                path_or_texture=None,
                character_scale : float | int = 1,
                detection_range : int = 300,
                speed : int = None,
                hp : int = 100,
                damage : int = 10,
                bullet_list = None):
        
        
        super().__init__(path_or_texture= path_or_texture, scale= character_scale)

        # Position
        self.center_x = x
        self.center_y = y

        # Autres caractéristiques
        self.name_or_precise_type = name_or_precise_type 
        self.bullet_list = bullet_list