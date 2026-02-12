import arcade
import math
import random
from Save.save import save_file, load_file
from menu_ingame.menu_ingamev1 import InGameMenu

# Taille des écrans / fenetre
MAP_HEIGHT = 5000
MAP_WIDTH = 5000

# Taille des diff mobs
PLAYER_SIZE = 50
ENEMY_SIZE = 45

# Vitesse des diff mobs
PLAYER_SPEED = 400
ENEMY_SPEED = 300
CAMERA_PAN_SPEED = 0.2

class GameView(arcade.View):
    def __init__(self) -> None:
        super().__init__()
        arcade.set_background_color(arcade.color.BLUE_SAPPHIRE)

        self.data = load_file()
        
        # Joueur 
        self.player_list = arcade.SpriteList()
        self.player = arcade.SpriteSolidColor(
            width=PLAYER_SIZE,
            height= PLAYER_SIZE,
            color= arcade.color.WHITE
        )
        self.player.center_x = self.data["player"]["player_x"]
        self.player.center_y= self.data["player"]["player_y"]
        self.player_hp = 10

        self.player_list.append(self.player)

        self.direction = set()

        # Ennemis 
        self.enemy_list = arcade.SpriteList()
        self.create_enemies()

        # Caméra
        self.camera = arcade.camera.Camera2D()
        

        # Sauvegarde + Inventaire
        self.inventory = {}
        self.stuff_to_save = {}

        # Test
        self.is_debug_menu_open = False

        
        

    def on_draw(self) -> None:

        self.camera.use()
        self.clear()
        arcade.draw_lbwh_rectangle_filled(left=0,
                                          bottom=0,
                                          width=MAP_WIDTH,
                                          height=MAP_HEIGHT,
                                          color= arcade.color.DARK_GREEN)
        self.player_list.draw()
        self.enemy_list.draw()
        
        # Test avec affichage de la position du joueur 
        if self.is_debug_menu_open:
            arcade.draw_text(x= self.camera_x - ((self.window.width - PLAYER_SIZE) // 2),
                         y= self.camera_y - ((self.window.height - PLAYER_SIZE) // 2),
                         text=f"x : {self.player.center_x} -- y : {self.player.center_y}")
            arcade.draw_text(x= self.camera_x - ((self.window.width - PLAYER_SIZE) // 2),
                             y= self.camera_y + ((self.window.height - PLAYER_SIZE) // 2),
                             text=f"HP : {self.player_hp}-- nbr_enemy : {len(self.enemy_list)}")



    def on_update(self, delta_time:float) -> None:
        # Gestion des mouvements 
        if arcade.key.Z in self.direction:
            self.player.center_y += PLAYER_SPEED * delta_time
        if arcade.key.S in self.direction:
            self.player.center_y -= PLAYER_SPEED * delta_time
        if arcade.key.D in self.direction:
            self.player.center_x += PLAYER_SPEED * delta_time
            self.player.scale_x = 1
        if arcade.key.Q in self.direction:
            self.player.center_x -= PLAYER_SPEED * delta_time
            self.player.scale_x = -1

        if self.player.center_x + (PLAYER_SIZE // 2) > MAP_WIDTH:
            self.player.center_x -= PLAYER_SPEED * delta_time
        if self.player.center_x - (PLAYER_SIZE // 2) < 0:
            self.player.center_x += PLAYER_SPEED * delta_time
        if self.player.center_y + (PLAYER_SIZE // 2) > MAP_HEIGHT:
            self.player.center_y -= PLAYER_SPEED * delta_time
        if self.player.center_x - (PLAYER_SIZE // 2) < 0:
            self.player.center_y += PLAYER_SPEED * delta_time


        if arcade.key.F3 in self.direction:
            self.is_debug_menu_open = not self.is_debug_menu_open
        
        # Caméra qui suit le player
        self.camera_x, self.camera_y = self.camera.position
        self.pan_camera_to_player(CAMERA_PAN_SPEED)


        # Mise a jour des infos a sauvegarder
        self.stuff_to_save = {
            "player": {
                "player_x": self.player.center_x,
                "player_y": self.player.center_y
            },
            "inventory": self.inventory
        }
        # IA des ennemis pr aller vers le player
        for enemy in self.enemy_list:
            if math.dist((enemy.center_x, enemy.center_y),(self.player.center_x,self.player.center_y)) <= 750:            
                angle_player_enemy = math.atan2((self.player.center_y - enemy.center_y),
                                                (self.player.center_x - enemy.center_x ))
                last_value_x, last_value_y = enemy.center_x, enemy.center_y
                enemy.center_x += math.cos(angle_player_enemy) * ENEMY_SPEED * delta_time
                if arcade.check_for_collision_with_list(enemy, self.enemy_list):
                    enemy.center_x = last_value_x
                if math.cos(angle_player_enemy) * ENEMY_SPEED * delta_time > 0:
                    enemy.scale_x = 1
                else:
                    enemy.scale_x = -1

                enemy.center_y += math.sin(angle_player_enemy) * ENEMY_SPEED * delta_time
                if arcade.check_for_collision_with_list(enemy, self.enemy_list):
                    enemy.center_y = last_value_y
            

            # Regarde si un ennemi touche le joueur et lui enlève un HP
            if arcade.check_for_collision_with_list(enemy, self.player_list):
                self.player_hp -= 1
                enemy.remove_from_sprite_lists()

        if len(self.enemy_list) < 50:
            missing_enemy = 50 - len(self.enemy_list) 
            self.create_enemies(number_of_enemies=missing_enemy)
            


    def on_key_press(self, symbol:int, modifiers:int) -> None:
        # Quitte directement si ESC est cliqué
        if symbol == arcade.key.ESCAPE:
            save_file(self.stuff_to_save)
            self.window.show_view(InGameMenu(self))
        else:
            self.direction.add(symbol)


    def on_key_release(self, symbol:int, modifiers:int) -> None:
        if symbol in self.direction:
            self.direction.remove(symbol)


    def create_enemies(self, number_of_enemies:int = 100) -> None:
        """
        Create a list of enemy generated randomly all arround the map 
        """
        for _ in range(number_of_enemies) :
            placed = False
            while not placed:
                x = random.randint(0, MAP_WIDTH)
                y = random.randint(0, MAP_HEIGHT)
                enemy = arcade.SpriteSolidColor(
                    width= ENEMY_SIZE,
                    height= ENEMY_SIZE,
                    color= arcade.color.VIOLET
                )
                enemy.center_x = x
                enemy.center_y = y

                # Vérifie si il n'y a pas deja d'ennemis à l'endroit choisi
                if not arcade.check_for_collision_with_list(enemy, self.enemy_list):
                    placed = True
                    self.enemy_list.append(enemy)


    def pan_camera_to_player(self, panning_fraction: float = 1.0):
        """Manage scrolling -- from Arcade docs"""
        self.camera.position = arcade.math.smerp_2d(
            self.camera.position,
            self.player.position,
            self.window.delta_time,
            panning_fraction
        )
