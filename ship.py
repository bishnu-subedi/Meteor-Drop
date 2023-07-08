import pygame
from pygame.locals import *

class Ship(pygame.sprite.Sprite):
    def __init__(self, settings):
        super().__init__()
        self.image = pygame.image.load('images/ship.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = settings.screen_width // 2 - self.rect.width // 2
        self.rect.y = settings.screen_height - self.rect.height
        self.speed = 0
        self.settings = settings

    def update(self):
        self.rect.x += self.speed
        self.rect.x = max(0, min(self.rect.x, self.settings.screen_width - self.rect.width))

    def move_left(self):
        self.speed = -5  # Ship speed moving left

    def move_right(self):
        self.speed = 5  # Ship speed moving right

    def stop(self):
        self.speed = 0
