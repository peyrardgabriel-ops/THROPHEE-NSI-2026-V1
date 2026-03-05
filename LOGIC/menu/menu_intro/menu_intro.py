import arcade

class MenuIntro(arcade.View):
    def __init__(self, game):
        self.game = game
        super().__init__()
        self.background_color = arcade.color.DARK_GREEN

        self.time = 0
        self.alpha = 255

        self.text1 = arcade.Text("THE GAME", x= self.window.center_x - 100,
                                            y = self.window.center_y,
                                            color=arcade.color.BLACK,
                                            font_size=40)
        self.text2 = arcade.Text("MADE WITH ARCADE", x= self.window.center_x - 200,
                                            y = self.window.center_y,
                                            color=arcade.color.BLACK,
                                            font_size=40)
        

    def on_update(self, delta_time):
        self.time += 2

        
        #text1 est affiché
        if self.alpha > 0 and self.time < 250:
            self.alpha = max(self.alpha - 1, 0)
        elif self.time >= 350 and self.time < 600:
            self.alpha = min(self.alpha +1, 255)

        # text2 est affiché
        elif self.time >= 700 and self.time < 950:
            self.alpha = max(self.alpha - 1, 0)
        elif self.time >= 1050 and self.time < 1300:
            self.alpha = min(self.alpha +1, 255)

        
        if self.time >= 1400:
            self.open_start()
        
        



    def on_draw(self):
        self.clear()
        arcade.draw_lrbt_rectangle_filled(0, self.window.width, 0, self.window.height,
        (0, 0, 0, self.alpha))
        if self.time <= 700:
            self.text1.draw()
        elif self.time < 1400 and self.time > 700:
            self.text2.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.open_start()


    def open_start(self):
        from LOGIC.menu.menu_start.menu_start import MenuStart
        self.game.switch_scene(MenuStart(self.game))
        
