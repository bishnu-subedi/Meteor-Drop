import pygame
from pygame.locals import *
import random
from settings import Settings
from comet import Comet
from ship import Ship
from missile import Missile
from scoreboard import Scoreboard

# Initialize Pygame
pygame.init()

# Set up the screen
settings = Settings()
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
pygame.display.set_caption("Comet Game")

# Create comet group
comet_group = pygame.sprite.Group()
missile_group = pygame.sprite.Group()

# Create ship
ship = Ship(settings)

# Create scoreboard
scoreboard = Scoreboard(settings, screen)

# Game loop
running = True
game_over = False  # New variable for game over state
game_over_delay = None


comet_timer = 0
comet_delay = 1000  # Adjust the delay value (in milliseconds) as needed

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 48)  # Define the font for the restart button

restart_text = font.render("Restart", True, (0, 0, 0))
restart_rect = restart_text.get_rect(center=(400, 300))

restart_game = False

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
            elif event.key == K_SPACE and len(missile_group) < settings.missile_limit:
                missile = Missile(settings.screen_width, settings.screen_height, ship.rect)
                missile_group.add(missile)

        elif event.type == KEYUP:
            if event.key == K_LEFT and ship.speed < 0:
                ship.stop()
            elif event.key == K_RIGHT and ship.speed > 0:
                ship.stop()
        elif event.type == MOUSEBUTTONDOWN:
            if game_over and restart_rect.collidepoint(event.pos):
                restart_game = True
                game_over = False
                game_over_delay = None
                scoreboard.reset()
                comet_group.empty()
                missile_group.empty()

    # Update comet timer
    comet_timer += dt

    # Create comets with a delay
    if comet_timer >= comet_delay:
        comet = Comet(settings.screen_width, settings.comet_speed)
        comet_group.add(comet)
        comet_timer = 0

    # Update ship, comets, and missiles
    ship.update()
    comet_group.update()
    missile_group.update()

    # Check for collisions between comets and missiles
    collisions = pygame.sprite.groupcollide(comet_group, missile_group, True, True)
    for collision in collisions:
        scoreboard.score += 1

    # Check for collisions between ship and comets
    ship_collisions = pygame.sprite.spritecollide(ship, comet_group, True)
    for ship_collision in ship_collisions:
        scoreboard.decrease_ship()
        if scoreboard.ship_count <= 0:
            if not game_over:
                game_over = True
                game_over_delay = pygame.time.get_ticks()

    # Draw the screen
    screen.fill((0, 0, 0))
    comet_group.draw(screen)
    missile_group.draw(screen)
    pygame.draw.rect(screen, (0, 255, 0), ship.rect)

    # Update the scoreboard
    scoreboard.update_score()
    scoreboard.update_ships()

    # Show "game over" if all ships are depleted
    if game_over:
        scoreboard.show_game_over()
        pygame.draw.rect(screen, (255, 255, 255), (200, 250, 400, 100))  # Restart button background
        screen.blit(restart_text, restart_rect)

    pygame.display.flip()


    # # Check if game over delay has been set
    # if game_over_delay is not None:
    #     elapsed_time = pygame.time.get_ticks() - game_over_delay
    #     if elapsed_time >= 2000:  # Display the game over screen for 2000 milliseconds (2 seconds)
    #         game_over_delay = None
    #         running = False

    # Restart the game if requested
    if restart_game:
        restart_game = False
        game_over = False
        game_over_delay = None
        scoreboard.reset()
        comet_group.empty()
        missile_group.empty()

# Quit the game
pygame.quit()
