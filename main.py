import arcade
from LOGIC2.Player_v2_avec_arcade import GameView

window = arcade.Window(1280, 720, "Jeu", fullscreen=True)
window.center_window()

game = GameView()
window.show_view(game)
arcade.run()
