import pygame
import os
import time
from setting_menu import SettingMenu
from setting import *
from tutorial import Tutorial
from buttons import Buttons

pygame.init()
pygame.mixer.init()

start_img = pygame.transform.scale(pygame.image.load(os.path.join("img/start_menu", f"start.png")), (285, 100))
# end_img = pygame.transform.scale(pygame.image.load(os.path.join("img/start_menu", f"end.png")), (285, 100))
setting_img = pygame.transform.scale(pygame.image.load(os.path.join("img/start_menu", f"setting.png")), (70, 70))

title_path = get_path("img/start_menu/title1")
title_anim = [pygame.transform.scale(pygame.image.load(path), (WIDTH, HEIGHT)) for path in title_path['title1']]

class StartMenu:
    def __init__(self):
        # win
        self.menu_win = pygame.display.set_mode((WIDTH, HEIGHT))

        # button
        self.title_anim = title_anim
        self.animation_index = 0
        self.title_img = title_anim[0]
        # self.setting_bg = setting_bg
        self.setting_menu = SettingMenu()
        
        self.last_update = time.time()
        self.frame_rate = 0.1 # 每0.1秒換一張圖
        self.start_btn = Buttons(start_img, 867, 208)
        # self.end_btn = Buttons(end_img, WIDTH // 2 - 142.5, 650)
        self.setting_btn = Buttons(setting_img, WIDTH - 95, 50)
        self.volume = 0.4

    def play_music(self):
        pygame.mixer.music.load("audio/meowSSion.mp3")
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(-1, 0)
    
    def draw(self, surf):
        surf.blit(self.title_img, (0, 0))
        # surf.blit(self.start_btn.img, self.start_btn.rect)
        # surf.blit(self.end_btn.img, self.end_btn.rect)
        surf.blit(self.setting_btn.img, self.setting_btn.rect)

    def update_animation(self):
        now = time.time()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.animation_index += 1
            self.title_img = self.title_anim[self.animation_index % len(self.title_anim)]

    def menu_run(self):
        pygame.init()
        run = True
        clock = pygame.time.Clock()
        pygame.display.set_caption("家裡放煙火囉")
        self.play_music()

        while run:
            clock.tick(FPS)
            self.update_animation()
            self.draw(self.menu_win)
            x, y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(x, y)
                    if self.setting_btn.is_clicked(x, y):
                        self.setting_menu.setting_show(self.menu_win)
                    
                    # if self.end_btn.is_clicked(x, y):
                    #     run = False

                    if self.start_btn.is_clicked(x, y):
                        ttl = Tutorial()
                        ttl.ttl_run()
                        run = False
                       

            pygame.display.update()
        pygame.quit()