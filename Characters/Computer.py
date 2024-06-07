from .Player import Player
from config import *

class Computer(Player):
    def __init__(self, name="bogot"):
        super().__init__(name)
        self.name
        self.health = 3
        self.items = INITIAL_ITEMS_COMP
        self.revealed = False
        
    def get_action(self, shotgun, sight="Nothing"):

        self.revealed = shotgun.get_revealed()
        buckshots = shotgun.get_rounds()
        if not buckshots:
            raise AssertionError("Why would this happen")
        
        true_count = sum(buckshots)
        false_count = len(buckshots) - true_count
        
        # Check if Revealer should be used
        if self.items[REVEALER] > 0 and not self.revealed:
            revealed_shot = shotgun.reveal_next_shot()
            self.revealed = True
            if revealed_shot is not None:
                if revealed_shot:
                    return LIVE
                else:
                    return BLANK
        
        # Check if Healing should be used
        if self.items[HEALING] > 0 and self.health < 4:
            return HEALING
        
        # Check if Strength should be used
        if self.items[STRENGTH] > 0 and shotgun.get_damage() != 2:
            if sight == True:
                return STRENGTH
            elif sight==UNKNOWN:
                if true_count >= false_count:
                    return STRENGTH
        
        if sight == False:
            self.revealed = False
            return SELF
        
        # Default attack action
        attack_action = OPP if true_count >= false_count else SELF
        self.revealed = False
        return attack_action
    
    def use_item(self, item_name, shotgun):
        """Use an item and apply its effect to the computer player.

        Args:
            item_name (str): The name of the item to use.
            shotgun (Shotgun): The shotgun instance to apply the effect.

        Returns:
            Item: The used item instance.
        """
        if self.items[item_name] < 1:
            raise ValueError("Cannot find this item")
        
        self.items[item_name] -= 1
        item = self.create_item(item_name)
        item.apply_effect(self, shotgun)
        
        print(f"Computer used {item_name}")
        return item
    