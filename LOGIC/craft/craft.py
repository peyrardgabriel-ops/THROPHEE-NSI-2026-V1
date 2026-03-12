import json

from LOGIC.inventory.inventory import Inventory

# Les recettes sont de la forme [ingrédient, quantité_produite]
PATH_TO_RECIPE = "LOGIC/craft/recipes.json"

class Craft:
    def __init__(self, file, gameview):
        self.recipes = self.load_recipes()
        self.inventory_cls = Inventory(file)


    def load_recipes(self):
        """Load the file of the recipes and return its content"""
        with open(PATH_TO_RECIPE, "r") as recipes_file:
            recipes = json.load(recipes_file)
        return recipes
    

    def list_can_craft(self) -> list:
        """return the list of the recipes that the player can craft with its 
        current inventory"""
        recipes_craftable = []
        for name, ingredient in self.recipes.items():
            can_make = True
            for element, quantity in ingredient[0].items():
                if not self.inventory_cls.get_quantity(element) >= quantity:
                    can_make = False
                    break
            if can_make:
                recipes_craftable.append(name)
        return recipes_craftable
    
    
    def can_craft_item(self, item) -> bool:
        return item in self.list_can_craft()


    def craft(self, item_to_craft):
        """craft the item choosen, add it to the inventory and remove the ingredients """
        if not self.can_craft_item(item_to_craft):
            raise ValueError(f"You can't craft the item{item_to_craft}")
            

        ingredients = self.recipes[item_to_craft][0]

        for item, quantity in ingredients.items():
            self.inventory_cls.remove_from_inventory(item, quantity)
        self.inventory_cls.add_to_inventory(item_to_craft, self.recipes[item_to_craft][1])

        self.inventory_cls.save_inventory(self.inventory_cls.file)