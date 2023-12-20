import pygame
import os
import math
from setting import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

ult_img = pygame.transform.scale(pygame.image.load(os.path.join("img/bullet", "ult.png")).convert(), (1000, 600))

class Ultimate(pygame.sprite.Sprite):
    def __init__(self, x=WIDTH, y=HEIGHT):
        pygame.sprite.Sprite.__init__(self)
        self.img_ori = ult_img
        self.img_ori.set_colorkey(BLACK)
        self.image = self.img_ori.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rectx_ori = x
        self.recty_ori = y
        self.angle = 0
        self.originPos = [0,5]
    
    def blitRotate(self):
        w = self.rect.width
        h = self.rect.height
        pos = [self.rectx_ori, self.recty_ori] 
    
        # calcaulate the axis aligned bounding box of the rotated image
        sin_a, cos_a = math.sin(math.radians(self.angle)), math.cos(math.radians(self.angle)) 
        min_x, min_y = min([0, sin_a*h, cos_a*w, sin_a*h + cos_a*w]), max([0, sin_a*w, -cos_a*h, sin_a*w - cos_a*h])
        
        # calculate the translation of the pivot 
        pivot        = pygame.math.Vector2(self.originPos[0], - self.originPos[1])
        pivot_rotate = pivot.rotate(self.angle)
        pivot_move   = pivot_rotate - pivot

        # calculate the upper left origin of the rotated image
        new_x = pos[0] - self.originPos[0] + min_x - pivot_move[0]
        new_y = pos[1] - self.originPos[1] - min_y + pivot_move[1]
        self.rect.x = new_x
        self.rect.y = new_y

        # get a rotated image
        self.image = pygame.transform.rotate(self.img_ori, self.angle)
        self.image.set_colorkey(BLACK)

    def update(self):
        self.blitRotate()
        self.angle += 1
        if self.angle > 90:
            self.kill()