import math
from LOGIC.entity import Item

IMG_SWORD = "LOGIC/textures/item/sword/sword.png"

class Sword(Item):
    type = "sword"
    path_or_texture = IMG_SWORD

    def __init__(self, gameview, x, y, damage:int = 1):
        self.gameview = gameview
        
        
        super().__init__(x, y, path_or_texture= self.path_or_texture)
        self.center_x = x
        self.center_y = y
        self.damage = damage

        self.is_attacking = False
        self.already_attacked = set()
        self.attack_speed = 100
        

    def right_click(self):
        pass

    def left_click(self):
        self.is_attacking = True
        self.already_attacked.clear()
        self.attack_target_angle = - math.pi / 2
        

        
    def update_animation(self, delta_time=1/60):
        if  not self.is_attacking:
            # Direction de l'épée lorsque le joueur n'attaque pas
            if self.gameview.attack_direction == 1:
                self.angle = 2 * math.pi
            else:
                self.angle = math.pi 
            
        else:
            # Calcul de la position de l'épée
            pivot_x = self.gameview.player.center_x
            pivot_y = self.gameview.player.center_y

            self.center_x = pivot_x + math.cos(self.attack_target_angle) * 100
            self.center_y = pivot_y + math.sin(self.attack_target_angle) * 100



            dx = self.center_x - pivot_x
            dy = self.center_y - pivot_y

        # Rotation de l'épée
            if self.gameview.attack_direction == 1:
                self.attack_target_angle += math.pi / 30
                self.angle = 90 - math.degrees(math.atan2(dy, dx))
                if self.attack_target_angle >= math.pi / 2:
                    self.is_attacking = False
            else:
                self.attack_target_angle -= math.pi / 30
                self.angle = 90 - math.degrees(math.atan2(dy, dx))
                if self.attack_target_angle <= -(3 * math.pi) / 2:
                    self.is_attacking = False
        
         