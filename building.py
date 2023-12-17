'''建築物'''

import pygame
import random
import os
from setting import *

# screen = pygame.display.set_mode((WIDTH, HEIGHT))   

all_sprites = pygame.sprite.Group()
buildings = pygame.sprite.Group()

building_path = get_path("img/building")
building_anim = [pygame.transform.scale(pygame.image.load(path), (400, 350)) for path in building_path['building']]
class Building(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.frame = 0
        self.anim = building_anim
        self.image = building_anim[0]
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.7 / 2)
        self.rect.x = random.randrange(WIDTH + 100, WIDTH + 800)
        self.rect.bottom = HEIGHT - 30
        self.speed_build = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 200

    def update(self):
        # pygame.draw.circle(screen, RED, self.rect.center, self.radius, 1)
        self.rect.move_ip(-self.speed_build, 0)
        if self.rect.right < 0:
            self.kill()
            new_building()
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            self.image = self.anim[self.frame % len(self.anim)] 
        
#生成新的建築
def new_building():
    b = Building()
    all_sprites.add(b)
    buildings.add(b)