import arcade
from GAME.menu.menu_intro.menu_intro import MenuIntro


arcade.enable_timings()

class Game:
    def __init__(self):
        window.show_view(MenuIntro(self))

    def switch_scene(self, new_scene):
        window.show_view(new_scene)

window = arcade.Window(fullscreen=True, vsync=True)
window.center_window()

game = Game()
arcade.run()


