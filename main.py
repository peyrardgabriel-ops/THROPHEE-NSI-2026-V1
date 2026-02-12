import arcade
from LOGIC.logic import GameView

window = arcade.Window(1280, 720, "Jeu", fullscreen=True)
window.center_window()

game = GameView()
window.show_view(game)
arcade.run()


