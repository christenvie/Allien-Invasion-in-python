
# Author J'yrens Christenvie , Please acknowledge the author if you are using his code for your game
# People acknowledged : Eric Matthes 

import pygame

pygame.mixer.init()

bullet_sound = pygame.mixer.Sound('sounds/laser1.wav')
alien_sound =pygame.mixer.Sound('sounds/explosion01.wav')
ship_hit_sound = pygame.mixer.Sound('sounds/explosion-01.wav')