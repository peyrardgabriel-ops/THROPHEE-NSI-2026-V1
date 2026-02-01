import arcade

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "j'ai vrm pas d'idée"




fenetre = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
fenetre.center_window()

class GameView(arcade.View):
    def __init__(self) -> None:
        super().__init__()
        #background
        self.background = arcade.Sprite(":resources:/images/backgrounds/abstract_1.jpg")
        self.background.center_x = SCREEN_WIDTH // 2
        self.background.center_y = SCREEN_HEIGHT // 2
        self.background.width = SCREEN_WIDTH
        self.background.height = SCREEN_HEIGHT

        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.speed = 500
        self.direction = {
            "right":False,
            "left":False,
            "up":False,
            "down":False
        }

    def on_draw(self) -> None:
        self.clear()

        #background 
        arcade.draw_sprite(self.background)

        arcade.draw_circle_filled(center_x=self.x, center_y=self.y, radius=30,color=arcade.color.AO)

        #test
        arcade.draw_text(text=f"x = {self.x:.2f} -- y = {self.y:.2f}", x = 10, y= SCREEN_HEIGHT-10, color=arcade.color.WHITE)

        

    def on_update(self, delta_time) -> None:

        #partie mouvement 
        if self.direction["right"]:
            self.x += self.speed * delta_time
        if self.direction["left"]:
            self.x -= self.speed * delta_time
        if self.direction["up"]:
            self.y += self.speed * delta_time
        if self.direction["down"]:
            self.y -= self.speed * delta_time

    def on_key_press(self, symbol:int, modifiers:int) -> None:

        #mouvement
        if symbol == arcade.key.D:
            self.direction["right"] = True
        if symbol == arcade.key.Q:
            self.direction["left"] = True
        if symbol == arcade.key.Z:
            self.direction["up"] = True
        if symbol == arcade.key.S:
            self.direction["down"] = True
    
    def on_key_release(self, symbol:int, modifiers:int) -> None:
        
        #mouvement
        if symbol == arcade.key.D:
            self.direction["right"] = False
        if symbol == arcade.key.Q:
            self.direction["left"] = False
        if symbol == arcade.key.Z:
            self.direction["up"] = False
        if symbol == arcade.key.S:
            self.direction["down"] = False


game = GameView()
fenetre.show_view(game)
arcade.run()
