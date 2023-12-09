import pygame
import os
import time
from setting import *
from tutorial import Tutorial
from buttons import Buttons

pygame.init()
pygame.mixer.init()

start_img = pygame.transform.scale(pygame.image.load(os.path.join("img/start_menu", f"btn-start.png")), (285, 100))
sound_img = pygame.transform.scale(pygame.image.load(os.path.join("img/start_menu", f"sound.png")), (70, 70))
mute_img = pygame.transform.scale(pygame.image.load(os.path.join("img/start_menu", f"mute.png")), (70, 70))
title_anim = [pygame.transform.scale(pygame.image.load(os.path.join("img/start_menu/title", f"title-ani-{i}.png")), (WIDTH, HEIGHT)) for i in range(20)]

class StartMenu:
    def __init__(self):
        # win
        self.menu_win = pygame.display.set_mode((WIDTH, HEIGHT))

        # button
        self.title_anim = title_anim
        self.animation_index = 0
        self.title_img = title_anim[0]
        self.last_update = time.time()
        self.frame_rate = 0.1 # 每0.1秒換一張圖
        self.start_btn = Buttons(start_img, WIDTH // 2 - 142.5, 650)
        self.sound_btn = Buttons(sound_img, WIDTH - 175, 720)
        self.mute_btn = Buttons(mute_img, WIDTH - 85, 720)
        self.volume = 0.4

    def play_music(self):
        pygame.mixer.music.load("audio/meowSSion.mp3")
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(-1, 0)

    def draw(self, surf):
        surf.blit(self.title_img, (0, 0))
        surf.blit(self.start_btn.img, (WIDTH // 2 - 142.5, 650))
        surf.blit(self.sound_btn.img, (WIDTH - 175, 720))
        surf.blit(self.mute_btn.img, (WIDTH - 85, 720))

    def update_animation(self):
        now = time.time()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.animation_index += 1
            self.title_img = self.title_anim[self.animation_index % len(self.title_anim)]

    def menu_run(self):
        run = True
        clock = pygame.time.Clock()
        pygame.display.set_caption("貓貓救援大作戰")
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
                    if self.sound_btn.is_clicked(x, y):
                        pygame.mixer.music.unpause()

                    if self.mute_btn.is_clicked(x, y):
                        pygame.mixer.music.pause()

                    if self.start_btn.is_clicked(x, y):
                       ttl = Tutorial()
                       ttl.ttl_run()
                       run = False

            pygame.display.update()
        pygame.quit()