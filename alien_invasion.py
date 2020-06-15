# 08 / 05 / 2020 
# Alien Invasion game
# Author J'yrens Christenvie , Please acknowledge the author if you are using his code for your game
# People acknowledged : Eric Matthes 

import sys
import json
from time import sleep

import pygame 

from settings import Settings 
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from pause import Pause
from ship  import Ship
from bullet import Bullet 
from alien import Alien 
import sound_effects as se

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources """
        pygame.init()
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width,self.settings.screen_height))
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        #self.settings.screen_width = self.screen.get_rect().width 
        #self.settings.screen_height = self.screen.get_rect().height
        self.caption = "J'y-rens Alien Invasion 1.0"
        pygame.display.set_caption(self.caption)

        #Create an instance to store game statistics. 
        # and create a scoreboar.        
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)

        #bullet groups
        self.bullets = pygame.sprite.Group()

        #Alien Groups
        self.aliens = pygame.sprite.Group()

        # create fleet of aliens
        self._create_fleet()

        #Make the Play Button.
        self.play_button = Button(self,"Play")
        self.pause_button = Pause(self,"Pause")
        
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            #Watch for keyboard and mouse events.
            self._check_events()

            if self.stats.game_active and self.caption == "J'y-rens Alien Invasion 1.0":
                # Update the ship position 
                self.ship.update()

                # Update bullets and get rid of old bullets
                self._update_bullets()

                #Update the position of each Alien
                self._update_aliens()
            
            # Redraw the screen during each pass through the loop and flip to the new screen.
            self._update_screen()
            
    def _check_events(self):
        """ Respond to keypresses and mouse events """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.write_high_score_to_folder()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_pause_button(mouse_pos)          

    def _check_pause_button(self, mouse_pos):
        """Lock the game when the player cliks the pause  button """
        button_clicked = self.pause_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.stats.game_active:
            # Reset the game settings.
            self.stats.game_active = False
            #self.play_button.draw_button()
              
    def _check_play_button(self, mouse_pos):
        """Starts a new game when the player clicks Play """
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active :
            # Reset the game settings.     
            self.settings.initialize_dynamic_settings()
            # starts the game when the player clicks play and the game is inactive
            if self.stats.score == 0:
                self._start_game()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

    def _check_keydown_events(self,event):
        """ Respond to keypresses """
        if event.key == pygame.K_RIGHT:
            #Move the ship  to the right 
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            #Move the ship  to the left 
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self.write_high_score_to_folder()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p or pygame.K_KP_ENTER:
            if not self.stats.game_active:
                self._start_game()

    def write_high_score_to_folder(self):
        """write High score to folder"""
        with open(self.stats.filename, 'w') as f:
                    json.dump(self.stats.high_score, f)

    def _start_game(self):
        """Start the game when the player presses the button"""
        # Reset the game statistics.        
        self.stats.reset_stats()
        self.stats.game_active = True

        # Get rid of any remaining aliens and bullets 
        self.aliens.empty()
        self.bullets.empty()

        #Create a new fleet and center the ship.     
        self._create_fleet()
        self.ship.center_ship() 

        # Hide the mouse cursor.       
        pygame.mouse.set_visible(True)

    def _check_keyup_events(self,event):
        """ Respond to key releases """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            se.bullet_sound.play()

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets """
        # update the bullets
        self.bullets.update()

        # Get rid of old bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # Check for any bullets that have hit aliens.
        # If so , get rid of the alien and the bullet.
        self._check_bullet_allien_collisions()
        
    def _check_bullet_allien_collisions(self):
        """ Respond to bullet alien collisions """
        # Remove any bullets an allien that have collided
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True,True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
            se.alien_sound.play()

        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.start_new_level()

    def start_new_level(self):
        """Start a new level if aliens have been destroyed  """
        self.bullets.empty()
        self._create_fleet() 
        self.settings.increase_speed()

        # Increase level.       
        self.stats.level +=1
        self.sb.prep_level()

    def _create_fleet(self):
        """ Create fleet of Aliens """
        # create an Alien and find the number of aliens in a row
        # Spacing between each alien is equal to one alien width
        alien = Alien(self)
        
        alien_width = alien.rect.width
        alien_height = alien.rect.height

        # Determine the number columns that fit the aliens on the screen
        available_space_x = self.settings.screen_width - ( 2 * alien_width)
        number_aliens_x = available_space_x // (2*alien_width)
        
        # Determine the number of rows that fit the Alien on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - 
                                (3 * alien_height) - ship_height)
        number_rows = available_space_y //(2*alien_height)


        # create the full feet of aliens 
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number,row_number)
            
    def _create_alien(self,alien_number,row_number):
        """ Create an Instance of an Alien """
        #Create an alien and place it in the row  .       
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.y = alien_height + 2 * alien_height * row_number
        alien.rect.x = alien.x
        alien.rect.y = alien.y
        self.aliens.add(alien)
    
    def _check_fleet_edges(self):
        """Respond Appropriatly  if any aliens have reached the edge """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *=-1
    
    def _ship_hit(self):
        """Respond to the ship being hit by an alien """
        
        if self.stats.ships_left > 0:
            se.ship_hit_sound.play()

            # Decrement ships_left and update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaning aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause. 
            sleep(0.5)
        else:
            self.stats.game_active = False   
            pygame.mouse.set_visible(True) 

    def _check_aliens_bottom(self):
        """Check if aliens have reached the bottom of the screen """
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom :
                # Treat it the same way as if a ship got hit 
                self._ship_hit()
                break

    def _update_aliens(self):
        """Update the positions of all aliens in the fleet """
        
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions .
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        #Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    def _update_screen(self):
        """ Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        # Make the most recently drawn screen visible.
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw the score information
        self.sb.show_score()

        
        

        # Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()
        else:
            self.pause_button.draw_button()

        pygame.display.flip()

if __name__ == '__main__':
    #Make a game instance , and run the game.
    ai = AlienInvasion()
    ai.run_game()