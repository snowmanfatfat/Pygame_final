from setting import *
import pygame
from fireball import Fireball, fireballs
from building import all_sprites

# screen = pygame.display.set_mode((WIDTH, HEIGHT))

boss_path = get_path("img/boss")
boss_imgs = {}
boss_imgs['win'] = [pygame.transform.scale(pygame.image.load(path), (750, 500)) for path in boss_path['win']]
boss_imgs['lose'] = [pygame.transform.scale(pygame.image.load(path), (750, 500)) for path in boss_path['lose']]

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.hp = 1000
        self.damage = 20
        self.image = boss_imgs['win'][0]
        self.animation = boss_imgs
        self.idx = 0
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 650
        self.rect.bottom = HEIGHT - 150
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 200
        self.radius = int(self.rect.width * 0.3 / 2)
        
    def attack(self):
        fireball = Fireball(self.rect.centerx, self.rect.centery)
        all_sprites.add(fireball)
        fireballs.add(fireball)
        
    def update(self):
        now = pygame.time.get_ticks()
        # pygame.draw.circle(screen, RED, self.rect.center, self.radius, 1)
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.idx += 1
            if self.hp <= 0:
                self.image = self.animation['lose'][self.idx % len(self.animation['lose'])]
            else:
                self.image = self.animation['win'][self.idx % len(self.animation['win'])]
            self.image.set_colorkey(WHITE)