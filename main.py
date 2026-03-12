import arcade
from LOGIC.menu.menu_intro.menu_intro import MenuIntro

arcade.enable_timings()



class Game(arcade.Window):
    def __init__(self):
        super().__init__(title="Jeu", fullscreen=True)
        self.center_window()
        self.show_view(MenuIntro(self))

    
    def switch_scene(self, view):
        self.show_view(view)

game = Game()
arcade.run()


