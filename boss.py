from setting import *
import pygame
from fireball import Fireball, fireballs
from building import all_sprites

boss_path = get_path("img/boss")
boss_imgs = [pygame.transform.scale(pygame.image.load(path), (300, 500)) for path in boss_path['boss']]

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.hp = 1000
        self.damage = 20
        self.image = boss_imgs[0]
        self.animation = boss_imgs
        self.idx = 0
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 350
        self.rect.bottom = HEIGHT - 150
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 200
        
    def attack(self):
        fireball = Fireball(self.rect.centerx, self.rect.centery)
        all_sprites.add(fireball)
        fireballs.add(fireball)
        
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.idx += 1
            self.image = self.animation[self.idx % len(self.animation)]
            self.image.set_colorkey(WHITE)