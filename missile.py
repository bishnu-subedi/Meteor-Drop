import pygame
from pygame.locals import *

RED = (255, 0, 0)

class Missile(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, ship_rect):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = ship_rect.centerx
        self.rect.bottom = ship_rect.top
        self.speed = -10  # Adjust the missile speed as needed

    def update(self):
        self.rect.y += self.speed

    def off_screen(self):
        return self.rect.bottom < 0
