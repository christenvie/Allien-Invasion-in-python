# Author J'yrens Christenvie , Please acknowledge the author if you are using his code for your game
# People acknowledged : Eric Matthes 

# 28 / 05 / 2020
# This class stores all the stats about the game

import json

class GameStats:
    """Track stats for alien Invasion """

    def __init__(self,ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

        # Start Alien Invasion in an active 
        self.game_active = False

        # High score should never be reset.
        self.load_high_score()
            
    def reset_stats(self):
        """Initialize statistics that can change during the game """
        self.ships_left = self.settings.ship_limit
        self.score = 0 
        self.level = 1

    def load_high_score(self):
        """Load High score from a file and write it in a file """
        self.filename = 'high_score.json' 
        try :
            with open(self.filename) as f:
                self.high_score = json.load(f)
        except FileNotFoundError:
            self.high_score = 0
            with open(self.filename, 'w') as f:
                    json.dump(self.high_score, f)

    
    
        
        
