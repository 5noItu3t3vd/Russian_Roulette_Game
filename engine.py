from Characters.Player import Player
from Characters.Computer import Computer
from Characters.Shotgun import Shotgun
from config import *

class Engine:
    def __init__(self, player, opponent=Computer(), gamemode="single"):
        """Initialize the game engine with players, shotgun, and game mode.

        Args:
            player (Player): The first player.
            opponent (Player): The second player, defaulting to a Computer.
            gamemode (str): The game mode, defaulting to "single".
        """
        self.gamemode = gamemode
        self.player = player
        self.opponent = opponent
        self.shotgun = Shotgun()
        self.shot_counts = None
        self.current_player = self.player
        self.other_player = self.opponent
        self.turn = 0
        
        self.isExhausted = True
        self.next_shot = None

    def reload_all_bullets(self):
        """Reload all bullets if the shotgun is exhausted."""
        if self.shotgun.is_exhausted():
            play_mp3(RELOAD_SOUND)
            self.shotgun.add_rounds(self.turn)
            self.isExhausted = False
            print("HELLLLLLOOO")
        
        self.shot_counts = self.shotgun.get_rounds()
        self.next_shot = self.shotgun.get_next_shot()
        print(f"Turns: {self.turn}")

    def add_turn(self):
        """Increment the turn and reload bullets."""
        self.turn += 1
        self.reload_all_bullets()

    def start_round(self):
        """Start a new round, reloading bullets and choosing players."""
        self.add_turn()
        self.reload_all_bullets()
        
        self.current_player = random.choice([self.opponent,self.player])
        self.other_player = self.opponent if self.current_player == self.player else self.player
        
        self.current_player.create_gatcha_items(self.turn)
        self.other_player.create_gatcha_items(self.turn)
        self.next_shot = self.shotgun.get_next_shot()  # Get the actual next shot
        assert(self.next_shot == self.shotgun.rounds[0])  # Check against the first round in the list
        return self.next_shot
    
    def reset_all(self):
        """Reset all game elements to their initial states."""
        self.player.reset()
        self.opponent.reset()
        self.shotgun.reset_damage()
        self.status_text()

    def role_switch(self):
        """Switch the roles of the current and other players."""
        if self.current_player == self.player:
            self.current_player = self.opponent
            self.other_player = self.player
        else:
            self.current_player = self.player
            self.other_player = self.opponent

    def status_text(self):
        """Print the status of the players and the shotgun."""
        print(f"Player {self.player.name}:\n  LIFE: {self.player.health}\n  ITEMS: {self.player.items}")
        print(f"Player {self.opponent.name}:\n  LIFE: {self.opponent.health}\n  ITEMS: {self.opponent.items}")            
        print(f"\nShotgun Status: \n   ROUNDS:{self.shotgun.get_rounds()}\n   DAMAGE: {self.shotgun.get_damage()}\n   NextShot{self.shotgun.next_shot}")
        print(f"Current Player: {self.get_current_player().name}")
    
    def choose_turn(self):
        """Randomly choose which player starts the turn.

        Returns:
            tuple: The current player and the other player.
        """
        choice = random.choice(["heads", "tails"])
        if choice == "heads":
            return self.player, self.opponent
        else:    
            return self.opponent, self.player
    
    def get_player(self):
        """Get the first player.

        Returns:
            Player: The first player.
        """
        return self.player
    
    def get_opponent(self):
        """Get the second player.

        Returns:
            Player: The second player.
        """
        return self.opponent
    
    def get_shotgun(self):
        """Get the shotgun instance.

        Returns:
            Shotgun: The shotgun instance.
        """
        return self.shotgun
        
    def get_current_player(self):
        """Get the current player.

        Returns:
            Player: The current player.
        """
        assert(self.other_player != self.current_player)
        return self.current_player
    
    def get_other_player(self):
        """Get the other player.

        Returns:
            Player: The other player.
        """
        assert(self.other_player != self.current_player)
        return self.other_player
    
    def get_shotcounts(self):
        """For getting the shot list before picking rounds (Because it pops the list)"""

        return self.shotgun.get_rounds()