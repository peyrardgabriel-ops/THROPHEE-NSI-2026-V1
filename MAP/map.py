import arcade
import random
import os

# CONSTANTES
TILE_SIZE = 60     # taille des tiles
MAP_WIDTH = 50      # nombre de tiles horizontal
MAP_HEIGHT = 30     # nombre de tiles vertical
TILE_FOLDER = "assets/tiles"  # chemin vers les tiles
CAMERA_SPEED = 5    # vitesse de la caméra (pixels par frame)

# Liste des chemins d'accès aux images de tiles
tile_files = [os.path.join(TILE_FOLDER, f) for f in [
    "0-grass.png",
    "1-grass.png",
    "2-bush.png",
    "2-flower.png"
]]

# FENETRE / JEU
class TileMapGame(arcade.Window):
    def __init__(self):
        super().__init__(fullscreen=True, title="MAP-1")
        arcade.set_background_color(arcade.color.SKY_BLUE)

        # Taille de l'écran
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = self.get_size()

        # Liste des tiles
        self.tile_list = arcade.SpriteList()
        self.setup()

        # Créer la caméra et la centrer sur le milieu de la map
        self.camera = arcade.camera.Camera2D()
        self.camera.scale = 1.0  # garder scale = 1 pour pixel-art
        center_x = (MAP_WIDTH * TILE_SIZE) / 2
        center_y = (MAP_HEIGHT * TILE_SIZE) / 2
        self.camera.position = (
            center_x - self.SCREEN_WIDTH / 2,
            center_y - self.SCREEN_HEIGHT / 2
        )

        # Position cible pour smooth movement
        self.camera_target_x, self.camera_target_y = self.camera.position

        # Touches enfoncées
        self.keys_held = set()

    def setup(self):
        """Générer la map aléatoire"""
        for row in range(MAP_HEIGHT):
            for col in range(MAP_WIDTH):
                tile_image = random.choice(tile_files)
                tile = arcade.Sprite(tile_image, scale=0.5)
                tile.center_x = col * TILE_SIZE + TILE_SIZE // 2
                tile.center_y = row * TILE_SIZE + TILE_SIZE // 2
                self.tile_list.append(tile)

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.tile_list.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        else:
            self.keys_held.add(key)

    def on_key_release(self, key, modifiers):
        if key in self.keys_held:
            self.keys_held.remove(key)

    def on_update(self, delta_time):
        if arcade.key.Z in self.keys_held:
            self.camera_target_y += CAMERA_SPEED
        if arcade.key.S in self.keys_held:
            self.camera_target_y -= CAMERA_SPEED
        if arcade.key.Q in self.keys_held:
            self.camera_target_x -= CAMERA_SPEED
        if arcade.key.D in self.keys_held:
            self.camera_target_x += CAMERA_SPEED

        # Smooth movement
        lerp_factor = 0.1
        cam_x = self.camera.position[0] + (self.camera_target_x - self.camera.position[0]) * lerp_factor
        cam_y = self.camera.position[1] + (self.camera_target_y - self.camera.position[1]) * lerp_factor
        self.camera.position = (round(cam_x), round(cam_y))


# LANCEMENT
def main():
    game = TileMapGame()
    arcade.run()


if __name__ == "__main__":
    main()

