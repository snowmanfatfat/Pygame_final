import pygame
import random
from setting import *
from pygame.math import Vector2

fireball_path = get_path("img/boss/attack")
fireball_imgs = [pygame.transform.scale(pygame.image.load(path), (100, 100)) for path in fireball_path['attack']]
fireballs = pygame.sprite.Group()

class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = fireball_imgs[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.radius = int(self.rect.width * 0.85 / 2)
        self.origin = Vector2(x, y)
        self.speed = FIREATK_SPEED
        self.calculate_speed()
        
    def calculate_speed(self):
        target = Vector2(random.randrange(-200, -100), random.randrange(100, HEIGHT - 50))
        direction = (target - self.origin).normalize()
        self.velocity = direction * self.speed
    
    def update(self):
        self.rect.move_ip(self.velocity)
        if not pygame.Rect(0, 0, WIDTH, HEIGHT).contains(self.rect):
            self.kill()
            