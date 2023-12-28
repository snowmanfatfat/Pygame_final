'''補給品'''

import pygame
import random
import os
from setting import *

# screen = pygame.display.set_mode((WIDTH, HEIGHT))

powers = pygame.sprite.Group()
power_imgs = {}
power_imgs['blood'] = pygame.transform.scale(pygame.image.load(os.path.join("img/power", "heart.png")), (100,100))
power_imgs['gun'] = pygame.transform.scale(pygame.image.load(os.path.join("img/power", "doublewater.png")), (100,100))
power_imgs['mana'] = pygame.transform.scale(pygame.image.load(os.path.join("img/power", "mana.png")), (100,100))
power_imgs['r'] = pygame.transform.scale(pygame.image.load(os.path.join("img/power", "r.png")), (100,100))
power_imgs['a'] = pygame.transform.scale(pygame.image.load(os.path.join("img/power", "a.png")), (100,100))
power_imgs['c'] = pygame.transform.scale(pygame.image.load(os.path.join("img/power", "c.png")), (100,100))
power_imgs['e'] = pygame.transform.scale(pygame.image.load(os.path.join("img/power", "e.png")), (100,100))

class Power(pygame.sprite.Sprite):
    def __init__(self, center, type):
        pygame.sprite.Sprite.__init__(self)
        if type == 'r':
            self.type = 'r'
        elif type == 'a':
            self.type = 'a'
        elif type == 'c':
            self.type = 'c'
        elif type == 'e':
            self.type = 'e'
        else:
            self.type = random.choice(['blood', 'gun', 'mana'])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        if type == 'none':
            self.rect.center = center
        else:
            self.rect.center = center
            self.rect.centerx += 100
        self.speed = 3

    def update(self):
        # pygame.draw.rect(screen, RED, self.rect, 1)
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()