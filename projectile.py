'''子彈'''

import pygame
import os
import math
from setting import *

bullet_big_img = pygame.transform.scale(pygame.image.load(os.path.join("img/bullet", "PeaNormal_0.png")), (108, 64))
waterball_big_img = pygame.transform.scale(pygame.image.load(os.path.join("img/bullet", "PeaIce_0.png")), (108, 64))

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        c, d = pygame.mouse.get_pos()
        if type == 'bullet':
            self.image = bullet_big_img
            self.speed = BULLET_SPEED
        elif type == 'waterball':
            self.image = waterball_big_img
            self.speed = WATERBALL_SPEED
        else:
            raise ValueError('type must be bullet or waterball')
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        distance_A_B = math.sqrt((x - c) ** 2 + (y - d) ** 2)
        unit_vector_x = (c - x) / distance_A_B
        unit_vector_y = (d - y) / distance_A_B
        self.speedx = unit_vector_x * self.speed
        self.speedy = unit_vector_y * self.speed

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()  # 矩形超出屏幕範圍
        