import pygame
import random

#WHITE = (255, 255, 255)

class Meteor(pygame.sprite.Sprite):
    def __init__(self, screen_width, speed):
        super().__init__()
        self.image = pygame.image.load('images/meteor.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
