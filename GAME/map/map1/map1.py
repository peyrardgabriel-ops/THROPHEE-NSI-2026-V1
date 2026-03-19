import arcade
import random
import os
import json

# --- Configuration ---
MAIN_PATH = os.path.dirname(os.path.abspath(__file__))
TILE_SIZE = 120
CHUNK_SIZE = 8       
VIEW_DISTANCE = 3    

# --- SEED (La graine du monde) ---
# Change ce nombre pour générer un monde totalement différent
WORLD_SEED = 12345 

# --- LIMITES DU MONDE ---
MAP_LIMIT_MIN = -5  
MAP_LIMIT_MAX = 5   

class MapEngine:
    def __init__(self, player):
        self.player = player
        
        self.tile_list = arcade.SpriteList()
        self.scene_list = arcade.SpriteList() 
        self.hit_box_list = arcade.SpriteList()
        
        self.camera = None
        self.loaded_chunks = {} 
        self.map_memory = {}    # Garde les chunks en mémoire vive pendant la session
        self.show_hitboxes = False

        self.can_attack = True
        self.can_enemy_spawn = True
        self.can_pnj_spawn = True

    def setup(self):
        self.camera = arcade.camera.Camera2D()
        
        if self.player not in self.scene_list:
            self.scene_list.append(self.player)
        
        # Chargement des textures
        self.tex_tiles = [arcade.load_texture(os.path.join(MAIN_PATH, f"herbe_{i}.png")) for i in range(1, 5)]
        self.tree_tex = arcade.load_texture(os.path.join(MAIN_PATH, "arbre.png"))
        self.rock_tex = arcade.load_texture(os.path.join(MAIN_PATH, "rocher.png"))

    def generate_chunk(self, cx, cy):
        chunk_key = f"{cx},{cy}"
        
        # --- LOGIQUE DE LA SEED ---
        # On initialise le générateur aléatoire spécifiquement pour ce chunk
        # cx * 1000 + cy crée un identifiant unique pour chaque position
        random.seed(WORLD_SEED + (cx * 1000 + cy))
        
        if chunk_key not in self.map_memory:
            chunk_data = []
            for row in range(CHUNK_SIZE):
                for col in range(CHUNK_SIZE):
                    tx, ty = cx * CHUNK_SIZE + col, cy * CHUNK_SIZE + row
                    rand = random.random()
                    obj = "tree" if rand < 0.08 else ("rock" if rand < 0.12 else None)
                    chunk_data.append({"tx": tx, "ty": ty, "type": obj, "tex_idx": random.randint(0, 3)})
            self.map_memory[chunk_key] = chunk_data

        # Création des sprites (identique à avant)
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

                hb = arcade.SpriteSolidColor(100, 40, arcade.color.WHITE)
                hb.center_x, hb.center_y = tree.center_x, tree.center_y - 100
                hb.alpha = 0 
                hb.properties["type"] = "tree"
                hb.hp, hb.max_hp = 5, 5
                hb.drop_loot = "log"
                self.hit_box_list.append(hb)

            elif item['type'] == "rock" and item['tex_idx'] == 0:
                rock = arcade.Sprite(self.rock_tex, scale=2.0)
                rock.center_x, rock.center_y = tile.center_x, tile.center_y
                rock.properties["type"] = "rock"
                rock.hp, rock.max_hp = 10, 10
                rock.drop_loot = "stone"
                self.scene_list.append(rock)
                self.hit_box_list.append(rock)
        
        # TRÈS IMPORTANT : On remet une seed aléatoire pour ne pas bloquer 
        # le reste du jeu (mouvements ennemis, drops, etc.) sur la même valeur
        random.seed()

    def update(self, delta_time):
        # Murs invisibles
        min_px = MAP_LIMIT_MIN * CHUNK_SIZE * TILE_SIZE
        max_px = (MAP_LIMIT_MAX + 1) * CHUNK_SIZE * TILE_SIZE - TILE_SIZE

        self.player.center_x = max(min_px, min(self.player.center_x, max_px))
        self.player.center_y = max(min_px, min(self.player.center_y, max_px))

        # Transparence arbres
        for s in self.scene_list:
            if s.properties.get("type") == "tree":
                dist = arcade.get_distance_between_sprites(self.player, s)
                s.alpha = 140 if (dist < 220 and self.player.center_y > s.center_y) else 255

        # Chargement chunks dans les limites
        p_cx = int(self.player.center_x // (CHUNK_SIZE * TILE_SIZE))
        p_cy = int(self.player.center_y // (CHUNK_SIZE * TILE_SIZE))

        for y in range(p_cy - VIEW_DISTANCE, p_cy + VIEW_DISTANCE + 1):
            for x in range(p_cx - VIEW_DISTANCE, p_cx + VIEW_DISTANCE + 1):
                if MAP_LIMIT_MIN <= x <= MAP_LIMIT_MAX and MAP_LIMIT_MIN <= y <= MAP_LIMIT_MAX:
                    if (x, y) not in self.loaded_chunks:
                        self.loaded_chunks[(x, y)] = True
                        self.generate_chunk(x, y)

        self.camera.position = self.player.position

    def draw(self):
        self.camera.use()
        self.tile_list.draw()
        
        if self.player not in self.scene_list:
            self.scene_list.append(self.player)

        self.scene_list.sort(key=lambda x: x.center_y, reverse=True)
        self.scene_list.draw(pixelated=True)
        
        if self.show_hitboxes:
            self.hit_box_list.draw_hit_boxes(arcade.color.WHITE, line_thickness=2)
            self.player.draw_hit_box(arcade.color.RED, line_thickness=2)