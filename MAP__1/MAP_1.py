import arcade
import random
import os
import json

# --- Configuration ---
MAIN_PATH = os.path.dirname(os.path.abspath(__file__))
TILE_SIZE = 120
CHUNK_SIZE = 8       
VIEW_DISTANCE = 3    
SCREEN_TITLE = "Moteur NSI - Optimisation Debug"

PLAYER_SPEED = 8
ZOOM_LEVEL = 0.5 

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(title=SCREEN_TITLE, fullscreen=True, antialiasing=True)
        self.tile_list = arcade.SpriteList()
        self.scene_list = arcade.SpriteList() 
        self.hit_box_list = arcade.SpriteList() 
        
        self.player = None
        self.camera = None
        self.pressed_keys = set()
        self.loaded_chunks = {} 
        self.map_memory = {}    
        self.show_hitboxes = False
        
        self.load_save_file()

    def load_save_file(self):
        path = os.path.join(MAIN_PATH, "map_data.json")
        if os.path.exists(path):
            try:
                with open(path, "r") as f: self.map_memory = json.load(f)
            except: self.map_memory = {}

    def setup(self):
        self.camera = arcade.camera.Camera2D()
        self.camera.zoom = ZOOM_LEVEL
        
        pos = self.map_memory.get("player_pos", {"x": 500, "y": 500})
        self.player = arcade.Sprite(arcade.make_soft_circle_texture(TILE_SIZE // 3, arcade.color.BLUE))
        self.player.position = (pos["x"], pos["y"])
        self.player.hit_box_points = [(-15, -15), (15, -15), (15, 15), (-15, 15)]
        self.scene_list.append(self.player)
        
        self.tex_tiles = [arcade.load_texture(os.path.join(MAIN_PATH, f"herbe_{i}.png")) for i in range(1, 5)]
        self.tree_tex = arcade.load_texture(os.path.join(MAIN_PATH, "arbre.png"))
        self.rock_tex = arcade.load_texture(os.path.join(MAIN_PATH, "rocher.png"))

    def generate_chunk(self, cx, cy):
        chunk_key = f"{cx},{cy}"
        if chunk_key not in self.map_memory:
            chunk_data = []
            for row in range(CHUNK_SIZE):
                for col in range(CHUNK_SIZE):
                    tx, ty = cx * CHUNK_SIZE + col, cy * CHUNK_SIZE + row
                    rand = random.random()
                    obj = "tree" if rand < 0.08 else ("rock" if rand < 0.12 else None)
                    chunk_data.append({"tx": tx, "ty": ty, "type": obj, "tex_idx": random.randint(0, 3)})
            self.map_memory[chunk_key] = chunk_data

        for item in self.map_memory[chunk_key]:
            tile = arcade.Sprite(self.tex_tiles[item['tex_idx']])
            tile.center_x, tile.center_y = item['tx'] * TILE_SIZE, item['ty'] * TILE_SIZE
            self.tile_list.append(tile)

            if item['type'] == "tree":
                tree = arcade.Sprite(self.tree_tex)
                tree.center_x = tile.center_x
                tree.bottom = tile.bottom + 5
                tree.properties["type"] = "tree"
                tree.hit_box_points = [] 
                self.scene_list.append(tree)

                hb = arcade.SpriteSolidColor(100, 100, arcade.color.WHITE)
                hb.center_x = tree.center_x
                hb.center_y = tree.center_y - 100
                hb.alpha = 0 
                self.hit_box_list.append(hb)

            elif item['type'] == "rock" and item['tex_idx'] == 0:
                rock = arcade.Sprite(self.rock_tex, scale=2.0)
                rock.center_x, rock.center_y = tile.center_x, tile.center_y
                self.scene_list.append(rock)
                self.hit_box_list.append(rock)

    def on_update(self, delta_time):
        old_pos = self.player.position
        
        if arcade.key.Z in self.pressed_keys: self.player.center_y += PLAYER_SPEED
        if arcade.key.S in self.pressed_keys: self.player.center_y -= PLAYER_SPEED
        if arcade.key.Q in self.pressed_keys: self.player.center_x -= PLAYER_SPEED
        if arcade.key.D in self.pressed_keys: self.player.center_x += PLAYER_SPEED

        if arcade.check_for_collision_with_list(self.player, self.hit_box_list):
            self.player.position = old_pos

        for s in self.scene_list:
            if s.properties.get("type") == "tree":
                dist = arcade.get_distance_between_sprites(self.player, s)
                if dist < 220 and self.player.center_y > s.center_y:
                    s.alpha = 140
                else:
                    s.alpha = 255

        p_cx, p_cy = int(self.player.center_x // (CHUNK_SIZE * TILE_SIZE)), int(self.player.center_y // (CHUNK_SIZE * TILE_SIZE))
        for y in range(p_cy - VIEW_DISTANCE, p_cy + VIEW_DISTANCE + 1):
            for x in range(p_cx - VIEW_DISTANCE, p_cx + VIEW_DISTANCE + 1):
                if (x, y) not in self.loaded_chunks:
                    self.loaded_chunks[(x, y)] = True
                    self.generate_chunk(x, y)
        self.camera.position = self.player.position

    def on_draw(self):
        self.clear()
        self.camera.use()
        
        self.tile_list.draw()
        
        self.scene_list.sort(key=lambda x: x.center_y, reverse=True)
        self.scene_list.draw(pixelated=True)
        
        # --- DEBUG OPTIMISÉ ---
        if self.show_hitboxes:
            # On dessine toutes les hitboxes de la liste en un seul appel (très rapide)
            self.hit_box_list.draw_hit_boxes(arcade.color.WHITE, line_thickness=2)
            # Et celle du joueur
            self.player.draw_hit_box(arcade.color.RED, line_thickness=2)

    def on_key_press(self, key, modifiers):
        self.pressed_keys.add(key)
        if key == arcade.key.F:
            self.show_hitboxes = not self.show_hitboxes
        if key == arcade.key.ESCAPE:
            self.close()

    def on_key_release(self, key, modifiers):
        if key in self.pressed_keys:
            self.pressed_keys.remove(key)

if __name__ == "__main__":
    game = MyGame()
    game.setup()
    arcade.run()