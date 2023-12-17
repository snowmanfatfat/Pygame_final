'''在地上的火'''

import pygame
import random
from building import all_sprites
from setting import *

fire_img = [pygame.transform.scale(pygame.image.load(f"img/fire/fire_{i}.png"),(140,112)) for i in range(6)]
fires = pygame.sprite.Group()

class Fire(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.frame = 0
        self.image = fire_img[self.frame]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        self.rect.x = random.randrange(WIDTH + 100, WIDTH + 800)
        self.rect.bottom = HEIGHT - 50
        self.speed_fire = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 200

    def update(self):
        self.rect.move_ip(-self.speed_fire, 0)
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            self.image = fire_img[self.frame % 6] 
        if self.rect.right < 0:
            self.kill()
            new_fire()

#生成新的火
def new_fire():
    f = Fire()
    all_sprites.add(f)
    fires.add(f)