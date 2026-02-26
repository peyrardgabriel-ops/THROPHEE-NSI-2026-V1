import arcade
import math
import random

from LOGIC.Save.save import save_file, load_file
import LOGIC.entity as entity
from LOGIC.entity.item_cls import Sword, Gear_wheel
from LOGIC.inventory.inventory import Inventory

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
    def __init__(self, game = None, save_file = ""):
        self.game = game
        self.save_file = save_file
        self.map = map1

        super().__init__()
        arcade.set_background_color(arcade.color.LIGHT_BLUE)

        # Recupère les données stockées
        data = load_file(self.save_file)

        # Deplacement
        self.key_pressed = set()

        # Player
        self.player_list = arcade.SpriteList(use_spatial_hash=False)
        self.player = entity.Player(x= data["player"]["player_x"],
                             y= data["player"]["player_y"],
                             name_or_precise_type = "JP")
        self.attack_direction = 1
        self.player_list.append(self.player)

        if self.map.can_attack:
            self.sword_list = arcade.SpriteList(use_spatial_hash=False)
            sword = Sword(gameview=self,
                        x= self.player.center_x,
                        y = self.player.center_y,
                        damage=5)
            sword.scale = 2
            self.sword_list.append(sword)

        # Ennemis 
        self.current_number_enemy = 0
        self.enemy_list = arcade.SpriteList(use_spatial_hash=True)
        self.enemy_bullet_list = arcade.SpriteList(use_spatial_hash=True)
        self.number_max_enemy = 100
        
        
        

        # Items 
        self.item_list = arcade.SpriteList(use_spatial_hash=True)
        
        # Caméra
        self.camera = arcade.camera.Camera2D()
        self.camera_x, self.camera_y = self.camera.position
        

        # Débug Menu
        self.is_debug_menu_open = False
            

        # Inventaire
        self.inventory_cls = Inventory(save_file)
        self.inventory = self.inventory_cls.inventory
        if not self.inventory_cls.is_existing("sword"):
            self.inventory_cls.add_to_inventory("sword")

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

        if self.map.can_attack:    
            self.sword_list.draw()

        # Débug Menu 
        if self.is_debug_menu_open:
            arcade.draw_text(f"x: {self.player.center_x:.2f} y: {self.player.center_y:.2f} -- "
                            f"camera_x: {self.camera_x:.2f} camera_y: {self.camera_y:.2f} -- "
                            f"enemies: {len(self.enemy_list)} fps: {arcade.get_fps():.0f} -- "
                            f"hp: {self.player.hp}",
            self.camera_x - ((self.window.width - PLAYER_SIZE) // 2),
            self.camera_y + ((self.window.height - PLAYER_SIZE) // 2),
            arcade.color.WHITE,
            14)
            


    def on_update(self, delta_time):


        # Caméra
        self.pan_camera_to_player(CAMERA_PAN_SPEED)
        self.camera_x, self.camera_y = self.camera.position

        
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
        

        #                                           ---- Bullets ----

        
        for enemy in self.enemy_list:
            self.enemy_bullet_list.extend([b for b in enemy.bullet_list if b not in self.enemy_bullet_list])
        self.enemy_bullet_list.update()

        
        

        # Regarde si le joueur touche une bullet 
        for bullet in self.enemy_bullet_list:
            if arcade.check_for_collision_with_list(bullet, self.player_list):
                self.player.hp -= 1
                bullet.remove_from_sprite_lists()
                if self.player.hp <= 0:
                    self.open_gameover()

        
        
        

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            save_file(self.stuff_to_save, self.save_file)
            self.open_pause()
        elif symbol == arcade.key.E:
            save_file(self.stuff_to_save, self.save_file)
            self.open_inventory()
        elif symbol == arcade.key.F3:
            self.is_debug_menu_open = not self.is_debug_menu_open
        elif symbol == arcade.key.K:
            self.player.hp = 0
        else:
            self.key_pressed.add(symbol)


    def on_key_release(self, symbol, modifiers):
        if symbol in self.key_pressed:
            self.key_pressed.remove(symbol)


    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.map.can_attack:
                world_x = x + self.camera_x - (self.window.width // 2)
                if  world_x < self.player.center_x:
                    self.attack_direction = -1 
                else:
                    self.attack_direction = 1
                for sword in self.sword_list:
                    sword.left_click()

    def on_show_view(self):
        self.camera.position = self.player.position
        self.create_enemy(100)
        
    
    def on_fixed_update(self, delta_time):
        # Mise à jour régulière des animations
        self.enemy_list.update_animation(delta_time)
        self.enemy_list.update()

        if self.map.can_attack:
            self.sword_attack()
            self.sword_list.update_animation(delta_time)

        # Déplacements des ennemis
        self.enemy_movement(delta_time=delta_time)
        

        # Déplacements du joueur
        if arcade.key.Z in self.key_pressed:
            self.player.center_y += self.player.speed * delta_time
        if arcade.key.S in self.key_pressed:
            self.player.center_y -= self.player.speed * delta_time
        if arcade.key.D in self.key_pressed:
            self.player.center_x += self.player.speed * delta_time
        if arcade.key.Q in self.key_pressed:
            self.player.center_x -= self.player.speed * delta_time

        
            
        


# Fonction non présentes de base dans arcade
    def pan_camera_to_player(self, panning_fraction: float = 1.0):
        """Manage scrolling -- from Arcade docs"""
        self.camera.position = arcade.math.smerp_2d(
            self.camera.position,
            self.player.position,
            self.window.delta_time,
            panning_fraction)
        

    def create_enemy(self, number_of_enemy:int = 100, area_of_spawn:tuple = ((0,0), (MAP_WIDTH, MAP_HEIGHT))):
        """Create (number_of_enemy) enemy and add them to the self.enemy_list.
        do not put too many enemies in a limited space : the program could run endlessly"""

        if self.map.can_enemy_spawn:
            enemy_classes = entity.Enemy.__subclasses__()
            x_min, y_min = area_of_spawn[0]
            x_max, y_max = area_of_spawn[1]
            for _ in range(number_of_enemy):
                x = random.randint(x_min, x_max)
                y = random.randint(y_min, y_max)
                enemy_class = random.choice(enemy_classes)
                enemy = enemy_class(x=x, y=y, player = self.player)
                self.enemy_list.append(enemy)
                    


    

    # Items
    def get_item_class(self, name: str):
        for cls in entity.Item.__subclasses__():
            if cls.type == name:
                return cls
        return None


    def drop_item(self, x:int|float, y:int|float, item:str):
        """Create a item at the coordonates x,y and store it in the self.item_list"""
        item_class = self.get_item_class(item)
        if item_class == None:
            raise ValueError(f"Item inconnu : {item}")
        new_item = item_class(x=x, y=y)
        self.item_list.append(new_item)


    # Inventaire
    def pickup_item(self):
        """Add the items in collision with the player to the inventory"""
        for item in self.item_list:
            if arcade.check_for_collision_with_list(item, self.player_list):
                self.inventory_cls.add_to_inventory(item.type)
                item.remove_from_sprite_lists()



    # Differents menus
    def open_pause(self):
        from LOGIC.menu.menu_pause.menu_pause import MenuPause
        self.game.switch_scene(MenuPause(self.game))

    def open_inventory(self):
        from LOGIC.menu.menu_inventory.menu_inventaire import InventoryMenu
        inventory_menu = InventoryMenu(self.game,
                                        file=self.save_file)
        self.game.switch_scene(inventory_menu)

    def open_gameover(self):
        from LOGIC.menu.menu_gameover.menu_gameover import MenuGameover
        self.game.switch_scene(MenuGameover(game=self.game, file=self.save_file))


    def enemy_movement(self, delta_time:float) -> None:
        """Define the 3 modes of the enemy 

                - if the enemy can attack, it will
                - if the enemy can't attack but can detect the player, it will follow him
                - if the enemy can't detect the enemy, it will follow a random movement"""
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

            # si l'ennemi ne detecte pas le joueur, mouvement de base du ennemi
            elif math.dist((enemy.center_x, enemy.center_y), (self.player.center_x, self.player.center_y)) < 1500:
                enemy.movement()

            # si l'ennemi est vrm trop loin, il ne se déplace pas
            else:
                pass
            
            # Gestion des bordures de la map
            if enemy.left < 0:
                enemy.left = 0
            elif enemy.right > MAP_WIDTH:
                enemy.right = MAP_WIDTH

            if enemy.bottom < 0:
                enemy.bottom = 0
            elif enemy.top > MAP_HEIGHT:
                enemy.top = MAP_HEIGHT
    
    def sword_attack(self) -> None:
        if self.map.can_attack:
            for sword in self.sword_list:
                if not sword.is_attacking:
                    if self.attack_direction == 1:
                        sword.center_x = self.player.center_x + 40
                        sword.scale_x = 1
                    else:
                        sword.center_x = self.player.center_x - 40
                        sword.scale_x = -1
                    sword.center_y = self.player.center_y

                # Regarde les collsions entre l'épée et les ennemis et auquel cas leur enlève 1 hp
                if sword.is_attacking:
                    for enemy in arcade.check_for_collision_with_list(sword, self.enemy_list):
                        if enemy in self.enemy_list:
                            if not enemy in sword.already_attacked:
                                enemy.hp -= sword.damage
                                sword.already_attacked.add(enemy)
                                if enemy.hp <= 0:
                                    self.drop_item(x = enemy.center_x,
                                                y = enemy.center_y,
                                                item= enemy.drop_loot)
                                    enemy.remove_from_sprite_lists()

class Map:
    def __init__(self,
                 can_attack: bool = True,
                 can_enemy_spawn: bool = True):
        self.can_attack = can_attack
        self.can_enemy_spawn = can_enemy_spawn

map1 = Map(True, True)
map2 = Map(False, False)
map3 = Map(...,...)          # <= A MODIFIER !!!!!!