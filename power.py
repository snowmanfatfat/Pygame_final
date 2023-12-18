'''補給品'''

import pygame
import random
import os
from setting import *

# screen = pygame.display.set_mode((WIDTH, HEIGHT))

powers = pygame.sprite.Group()
power_imgs = {}
power_imgs['blood'] = pygame.transform.scale(pygame.image.load(os.path.join("img/power", "heart.png")), (100,100))
power_imgs['gun'] = pygame.transform.scale(pygame.image.load(os.path.join("img/power", "doublewater.png")), (150,100))
power_imgs['mana'] = pygame.transform.scale(pygame.image.load(os.path.join("img/power", "mana.png")), (100,100))

class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['blood', 'gun', 'mana'])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speed = 3

    def update(self):
        # pygame.draw.rect(screen, RED, self.rect, 1)
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()