
# Author J'yrens Christenvie , Please acknowledge the author if you are using his code for your game
# People acknowledged : Eric Matthes 

# 08 / 05 / 2020
# This program all the settings for the game

class Settings:
    """A class to store all the settings for alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings settings."""
        # screen settings
        self.screen_width = 1500
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # ship settings 
      
        self.ship_limit = 3

        # Bullet settings
        
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)
        self.bullets_allowed = 5

        #Alien settings
        
        self.fleet_drop_speed = 10
        
        # How quickly the game speeds up 
        self.speedup_scale = 1.1

        # How quickly the alien point values increase 
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed= 3.0
        self.alien_speed = 0.5

        # fleet direction of 1 represents right ; -1 represents left 
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings an alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *=self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        

        
        
        

