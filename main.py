import pygame
from pygame.locals import *
import random
from settings import Settings
from meteor import Meteor
from ship import Ship
from missile import Missile
from scoreboard import Scoreboard

# Initialize Pygame
pygame.init()

# Set up the screen
settings = Settings()
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
pygame.display.set_caption("Meteor Game")

# Create meteor group
meteor_group = pygame.sprite.Group()
missile_group = pygame.sprite.Group()

# Create ship
ship = Ship(settings)

# Create scoreboard
scoreboard = Scoreboard(settings, screen)

# Game loop
running = True
game_over = False  
game_over_delay = None


meteor_timer = 0
meteor_delay = 1000  # Delay value (in milliseconds)

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 48)  # Font for the restart button (Play again)

restart_text = font.render("Play Again", True, (255, 255, 255))
restart_rect = restart_text.get_rect(center=(400, 300))

restart_game = False
game_active = True

while running:
    dt = clock.tick(60)  # Limit the frame rate to 60 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_q:
                running = False
            elif event.key == K_LEFT:
                ship.move_left()
            elif event.key == K_RIGHT:
                ship.move_right()
            elif event.key == K_SPACE:
                missile = Missile(settings.screen_width, settings.screen_height, ship.rect)
                missile_group.add(missile)

        elif event.type == KEYUP:
            if event.key == K_LEFT and ship.speed < 0:
                ship.stop()
            elif event.key == K_RIGHT and ship.speed > 0:
                ship.stop()
        elif event.type == MOUSEBUTTONDOWN:
            if game_over and restart_rect.collidepoint(event.pos):
                game_active = True
                restart_game = True
                game_over = False
                game_over_delay = None
                scoreboard.reset()
                meteor_group.empty()
                missile_group.empty()

    if game_active:

        # Update meteor timer
        meteor_timer += dt

        # Create meteors with a delay
        if meteor_timer >= meteor_delay:
            meteor = Meteor(settings.screen_width, settings.meteor_speed)
            meteor_group.add(meteor)
            meteor_timer = 0

        # Update ship, meteors, and missiles
        ship.update()
        meteor_group.update()
        missile_group.update()

    # Check for collisions between meteors and missiles
    collisions = pygame.sprite.groupcollide(meteor_group, missile_group, True, True)
    for collision in collisions:
        scoreboard.score += 1

    # Check for collisions between ship and meteors
    ship_collisions = pygame.sprite.spritecollide(ship, meteor_group, True)
    for ship_collision in ship_collisions:
        scoreboard.decrease_ship()
        if scoreboard.ship_count <= 0:
            game_active = False  # Set game_active to False to freeze the screen
            if not game_over:
                game_over = True
                game_over_delay = pygame.time.get_ticks()

    # Draw the screen
    screen.fill((255, 255, 255))
    meteor_group.draw(screen)
    missile_group.draw(screen)
    screen.blit(ship.image, ship.rect) # Draw the ship image
    
    # Update the scoreboard
    scoreboard.update_score()
    scoreboard.update_ships()

    # Show "game over" if all ships are depleted
    if game_over:
        scoreboard.show_game_over()
        pygame.draw.rect(screen, (0, 0, 0), (200, 250, 400, 100))  # Restart button background
        screen.blit(restart_text, restart_rect)

    pygame.display.flip()

    # Restart the game if requested
    if restart_game:
        restart_game = False
        game_over = False
        game_over_delay = None
        scoreboard.reset()
        meteor_group.empty()
        missile_group.empty()
