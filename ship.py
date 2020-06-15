# Author J'yrens Christenvie , Please acknowledge the author if you are using his code for your game
# People acknowledged : Eric Matthes 

# 08 / 05 /2020
# This class manages the ship

import pygame
from pygame.sprite import Sprite



class Ship(Sprite):
    """ A class to manage the ship """ 

    def __init__(self,ai_game):
        """Initialize the ship and sets starting position """
        super().__init__()
        # take the screen settings and its rectangle 
        self.screen = ai_game.screen 
        self.settings = ai_game.settings 
        self.screen_rect = ai_game.screen.get_rect()

        # load the ship image  and get its rect.
        self.image = pygame.image.load('images/ship4.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        #store a decimal value of the ship horizontal position
        self.x = float(self.rect.x)

        #Movement flag 
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        """Update the ship's position based on the movement flag. """
        # update the ship x's value not the rect 
        if self.moving_right and self.rect.right < self.screen_rect.right :
            self.x += self.settings.ship_speed 
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        
        #Update rect object from self.x.
        self.rect.x = self.x 

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        """Center the ship on the screen """
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        
