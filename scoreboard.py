# Author J'yrens Christenvie , Please acknowledge the author if you are using his code for your game
# People acknowledged : Eric Matthes 

# 29 / 05 / 2020
# This class displays the scoreboard on the screen

import pygame.font
from pygame.sprite import Group 

from ship import Ship


class Scoreboard: 
    """A class to report scoring information."""

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen 
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings 
        self.stats = ai_game.stats 

        # Font settings for scoring information.        
        self.text_color = (253, 209, 0)
        self.my_score_color = (253, 209, 0)
        self.font = pygame.font.SysFont("DS-Digital", 36)
        self.level_font = pygame.font.SysFont("DS-Digital", 18)

        # Prepare the initial score image.        
        self.prep_images()
        
    def prep_score(self):
        """Turn the score into a rendered image. """

        # round the value of the score to the nearest 10 , 100 , 1000
        rounded_score = round(self.stats.score , -1)
        score_str = "Score " +"{:,}".format(rounded_score) 
        self.score_image = self.font.render(score_str,True , 
                self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen.   
        self.score_rect = self.score_image.get_rect()   
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "High Score " +"{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, 
                self.text_color, self.settings.bg_color)
        
        # Center the high score at the top of the screen.     
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Turn the level in to a rendered image."""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str,True,
                self.text_color, self.settings.bg_color)

        # Position the level below the score .    
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 30

    def prep_the_level(self):
        """Turn the level in to a rendered image."""
        the_level_str = "Level"
        self.the_level_image = self.level_font.render(the_level_str,True,
                self.my_score_color, self.settings.bg_color)

        # Position the level below the score .    
        self.the_level_rect = self.the_level_image.get_rect()
        self.the_level_rect.right = self.screen_rect.right - 10
        self.the_level_rect.top = self.score_rect.bottom + 10

    def show_score(self):
        """Draw score to the screen , levels and ships to the screen"""
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        
       
        self.screen.blit(self.level_image,self.level_rect)
        self.screen.blit(self.the_level_image,self.the_level_rect)

        self.ships.draw(self.screen)

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships =Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_images(self):
        """Prep the scoreboard  """
        self.prep_score()
        
        self.prep_high_score()
        
        self.prep_level()
        self.prep_the_level()

        self.prep_ships()

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score 
            self.prep_high_score()


