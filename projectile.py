'''子彈'''

import pygame
import os
import math
from setting import *

# screen = pygame.display.set_mode((WIDTH, HEIGHT))

bullet_img = pygame.transform.scale(pygame.image.load(os.path.join("img/bullet", "waterbullet.png")), (80, 80))
water_img = pygame.transform.scale(pygame.image.load(os.path.join("img/bullet", "watercolumn.png")), (108, 108))

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        c, d = pygame.mouse.get_pos()
        if type == 'bullet':
            self.image_ori = bullet_img
            self.image = self.image_ori.copy()
            self.speed = BULLET_SPEED
        elif type == 'water':
            self.image_ori = water_img
            self.image = self.image_ori.copy()
            self.speed = BULLET_SPEED
        else:
            raise ValueError('type must be bullet or water')
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        self.rect.centerx = x
        self.rect.centery = y
        
        angle = math.atan2(d - y, c - x)
        self.angle_degrees = math.degrees(angle)
        
        distance_A_B = math.sqrt((x - c) ** 2 + (y - d) ** 2)
        unit_vector_x = (c - x) / distance_A_B
        unit_vector_y = (d - y) / distance_A_B
        self.speedx = unit_vector_x * self.speed
        self.speedy = unit_vector_y * self.speed
        
    def rotate(self):
        self.image = pygame.transform.rotate(self.image_ori, -self.angle_degrees) 
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        # pygame.draw.circle(screen, RED, self.rect.center, self.radius, 1)
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()  # 矩形超出屏幕範圍
        