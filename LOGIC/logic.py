import arcade
import math
import random
from LOGIC.Save.save import save_file, load_file
from LOGIC.menu_ingame.menu_ingamev1 import InGameMenu
import LOGIC.entity as entity

# Taille des écrans / fenetre
MAP_HEIGHT = 5000
MAP_WIDTH = 5000

# Taille des diff mobs
PLAYER_SIZE = 50
ENEMY_SIZE = 45
ITEM_SIZE = 30

# Vitesse des diff mobs
PLAYER_SPEED = 400
CAMERA_PAN_SPEED = 0.2

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.LIGHT_BLUE)

        # Recupère les données stockées
        data = load_file()

        # Deplacement
        self.key_pressed = set()

        # Player
        self.player_list = arcade.SpriteList()
        self.player = entity.Player(x= data["player"]["player_x"],
                             y= data["player"]["player_y"],
                             name_or_precise_type = "JP")
        self.attack_direction = 1
        self.player_list.append(self.player)

        # Ennemis 
        self.enemy_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.create_enemy(100)

        # Items 
        self.item_list = arcade.SpriteList()
        
        # Caméra
        self.camera = arcade.camera.Camera2D()
        self.camera_x, self.camera_y = self.camera.position
        

        # Débug Menu
        self.is_debug_menu_open = False

        # Inventaire
        self.inventory = data["inventory"]

        # Sauvegarde
        self.stuff_to_save = {
                            "player":{
                                "player_x":self.player.center_x,
                                "player_y": self.player.center_y
                                },
                            "inventory": self.inventory
                            }
        
        
        

    def on_draw(self):
        self.camera.use()
        self.clear()

        # la map actuelle ;(
        arcade.draw_lbwh_rectangle_filled(left=0,
                                          bottom=0,
                                          width=MAP_WIDTH,
                                          height=MAP_HEIGHT,
                                          color=arcade.color.BLUE_SAPPHIRE)
        
        
        self.item_list.draw()
        self.player_list.draw()
        self.enemy_list.draw()
        self.enemy_bullet_list.draw()

        # Débug Menu 
        if self.is_debug_menu_open:
            arcade.draw_text(x= self.camera_x - ((self.window.width - PLAYER_SIZE) // 2),
                            y= self.camera_y - ((self.window.height - PLAYER_SIZE) // 2),
                            text=f"x : {self.player.center_x:.2f} -- y : {self.player.center_y:.2f}")
            arcade.draw_text(x= self.camera_x - ((self.window.width - PLAYER_SIZE) // 2),
                             y= self.camera_y + ((self.window.height - PLAYER_SIZE) // 2),
                             text=f"camera_x : {self.camera_x:.2f}-- camera_y : {self.camera_y:.2f}")
            arcade.draw_text(x= self.camera_x +((self.window.width - PLAYER_SIZE) // 2) - 150,
                             y= self.camera_y + ((self.window.height - PLAYER_SIZE) // 2),
                             text=f"number_of_enemy : {len(self.enemy_list)}")
            arcade.draw_text(x= self.camera_x +((self.window.width - PLAYER_SIZE) // 2) - 150,
                             y= self.camera_y - ((self.window.height - PLAYER_SIZE) // 2),
                             text=f"hp left : {self.player.hp}")
            self.player_list.draw_hit_boxes()
            self.enemy_bullet_list.draw_hit_boxes()
            self.enemy_list.draw_hit_boxes()


    def on_update(self, delta_time):
        if arcade.key.F3 in self.key_pressed:
            self.is_debug_menu_open = not self.is_debug_menu_open

        # Déplacements 
        if arcade.key.Z in self.key_pressed:
            self.player.center_y += self.player.speed * delta_time
        if arcade.key.S in self.key_pressed:
            self.player.center_y -= self.player.speed * delta_time
        if arcade.key.D in self.key_pressed:
            self.player.center_x += self.player.speed * delta_time
        if arcade.key.Q in self.key_pressed:
            self.player.center_x -= self.player.speed * delta_time

        # Caméra
        self.pan_camera_to_player(CAMERA_PAN_SPEED)
        self.camera_x, self.camera_y = self.camera.position

        # Déplacements des ennemies 
        for enemy in self.enemy_list:
            # si l'enemi peut il va attaquer
            if math.dist((enemy.center_x, enemy.center_y), (self.player.center_x, self.player.center_y)) < enemy.attack_range:
                enemy.state = "ATTACK" # joue l'animation d'attaque 

            # si l'ennemy est trop loin pr attaquer il va s'approcher
            elif math.dist((enemy.center_x, enemy.center_y), (self.player.center_x, self.player.center_y)) < enemy.detection_range:
                enemy.state = "RUN" # joue l'animation de déplacement 
                angle = math.atan2((self.player.center_y - enemy.center_y),
                                    (self.player.center_x - enemy.center_x))
                old_x, old_y = enemy.center_x, enemy.center_y
                enemy.center_x += math.cos(angle) * enemy.speed * delta_time

                if arcade.check_for_collision_with_list(enemy, self.enemy_list):
                    enemy.center_x = old_x

                if math.cos(angle) * enemy.speed * delta_time > 0:
                    enemy.scale_x = 1
                else:
                    enemy.scale_x = -1

                enemy.center_y += math.sin(angle) * enemy.speed * delta_time
                if arcade.check_for_collision_with_list(enemy, self.enemy_list):
                    enemy.center_y = old_y
            # si l'nnemi ne detecte pas le joueur, mouvement de base du ennemi
            else:
                enemy.movement()
            
            # Gestion des bordures de la map
            if enemy.left < 0:
                enemy.left = 0
            elif enemy.right > MAP_WIDTH:
                enemy.right = MAP_WIDTH

            if enemy.bottom < 0:
                enemy.bottom = 0
            elif enemy.top > MAP_HEIGHT:
                enemy.top = MAP_HEIGHT
           

            if arcade.check_for_collision_with_list(enemy, self.player_list):
                self.player.hp -= 1
                self.drop_item(enemy.center_x, enemy.center_y, item=enemy.drop_loot)
                enemy.remove_from_sprite_lists()
        
        # Check si le player ne peut pas pickup d'item
        self.pickup_item()

        # Mise à jour des données de sauvegarde 
        self.stuff_to_save = {
                            "player":{
                                "player_x":self.player.center_x,
                                "player_y": self.player.center_y
                                },
                            "inventory": self.inventory
                            }
        
        self.collect_enemy_bullets()
        self.enemy_list.update()
        self.enemy_list.update_animation(delta_time)

        # Regarde si le joueur touche une bullet 
        # for bullet in self.enemy_bullet_list:
        #     if arcade.check_for_collision_with_list(bullet, self.player_list):
        #         self.player.hp -= 1
        #         bullet.remove_from_sprite_lists()
        
        

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            save_file(self.stuff_to_save)
            self.window.show_view(InGameMenu(self))
        else:
            self.key_pressed.add(symbol)


    def on_key_release(self, symbol, modifiers):
        if symbol in self.key_pressed:
            self.key_pressed.remove(symbol)


    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            world_x = x + self.camera_x - (self.window.width // 2)
            if  world_x < self.player.center_x:
                self.attack_direction = -1 
            else:
                self.attack_direction = 1


# Fonction non présentes de base dans arcade
    def pan_camera_to_player(self, panning_fraction: float = 1.0):
        """Manage scrolling -- from Arcade docs"""
        self.camera.position = arcade.math.smerp_2d(
            self.camera.position,
            self.player.position,
            self.window.delta_time,
            panning_fraction)
        

    def create_enemy(self, number_of_enemy:int = 100):
        """Create (number_of_enemy) enemy and add them to the self.enemy_list"""
        enemy_classes = entity.Enemy.__subclasses__()
        for _ in range(number_of_enemy):
            placed = False
            while not placed:
                x = random.randint(0, MAP_WIDTH)
                y = random.randint(0, MAP_HEIGHT)
                enemy_class = random.choice(enemy_classes)
                enemy = enemy_class(x=x, y=y, player = self.player)
                if not arcade.check_for_collision_with_list(enemy, self.enemy_list):
                    placed = True
                    self.enemy_list.append(enemy)


    def add_to_inventory(self, item, number_of_item:int = 1) -> None:
        """Add the (item) to the self.inventory """
        if not item in self.inventory.keys():
            self.inventory[item] = 0
        self.inventory[item] += number_of_item
        print(self.inventory)


    def drop_item(self, x:int|float, y:int|float, item:str):
        """Create a item at the coordonates x,y and store it in the self.item_list"""
        item = entity.Item(x=x,
                      y=y,
                      name_or_precise_type = item)
        self.item_list.append(item)


    def pickup_item(self):
        """Add the items in collision with the player to the inventory"""
        for item in self.item_list:
            if arcade.check_for_collision_with_list(item, self.player_list):
                self.add_to_inventory(item.name_or_precise_type)
                item.remove_from_sprite_lists()


    def collect_enemy_bullets(self):
        """Collect the variables enemy.bullet_list from the differents enemies and put them in the self.enemy_bullet_list"""
        self.enemy_bullet_list.clear()
        for enemy in self.enemy_list:
            if enemy.bullet_list:
                self.enemy_bullet_list.extend(enemy.bullet_list) 