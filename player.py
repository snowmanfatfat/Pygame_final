'''貓貓 (主角)'''

import pygame
from projectile import Projectile
from soundset import play_sound
from setting import *
from building import all_sprites

# screen = pygame.display.set_mode((WIDTH, HEIGHT))

player_path = get_path("img/player/new")
player_img = [pygame.transform.scale(pygame.image.load(path), (200, 250)) for path in player_path['new']]
bullets = pygame.sprite.Group()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.num = 0
        self.time = pygame.time.get_ticks()
        self.image = player_img[self.num]
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.bottom = HEIGHT - 30
        self.radius = 70

        self.speedx = 8
        self.vel_y = 0 # 模擬重力
        self.hp = 100
        self.max_hp = 100
        self.gun = 1 # 單發或雙發
        self.gun_time = 0

        self.jump_counter = 0
        self.jumped = False

        self.p_range = 150
        self.p_trans = 90

        self.k_range = 100
        self.k_range_max = 1000

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
        play_sound("sfx\smw_swimming.wav")
        if self.gun == 1:
            bullet = Projectile(self.rect.centerx, self.rect.centery, 'bullet')
            all_sprites.add(bullet)
            bullets.add(bullet)
        elif self.gun == 2:
            bullet = Projectile(self.rect.centerx, self.rect.centery, 'water')
            all_sprites.add(bullet)
            bullets.add(bullet)

    # 武器升級成連發
    def gunup(self):
        self.gun = 2
        
    def update(self):
        # pygame.draw.circle(screen, RED, self.rect.center, self.radius, 1)
        self.image.set_colorkey(WHITE)
        if self.hp > 0:
            now = pygame.time.get_ticks()
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