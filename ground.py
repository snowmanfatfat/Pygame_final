'''地板（背景）'''
import pygame
from setting import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

ground_path = get_path("img/ground")
ground_name = list(ground_path.keys())
# print(ground_name)
ground_img = {}
for name in ground_name:
    ground_img[name] = [pygame.transform.scale(pygame.image.load(path).convert(), (1440, 810)) for path in ground_path[name]]

class Ground:
    def __init__(self):
        self.ground_name = ground_name
        self.ground_img = ground_img
        self.count = 0
        self.imgs = ground_img[ground_name[0]]
        self.imgs_rect = []
        self.ground_speed = SPEED
        
        for img in self.imgs:
            self.imgs_rect.append(img.get_rect())
    
        for i in range(len(self.imgs_rect)):
            self.imgs_rect[i].left = WIDTH * i

    def update(self):
        for i in range(len(self.imgs_rect)):
            self.imgs_rect[i].left -= self.ground_speed
            if self.imgs_rect[i].right <= 0:
                self.imgs_rect[i].left = WIDTH * (len(self.imgs_rect) - 1)

    def draw(self, screen):
        for i in range(len(self.imgs_rect)):
            screen.blit(self.imgs[i], self.imgs_rect[i])

    def change_ground(self):
        self.count += 1
        self.imgs = self.ground_img[self.ground_name[self.count % len(self.ground_name)]]
        