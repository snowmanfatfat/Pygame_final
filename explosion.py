'''爆炸特效'''

import pygame
import os
from setting import *

BLACK = (0, 0, 0)

expl_path = get_path("img/explosion")

expl_anim = {'lg': [], 'sm': [], 'player': []}

for path in expl_path['expl']:
    image = pygame.image.load(path)
    image.set_colorkey(WHITE)
    expl_anim['lg'].append(pygame.transform.scale(image, (200, 200)))
    expl_anim['sm'].append(pygame.transform.scale(image, (150, 150)))
    
for path in expl_path['player']:
    image = pygame.image.load(path)
    image.set_colorkey(WHITE)
    expl_anim['player'].append(pygame.transform.scale(image, (200, 200)))
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.frame = 0
        self.size = size
        self.image = expl_anim[self.size][self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        self.frame_rate2 = 100

    def update(self):
        now = pygame.time.get_ticks()
        frame_rate = self.frame_rate2 if self.size == 'player' else self.frame_rate
        if now - self.last_update > frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]