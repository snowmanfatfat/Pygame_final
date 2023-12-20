import pygame
import os
import time
from setting import *
from fire import fire_img
from building import building_anim
from game import Game

ttl_path = get_path("img/tutorial")
ttl_list = [pygame.transform.scale(pygame.image.load(path), (WIDTH, HEIGHT)) for path in ttl_path['tutorial']]
# ttl_list = [pygame.transform.scale(pygame.image.load(os.path.join("img/tutorial", f"ttl-{i+1}.png")), (WIDTH, HEIGHT)) for i in range(5)]

class Tutorial:
    def __init__(self):
        # win
        self.menu_win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.page = 0
        self.ani_idx = 0
        self.ani_idx2 = 0
        self.fire_ani = fire_img
        self.fire_img = fire_img[0]
        self.buliding_ani = building_anim
        self.buliding_img = building_anim[0]
        self.last_update = time.time()
        self.frame_rate = 0.05

    def draw(self, page, surf):
        surf.blit(ttl_list[page], (0, 0))

    def update_fire(self, surf):
        now = time.time()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.ani_idx += 1
            self.fire_img = self.fire_ani[self.ani_idx % len(self.fire_ani)]
        surf.blit(self.fire_img, (500, 260))
    
    def update_buliding(self, surf):
        now = time.time()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.ani_idx2 += 1
            self.buliding_img = self.buliding_ani[self.ani_idx2 % len(self.buliding_ani)]
        surf.blit(self.buliding_img, (1000, 340))

    def ttl_run(self):
        pygame.init()
        
        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(FPS)
            self.draw(self.page, self.menu_win)
            
            if self.page == 1:
                self.update_fire(self.menu_win)
                self.update_buliding(self.menu_win)
            
            x, y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.page += 1
                    elif event.key == pygame.K_a:
                        self.page -= 1
                        self.page = max(self.page, 0)
                        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(x, y)
                    if event.button == 1:
                        self.page += 1
                    elif event.button == 3:
                        self.page -= 1
                        self.page = max(self.page, 0)
                        
            if self.page == len(ttl_list):
                game = Game()
                game.game_run()
                run = False
                
            pygame.display.update()