import arcade

class ButtonSprite(arcade.Sprite):
    def __init__(self, center_x, center_y, width, height, color, text):
        # Création d'une texture simple pour le sprite
        texture = arcade.make_soft_square_texture(width, color, outer_alpha=color[3])
        super().__init__(texture, scale=1.0)
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.label = arcade.Text(text=self.text,
                                    x = self.center_x,
                                    y = self.center_y,
                                    color = arcade.color.BLACK,
                                    font_size= 20,
                                    anchor_x="center",
                                    anchor_y="center")
        self.base_width = self.width
        self.base_height = self.height