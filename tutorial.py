import pygame
import os
import time
from setting import *
from fire import fire_img
from game import Game

ttl_list = [pygame.transform.scale(pygame.image.load(os.path.join("img/tutorial", f"ttl-{i+1}.png")), (WIDTH, HEIGHT)) for i in range(5)]
player_img = pygame.transform.scale(pygame.image.load("img/player/new/fireman0.png"), (130, 130))

class Tutorial:
    def __init__(self):
        # win
        self.menu_win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.page = 0
        self.fire_num = 0
        self.fire_image = fire_img[self.fire_num]
        self.last_update = time.time()
        self.frame_rate = 0.1

    def draw(self, page, surf):
        surf.blit(ttl_list[page], (0, 0))

    def draw2(self, surf):
        surf.blit(player_img, (900, 350))

    def fire_ani(self, surf):
        now = time.time()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.fire_num += 1
            self.fire_image = fire_img[self.fire_num % len(fire_img)]
        surf.blit(self.fire_image, (840, 500))
        surf.blit(self.fire_image, (930, 500))

    def ttl_run(self):
        pygame.init()
        
        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(FPS)
            self.draw(self.page, self.menu_win)
            if self.page == 0:
                self.fire_ani(self.menu_win)
            elif self.page == 2:
                self.draw2(self.menu_win)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if self.page == len(ttl_list)-1 or  event.key == pygame.K_s:
                        game = Game()
                        game.game_run()
                        run = False
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.page += 1
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.page -= 1
                        self.page = max(self.page, 0)
                        
            pygame.display.update()