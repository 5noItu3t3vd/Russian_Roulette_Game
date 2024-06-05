from config import *

class Shotgun:
    def __init__(self):
        """Initialize a Shotgun instance with default damage and rounds."""
        self.damage = 1
        self.rounds = []
        self.next_shot = None
        self.revealed = False
        self.isExhausted = True

    def double_damage(self):
        """Double the damage of the shotgun."""
        self.damage = 2

    def reset_damage(self):
        """Reset the damage to its default value."""
        self.damage = 1
    
    def get_revealed(self):
        """Check if the next shot has been revealed."""
        return self.revealed

    def get_rounds(self):
        """Get the list of remaining rounds."""
        return self.rounds
    
    def is_exhausted(self):
        """Check if the shotgun is out of rounds."""
        return self.isExhausted
    
    def get_damage(self):
        """Get the current damage value of the shotgun."""
        return self.damage
    def get_next_shot(self):
        """Get the next shot without removing it from the rounds."""
        if self.rounds:
            print(f"The next shot is:(In class shotgun) {self.rounds[0]}")
            return self.rounds[0]
        return None
    
    def add_rounds(self, turn=1):
        
        if turn < 0: turn = 1

        self.rounds = []
        self.reset_damage()
        
        max_bullets_per_turn = {
            1: 3,
            2: 5,
            3: 7
        }
        
        max_bullets = max_bullets_per_turn.get(turn, 7)  # Default to 7 bullets if turn is greater than 3
        
        live_options = {
            1: [1, 2],
            2: [1, 2, 3],
            3: [2, 3]
        }
        
        live = random.choice(live_options.get(turn))
        blank = max_bullets - live
        
        self.rounds.extend([1] * live)
        self.rounds.extend([0] * blank)
        
        
        random.shuffle(self.rounds)
        self.isExhausted = False

    def pick_round(self):
        """Pick a round from the shotgun.

        Return:
            bool: True if a live round, False if a blank round, None if no rounds left.
        """
        try:
            if not self.rounds:
                raise Exception("shouldnt happen too")
            
            self.next_shot = self.rounds.pop(0)
            self.revealed = False
            self.isExhausted = False if 1 in self.get_rounds() else True
            return self.next_shot
        
        except IndexError as e:
            print(f"Error picking round: {e}")
            self.next_shot = None
            return None
    
    def reveal_next_shot(self):
        """Reveal the next shot without removing it from the rounds.

        Returns:
            bool: The next shot (True for live, False for blank), None if no rounds are left.
        """
        if self.rounds:
            self.revealed = True
            return self.rounds[0]
        return None
    
    