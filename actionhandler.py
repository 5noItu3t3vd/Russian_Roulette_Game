from config import *

class ActionHandler:
    def __init__(self, game_gui, player, opponent):
        self.game_gui = game_gui
        self.player = player
        self.opponent = opponent

    def handle_revealer(self, current_player, callback):
        current_player.use_item(REVEALER, self.game_gui.shotgun)
        dialogue = [f"{current_player.get_name()} uses {REVEALER}!"]
        self.game_gui.talk_sequence(dialogue, lambda: self.handle_revealer_step2(current_player, callback))

    def handle_revealer_step2(self, current_player, callback):
        dialogue = [f"{current_player.get_name()}: Forsees a vision!"]
        self.game_gui.talk_sequence(dialogue, callback)
        play_mp3(REVEAL_SOUND)

    def handle_healing(self, current_player, callback):
        dialogue = [f"{current_player.get_name()} uses {HEALING}!"]
        self.game_gui.talk_sequence(dialogue, lambda: self.handle_healing_step2(current_player, callback))

    def handle_healing_step2(self, current_player, callback):
        current_player.use_item(HEALING, self.game_gui.shotgun)
        dialogue = [f"{current_player.get_name()} healed 1 Heart"]
        self.game_gui.talk_sequence(dialogue, callback)
        play_mp3(HEAL_SOUND)

    def handle_strength(self, current_player, callback):
        dialogue = [f"{current_player.get_name()} uses {STRENGTH}!"]
        self.game_gui.talk_sequence(dialogue, lambda: self.handle_strength_step2(current_player, callback))    
        
    def handle_strength_step2(self, current_player, callback):
        current_player.use_item(STRENGTH, self.game_gui.shotgun)
        dialogue = [f"{current_player.get_name()}: powered the gun for the next bullet to deal 2 damages"]
        self.game_gui.talk_sequence(dialogue, callback)
        play_mp3(POWER_UP_SOUND)

    def handle_opp(self, current_player, callback):
        dialogue = [f"{current_player.get_name()} aims the gun at you!"]
        self.game_gui.talk_sequence(dialogue, callback)

    def handle_self(self, current_player, callback):
        dialogue = [f"{current_player.get_name()} aims the gun to their head!"]
        self.game_gui.talk_sequence(dialogue, callback)

