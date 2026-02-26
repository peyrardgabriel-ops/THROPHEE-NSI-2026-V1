import math
import random
import arcade


from LOGIC.entity.enemy import Enemy
from LOGIC.textures.load_sheet import load_sheet
from LOGIC.entity.entity import Entity

MAP_WIDTH = 5000
MAP_HEIGHT = 5000

TEXTURES = {"idle": "LOGIC/textures/enemy/robot/Robot_Idle.png",
                    "run": "LOGIC/textures/enemy/robot/Robot_run.png",
                    "shoot": "LOGIC/textures/enemy/robot/Robot_Shoot.png",
                    "bullet": "LOGIC/textures/enemy/robot/Bullet.png"}
        
idle_textures = load_sheet(TEXTURES["idle"], 6)
run_textures = load_sheet(TEXTURES["run"], 4)
shoot_textures = load_sheet(TEXTURES["shoot"], 8)
bullet_textures = load_sheet(TEXTURES["bullet"], 1)

class Robot(Enemy):
    ROBOT_SPEED = 200
    ROBOT_HP = 5
    

    BULLET_SPEED = 100

    def __init__(self, x:int|float, y:int|float, player,
                name_or_precise_type=None, path_or_texture = None):
        self.detection_range = 500
        self.attack_range = 200
        self.speed = self.ROBOT_SPEED
        self.hp = self.ROBOT_HP
        self.drop_loot = "gear wheel"
        self.player = player
        self.bullet_list = arcade.SpriteList()


        if random.random() < 0.01:
            self.drop_loot = "printed circuit"

        # Textures
        

        

        self.time_counter = 0
        self.frame_index = 0
        self.state = "IDLE"
        self.target_timer = 0

        super().__init__(x, y,
                        detection_range= self.detection_range,
                        name_or_precise_type=name_or_precise_type,
                        path_or_texture=idle_textures[0],
                        speed = self.speed,
                        hp= self.hp)

        if idle_textures:
            self.texture = idle_textures[0]

        

    def update_animation(self, delta_time=1/60):
        if self.state == "ATTACK":
            frames = shoot_textures
            speed = 0.10
        elif self.state == "RUN":
            frames = run_textures
            speed = 0.12
        else:
            frames = idle_textures
            speed = 0.18

        if not frames: return

        self.time_counter += delta_time
        if self.time_counter >= speed:
            self.time_counter = 0
            self.frame_index = (self.frame_index + 1) % len(frames)
            self.texture = frames[self.frame_index]

            if self.state == "ATTACK" and self.frame_index == 4:
                self.fire_bullet(self.player)

        if self.change_x < 0:
            self.scale_x = -1
        elif self.change_x > 0:
            self.scale_x = 1


    def fire_bullet(self, other, delta_time = 1/60):
        """Fire a bullet in the direction of the player to attack it"""
        bullet = Entity(x = self.center_x,
                        y = self.center_y,
                        path_or_texture=bullet_textures[0],
                        hp=7)
                        
        direction =math.atan2((other.center_y - self.center_y),
                            (other.center_x - self.center_x))
        bullet.change_x = math.cos(direction) * self.BULLET_SPEED * delta_time
        bullet.change_y = math.sin(direction) * self.BULLET_SPEED * delta_time
        self.bullet_list.append(bullet)


    def update(self, delta_time = 1 / 60):
        self.update_animation(delta_time)
        for bullet in self.bullet_list:
            bullet.hp -= delta_time
            if bullet.hp <= 0:
                bullet.remove_from_sprite_lists()

    
    def movement(self, delta_time = 1 / 60):
        """Move the robot in a random pattern if it's not attacking"""
        if self.state != "ATTACK":
            if self.target_timer <= 0:
                if random.random() < 0.4: 
                    self.state = "IDLE"
                    self.change_x = 0
                    self.change_y = 0
                    self.target_timer = random.uniform(1.5, 3.0)
                else:
                    self.state = "RUN"
                    angle = random.uniform(0, 2 * math.pi)
                    self.change_x = math.cos(angle) * self.speed * delta_time
                    self.change_y = math.sin(angle) * self.speed * delta_time
                    self.target_timer = random.uniform(2.0, 5.0)

            self.target_timer -= delta_time
        
        # Application du mouvement
        self.center_x += self.change_x 
        self.center_y += self.change_y    

    def get_bullet(self):
        return self.bullet_list   