import pygame
from pygame.locals import *
import random
from settings import Settings
from comet import Comet
from ship import Ship
from missile import Missile

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


# Game loop
running = True
comet_timer = 0
comet_delay = 1000  # Adjust the delay value (in milliseconds) as needed

clock = pygame.time.Clock()

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

    # Update comet timer
    comet_timer += dt

    comet_speed = 2  # Adjust the comet speed as needed
    # Create comets with a delay
    if comet_timer >= comet_delay:
        comet = Comet(settings.screen_width, comet_speed)
        comet_group.add(comet)
        comet_timer = 0

    # Update ship, comets, and missiles
    ship.update()
    comet_group.update()
    missile_group.update()

    # Remove missiles that are off-screen
    for missile in missile_group.copy():
        if missile.off_screen():
            missile_group.remove(missile)

    # Check for collisions between comets and missiles
    collisions = pygame.sprite.groupcollide(comet_group, missile_group, True, True)

    # Draw the screen
    screen.fill((0, 0, 0))
    comet_group.draw(screen)
    missile_group.draw(screen)
    pygame.draw.rect(screen, (0, 255, 0), ship.rect)
    pygame.display.flip()

# Quit the game
pygame.quit()
