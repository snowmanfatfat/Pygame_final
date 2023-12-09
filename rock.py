#掉落物
import pygame
import random
import os

from building import all_sprites
from setting import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

rock_imgs = []
rock_size = [(300,300), (200,200), (250,250), (300,300), (150,150), (200,200), (200,200), (200,200), (100,100), (120,120)]
for i in range(10):
    rock_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("img/rock", f"rock{i}.png")).convert(), rock_size[i]))

rocks = pygame.sprite.Group()

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rock_imgs)
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-180, -100)
        self.speedy = random.randrange(2, 5)
        self.speedx = random.randrange(-3, 3)
        self.total_degree = 0
        self.rot_degree = random.randrange(-3, 3)

    # 旋轉效果
    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree) # 每次旋轉都是以原圖為基準，因為若用旋轉後的圖繼續旋轉，會越來越模糊
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT  or self.rect.left > WIDTH or self.rect.right < 0 or self.rect.bottom < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)

#生成新的石頭
def new_rock():
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)