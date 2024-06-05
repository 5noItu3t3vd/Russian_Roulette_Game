from config import *

class Item:
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect

    def apply_effect(self, player, shotgun):
        """Apply the effect of the item to the player."""
        if self.name == HEALING:
            player.heal()
        elif self.name == STRENGTH:
            shotgun.double_damage()
        elif self.name == REVEALER:
            return shotgun.reveal_next_shot() == 1

class Kitbox(Item):
    def __init__(self):
        super().__init__(HEALING, "heals the player by 1 heart")

class GunPower(Item):
    def __init__(self):
        super().__init__(STRENGTH, "increases the next shotgun strength to take 2 hearts")

class Revealer(Item):
    def __init__(self):
        super().__init__(REVEALER, "reveals the next shot of the gun")
