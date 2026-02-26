from LOGIC.Save.save import load_file

class Inventory():
    def __init__(self,file, capacity = 10):
        data = load_file(file)
        if data["inventory"]:
            self.inventory = data["inventory"]
        else:
            self.inventory = []
        self.capacity = capacity

        self.item_in_use = None


    def add_to_inventory(self, obj, number_of_item: int = 1):
        """Add (number_of_time) times the (obj) in the inventory"""
        for i, (name, quantity) in enumerate(self.inventory):
            if name == obj:
                self.inventory[i] = (name, quantity + number_of_item)
                return
            
        if len(self.inventory) < self.capacity:
            self.inventory.append((obj, number_of_item))

    
    def remove_from_inventory(self, obj, number_of_item:int = 1):
        if number_of_item == 0:
            return
        for i, (name, quantity) in enumerate(self.inventory):
            if name == obj:
                self.inventory[i] = (name, quantity - number_of_item)
                if self.inventory[i][1] < 0:
                    raise ValueError(f"You tried removing more than the initial quantity of this item")
                elif self.inventory[i][1] == 0:
                    del self.inventory[i]
                return
        raise ValueError(f"You can't remove an item that doesn't exist")
    
    def is_existing(self, item):
        for tpl in self.inventory:
            if tpl[0] == item:
                return True
        return False
    




