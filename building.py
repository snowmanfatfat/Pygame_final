'''建築物'''

import pygame
import random
import os
from setting import *

all_sprites = pygame.sprite.Group()
buildings = pygame.sprite.Group()

sizes = [(150, 150), (140, 240), (100, 240), (220, 216), (150, 150), (150, 150), (160, 240)]
building_imgs = [pygame.transform.scale(pygame.image.load(os.path.join("img/building", f"building{i}.png")), size) for i, size in enumerate(sizes)]

class Building(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(building_imgs)
        self.image_ori.set_colorkey(BLACK) # 因為背景黑色，所以設定黑色為透明不渲染
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect() # rect有width, height, top, bottom, left, right, center, centerx, centery, x, y屬性
        self.height = self.image.get_height()
        self.radius = int(self.rect.width * 0.85 / 2)
        self.rect.x = random.randrange(WIDTH + 100, WIDTH + 800)
        self.rect.bottom = HEIGHT - 30
        self.speed_build = SPEED

    def update(self):
        self.rect.move_ip(-self.speed_build, 0)
        if self.rect.right < 0:
            self.kill()
            new_building()
        
#生成新的建築
def new_building():
    b = Building()
    all_sprites.add(b)
    buildings.add(b)