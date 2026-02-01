import arcade
import random
import os

TILE_SIZE = 60      # taille des tiles
MAP_WIDTH = 50      # nombre de tiles horizontal
MAP_HEIGHT = 30     # nombre de tiles vertical
CAMERA_SPEED = 5    # vitesse de la caméra (pixels par frame)
SCREEN_WIDTH = 1280 # largeur de la fenêtre
SCREEN_HEIGHT = 720 # hauteur de la fenêtre


BASE_DIR = os.path.dirname(__file__)
TILE_FOLDER = os.path.join(BASE_DIR, "assets", "tiles")

tile_files = [
    os.path.join(TILE_FOLDER, "0-grass.png"),
    os.path.join(TILE_FOLDER, "1-grass.png"),
    os.path.join(TILE_FOLDER, "2-bush.png"),
    os.path.join(TILE_FOLDER, "2-flower.png"),
]


window = arcade.Window(fullscreen=True, title="MAP-1", vsync=True)


class TileMapGame(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.SKY_BLUE)

      
        self.tile_list = arcade.SpriteList()
        self.setup()

        
        self.camera = arcade.camera.Camera2D()
        self.camera.scale = 1.0

       
        center_x = (MAP_WIDTH * TILE_SIZE) / 2
        center_y = (MAP_HEIGHT * TILE_SIZE) / 2
        self.camera.position = (
            center_x - MAP_WIDTH / 2,
            center_y - MAP_HEIGHT / 2
        )

        self.camera_target_x, self.camera_target_y = self.camera.position

        self.keys_held = set()

  
    def setup(self) -> None:
        for row in range(MAP_HEIGHT):
            for col in range(MAP_WIDTH):
                tile_image = random.choice(tile_files)
                tile = arcade.Sprite(tile_image, scale=0.5)
                tile.center_x = col * TILE_SIZE + TILE_SIZE // 2
                tile.center_y = row * TILE_SIZE + TILE_SIZE // 2
                self.tile_list.append(tile)

  
    def on_draw(self) -> None:
        self.clear()
        self.camera.use()
        self.tile_list.draw()

 
    def on_key_press(self, key, modifiers) -> None:
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        else:
            self.keys_held.add(key)

  
    def on_key_release(self, key, modifiers) -> None:
        if key in self.keys_held:
            self.keys_held.remove(key)

    
    def on_update(self, delta_time: float) -> None:
        if arcade.key.Z in self.keys_held:
            self.camera_target_y += CAMERA_SPEED
        if arcade.key.S in self.keys_held:
            self.camera_target_y -= CAMERA_SPEED
        if arcade.key.Q in self.keys_held:
            self.camera_target_x -= CAMERA_SPEED
        if arcade.key.D in self.keys_held:
            self.camera_target_x += CAMERA_SPEED

        
        self.camera.position = (round(self.camera_target_x), round(self.camera_target_y))



def main():
    game = TileMapGame()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()



