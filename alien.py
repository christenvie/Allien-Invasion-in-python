# Author J'yrens Christenvie , Please acknowledge the author if you are using his code for your game
# People acknowledged : Eric Matthes 


# 15 / 05 / 2020
# This class controls the Alien that will be placed on the screen


import pygame

from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single Alien in a fleet """

    def __init__(self,ai_game):
        """Initialize the alien and sets its starting position """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set its rect attribute 
        self.image = pygame.image.load('images/first_alien.bmp')
        self.rect = self.image.get_rect()

        # start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the Alien exact horizontal position
        self.x = float(self.rect.x)
    
    def check_edges(self):
        """Return true if an alien is at the edge of the screen. """
        screen_rect = self.screen.get_rect()

        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Move an alien to the right or left """
        self.x += (self.settings.alien_speed * 
                        self.settings.fleet_direction)
        self.rect.x = self.x 


        

