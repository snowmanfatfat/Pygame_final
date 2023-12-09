'''貓貓 (主角)'''

import pygame
from projectile import Projectile
from soundset import play_sound
from setting import *
from building import all_sprites

player_img = [pygame.transform.scale(pygame.image.load(f"img/player/run-{i}.png"), (150, 150)) for i in range(1, 9)]
bullets = pygame.sprite.Group()
waterballs = pygame.sprite.Group()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.num = 0
        self.time = pygame.time.get_ticks()
        self.image = player_img[self.num]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.bottom = HEIGHT - 30
        self.radius = 35
        self.speedx = 8
        self.vel_y = 0 # 模擬重力
        self.health = 100
        self.gun = 1 # 單發或雙發
        self.gun_time = 0

        self.jump_counter = 0
        self.jumped = False

        self.p_range = 150
        self.p_trans = 90
        self.protected = True

        self.k_range = 100
        self.k_range_max = 1000

    def draw_protect(self, surf):
        surface = pygame.Surface((self.p_range * 2, self.p_range * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, (70, 70, 255, self.p_trans), (self.p_range, self.p_range), self.p_range)
        surf.blit(surface, (self.rect.x - self.p_range // 2, self.rect.y - self.p_range // 2))

    def draw_kill_all(self, surf):
        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(surface, (255, 255, 255, 140), (WIDTH // 2, HEIGHT // 2), self.k_range)
        surf.blit(surface, (0, 0))
        if self.k_range < self.k_range_max:
            self.k_range += 60
        else:
            self.k_range = 100

    # 射子彈
    def shoot(self):
        play_sound("sfx\smb_fireball.wav")
        if self.gun == 1:
            bullet = Projectile(self.rect.centerx, self.rect.top, 'bullet')
            all_sprites.add(bullet)
            bullets.add(bullet)
        elif self.gun == 2:
            bullet1 = Projectile(self.rect.centerx, self.rect.top, 'bullet')
            bullet2 = Projectile(self.rect.centerx, self.rect.bottom, 'bullet')
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            bullets.add(bullet1)
            bullets.add(bullet2)

    # 射水球
    def shootwater(self):
        play_sound("sfx\smw_swimming.wav")
        waterball = Projectile(self.rect.left, self.rect.centery, 'waterball')
        all_sprites.add(waterball)
        waterballs.add(waterball)

    # 武器升級成雙彈
    def gunup(self):
        self.gun = 2
        self.gun_time = pygame.time.get_ticks()
        
    def update(self):
        # 雙彈時間
        now = pygame.time.get_ticks()
        if self.gun == 2 and now - self.gun_time > 5000:
            self.gun = 1
            self.gun_time = now
        
        # 回到原地
        if self.rect.bottom == (HEIGHT - 30):
            self.jump_counter = 0

        # 二段跳
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_w] or key_pressed[pygame.K_SPACE]:
            if (not self.jumped) and self.rect.bottom <= (HEIGHT - 30):
                if self.jump_counter < 2:
                    play_sound("sfx\smb_jump-small.wav")
                    self.vel_y = -22
                    self.jump_counter += 1
                self.jumped = True

        if not key_pressed[pygame.K_SPACE] and not key_pressed[pygame.K_w]:
            self.jumped = False

        self.vel_y += 0.8
        if self.vel_y > 10:
            self.vel_y = 10
        self.rect.y += self.vel_y

        if key_pressed[pygame.K_d]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_a]:
            self.rect.x -= self.speedx

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT - 30:
            self.rect.bottom = HEIGHT - 30
        if self.rect.top < 0:
            self.rect.top = 0
        
        if now - self.time > 300:
            self.time = now
            self.num += 1
            self.image = player_img[self.num % len(player_img)]