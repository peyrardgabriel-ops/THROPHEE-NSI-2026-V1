import arcade
from GAME.menu.button_sprite import ButtonSprite
from GAME.craft.craft import Craft
from GAME.entity.item import Item 

class MenuCraft(arcade.View):
    def __init__(self, game, file, gameview):
        super().__init__()
        self.game = game
        self.file = file
        self.gameview = gameview

        self.craft = Craft(file, gameview)
        
        
        self.button_list = arcade.SpriteList()
        self.preview_list = arcade.SpriteList()
        
    
        self.button_width = 300
        self.button_height = 60
        
        
        self.preview_sprite = arcade.Sprite()
        self.preview_text = arcade.Text("", x=0, y=0, color=arcade.color.BLACK, font_size=18, bold=True)
        self.ingredient_labels = [] 
        self.show_preview = False

        self.no_craft_text = arcade.Text(text="You can't craft anything ;(",
                                         x=300,
                                         y=self.window.height // 2,
                                         color=arcade.color.AO,
                                         font_size=60,
                                         bold=True)

        self.refresh_buttons()

        # Caméra
        self.camera = arcade.camera.Camera2D()
        self.camera.position = self.window.center_x, self.window.center_y

    def get_item_class(self, name: str):
        for cls in Item.__subclasses__():
            if cls.type == name:
                return cls
        return None

    def on_draw(self):
        self.camera.use()
        self.clear()

        if len(self.craft.list_can_craft()) == 0:
            self.no_craft_text.draw()
        
        # Boutons
        self.button_list.draw()
        for btn in self.button_list:
            btn.label.draw()
        
        # Preview
        if self.show_preview:
            self.preview_list.draw()
            self.preview_text.draw()
            for label in self.ingredient_labels:
                label.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        self.show_preview = False
        self.ingredient_labels.clear()
        self.preview_list.clear() 
        
        for btn in self.button_list:
            if (btn.center_x - btn.width / 2 <= x <= btn.center_x + btn.width / 2 and 
                btn.center_y - btn.height / 2 <= y <= btn.center_y + btn.height / 2):
                
                btn.width = btn.base_width + 10
                btn.height = btn.base_height + 10
                
                item_name = btn.text
                item_class = self.get_item_class(item_name)
                
                if item_class and item_name in self.craft.recipes:
                    recipe_data = self.craft.recipes[item_name]
                    
                    # Textures
                    tex_input = item_class.path_or_texture
                    try:
                        if isinstance(tex_input, list):
                            self.preview_sprite.texture = tex_input[0]
                        elif isinstance(tex_input, str):
                            self.preview_sprite.texture = arcade.load_texture(tex_input)
                        else:
                            self.preview_sprite.texture = tex_input
                    except Exception as e:
                        print(f"Erreur texture : {e}")
                    
                    self.preview_sprite.center_x = btn.center_x + self.button_width / 2 + 100
                    self.preview_sprite.center_y = btn.center_y
                    self.preview_sprite.scale = 1.0
                    self.preview_list.append(self.preview_sprite)
                    
                    self.preview_text.text = f"x{recipe_data[1]}"
                    self.preview_text.x = self.preview_sprite.center_x - 120
                    self.preview_text.y = self.preview_sprite.center_y 
                    
                    # Ingrédients
                    start_y = btn.center_y - 50
                    for ing_name, count in recipe_data[0].items():
                        color = arcade.color.BLACK
                        label = arcade.Text(f"- {ing_name}: {count}", 
                                            x=btn.center_x - self.button_width / 2 - 100,
                                            y=start_y + 50, color=color, font_size=12, bold=True)
                        self.ingredient_labels.append(label)
                        start_y -= 25
                    
                    self.show_preview = True
                    break 
            else:
                btn.width = self.button_width
                btn.height = self.button_height

    def on_mouse_press(self, x, y, button, modifiers):
        for btn in self.button_list:
            if (btn.center_x - btn.width / 2 <= x <= btn.center_x + btn.width / 2 and
                btn.center_y - btn.height / 2 <= y <= btn.center_y + btn.height / 2):
                
                if self.craft.can_craft_item(btn.text):
                    self.craft.craft(btn.text)
                    self.refresh_buttons()
                return

    def on_key_press(self, symbol, modifiers):
        """Retour au jeu avec Echap ou C"""
        if symbol == arcade.key.ESCAPE or symbol == arcade.key.C:
            self.load_game()

    def refresh_buttons(self):
        self.button_list.clear()
        self.names = self.craft.list_can_craft()
        y_start = self.window.height - 275
        for i, name in enumerate(self.names):
            y = y_start - i * (self.button_height + 20)
            btn = ButtonSprite(center_x=self.window.width // 2, 
                                center_y=y,
                                width=self.button_width, 
                                height=self.button_height,
                                color=(255, 255, 255, 200), 
                                text=name)
            self.button_list.append(btn)
        

    def load_game(self):
        self.game.switch_scene(self.gameview)