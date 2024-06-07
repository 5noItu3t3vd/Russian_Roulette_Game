from config import *
from items import *

class Player:
    def __init__(self, name="nul"):
        self.name = name
        self.health = 3
        self.items = INITIAL_ITEMS_SELF
        self.revealed = False
            
    def heal(self):
        self.health += 1
        
    def reset(self):
        self.health = 3
        self.revealed = False   
        
    def take_damage(self,shotgun) -> bool:
        if self.health <= 0:
            raise ValueError("There is no damage to take")
        
        if shotgun.pick_round() == 1:
            self.health -= shotgun.get_damage()
            shotgun.reset_damage()
            if self.health < 0:
                self.health = 0
            return True
        
        shotgun.reset_damage()
        return False
        
    def is_dead(self) -> bool:
        return self.health <= 0
        
    def set_health(self, value):
        self.health = value
        
    def add_items(self, item):
        if item in self.items:
            self.items[item] += 1
        else:
            raise ValueError("Invalid item")

    def use_item(self, item_name, shotgun):
        if not self.item_usable(shotgun,item_name):
            raise AssertionError("This is not OK")
            
        self.items[item_name] -= 1
        item = self.create_item(item_name)
        result = item.apply_effect(self, shotgun)
        return result

    def create_item(self, item_name):
        if item_name == HEALING:
            return Kitbox()
        elif item_name == STRENGTH:
            return GunPower()
        elif item_name == REVEALER:
            return Revealer()
        else:
            raise ValueError("Invalid item")
        
    def create_gatcha_items(self, num):
        item_choices = [HEALING, STRENGTH, REVEALER]
        if not num: raise Exception("Cannot Be Possible")
        
        
        for _ in range(num):
            selected_item = random.choice(item_choices)
            self.add_items(selected_item)
            if len(self.items)>(2+num):
                break
            
    def reset_items(self):
        """Reset the player's inventory."""
        self.items = {
            HEALING: 0,
            STRENGTH: 0,
            REVEALER: 0
        }
        
    def has_item(self,item_name):
        return self.items[item_name] > 0
    
    def get_name(self):
        """Get the player's name."""
        return self.name
    
    def get_items(self):
        """Get the items in the player's inventory."""
        return self.items
    
    def get_health(self):
        """Get the player's current health."""
        return self.health
    
    def statusToString(self):
        return f"Player {self.name} has {self.health}"
    
    def itemToString(self):
        item_str_list = []
        if self.items[HEALING] > 0:
            item_str_list.append(f"{self.items[HEALING]} {HEALING}")
        if self.items[STRENGTH] > 0:
            item_str_list.append(f"{self.items[STRENGTH]} {STRENGTH}")
        if self.items[REVEALER] > 0:
            item_str_list.append(f"{self.items[REVEALER]} {REVEALER}")

        if not item_str_list:
            return "no items"

        return ", ".join(item_str_list)

    def toString(self):
        return f"Player: {self.name}, Health: {self.health}, Items: {self.itemToString()}"

    def item_usable(self,shotgun,item_name):
        canHeal,canStrength,canReveal = self.can_heal(),self.can_strength(shotgun),self.can_reveal(shotgun)
        
        if item_name==HEALING: return canHeal
        elif item_name==REVEALER:return canReveal
        elif item_name==STRENGTH: return canStrength
        raise AssertionError("What is this item?")        
        
        
    def can_heal(self):
        return self.items[HEALING] > 0 and self.health < 5
    def can_strength(self,shotgun):
        return self.items[STRENGTH] > 0 and shotgun.get_damage() < 2
    def can_reveal(self,shotgun):
        return self.items[REVEALER] > 0 and not self.revealed and not shotgun.get_revealed()
            