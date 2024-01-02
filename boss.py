from setting import *
import pygame
from fireball import Fireball, fireballs, fireballs2
from building import all_sprites
from soundset import play_sound

# screen = pygame.display.set_mode((WIDTH, HEIGHT))

boss_path = get_path("img/boss")
boss_imgs = {}
boss_imgs['first'] = [pygame.transform.scale(pygame.image.load(path), (600, 500)) for path in boss_path['first']]
boss_imgs['second'] = [pygame.transform.scale(pygame.image.load(path), (600, 500)) for path in boss_path['second']]
boss_imgs['lose'] = [pygame.transform.scale(pygame.image.load(path), (600, 500)) for path in boss_path['lose']]

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.hp = 1000
        self.hp2 = 1000
        self.max_hp = 1000
        self.is_second = False
        self.image = boss_imgs['first'][0]
        self.animation = boss_imgs
        self.idx = 0
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 630
        self.rect.bottom = HEIGHT - 150
        self.orix = WIDTH - 630
        self.orib = HEIGHT - 150
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 200
        self.radius = int(self.rect.width * 0.3 / 2)
        
    def attack(self):
        if not self.is_second:
            fireball = Fireball(self.rect.centerx, self.rect.centery, 'fire')
            all_sprites.add(fireball)
            fireballs.add(fireball)
        else:
            fireball = Fireball(self.rect.centerx, self.rect.centery, 'fire')
            fireball2 = Fireball(self.rect.centerx, self.rect.centery, 'purple')
            all_sprites.add(fireball)
            all_sprites.add(fireball2)
            fireballs.add(fireball)
            fireballs2.add(fireball2)
        play_sound("sfx/boss_attack.wav", 1)
        
    def update(self):
        now = pygame.time.get_ticks()
        # pygame.draw.circle(screen, RED, self.rect.center, self.radius, 1)
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            if not self.is_second:
                self.image = self.animation['first'][self.idx % len(self.animation['first'])]
            elif self.is_second and self.hp > 0:
                self.image = self.animation['second'][self.idx % len(self.animation['second'])]
            elif self.is_second and self.hp <= 0:
                self.image = self.animation['lose'][self.idx % len(self.animation['lose'])]
        if self.hp <= 0 and not self.is_second:
            self.is_second = True
            self.hp = self.hp2