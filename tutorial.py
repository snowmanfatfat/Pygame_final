import pygame
import os
import time
from setting import *
from fire import fire_img
from building import building_anim
from player import player_img
from game import Game

ttl_path = get_path("img/tutorial")
ttl_name = ['a', 'b', 'c', 'tutorial']
ttl_ani = {}
for name in ttl_name:
    ttl_ani[name] = [pygame.transform.scale(pygame.image.load(path), (WIDTH, HEIGHT)) for path in ttl_path[name]]

class Tutorial:
    def __init__(self):
        # win
        self.menu_win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.page = 0
        
        self.ani_idx = 0
        self.fire_ani = fire_img
        self.fire_img = fire_img[0]
        
        self.ani_idx2 = 0
        self.buliding_ani = building_anim
        self.buliding_img = building_anim[0]
        
        self.ani_idx3 = 0
        self.player_ani = player_img
        self.player_img = player_img[0]
        
        self.ttl_count = 0
        self.ttl_ani = ttl_ani
        self.ttl_name = ttl_name
        self.ttl_img = ttl_ani[ttl_name[0]][0]
        
        self.last_update = time.time()
        self.last_update2 = time.time()
        self.last_update3 = time.time()
        self.last_update4 = time.time()
        
        self.bgframe_rate = 1
        self.frame_rate = 0.1

    def draw_ttl(self, surf, page):
        ttl_ani['tutorial'][page].set_colorkey(BLACK)
        surf.blit(ttl_ani['tutorial'][page], (0, 0))
        
    def update_bg(self, surf, page):
        surf.blit(self.ttl_img, (0, 0))
        now = time.time()
        if now - self.last_update4 > self.bgframe_rate:
            self.last_update4 = now
            self.ttl_count += 1
            self.ttl_img = self.ttl_ani[self.ttl_name[page]][self.ttl_count % len(self.ttl_ani[self.ttl_name[page]])]

    def update_fire(self, surf):
        surf.blit(self.fire_img, (450, 520))
        now = time.time()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.ani_idx += 1
            self.fire_img = self.fire_ani[self.ani_idx % len(self.fire_ani)]
    
    def update_buliding(self, surf):
        surf.blit(self.buliding_img, (900, 210))
        now = time.time()
        if now - self.last_update2 > self.frame_rate:
            self.last_update2 = now
            self.ani_idx2 += 1
            self.buliding_img = self.buliding_ani[self.ani_idx2 % len(self.buliding_ani)]

    def update_player(self, surf):
        surf.blit(self.player_img, (380, 280))
        now = time.time()
        if now - self.last_update3 > self.frame_rate:
            self.last_update3 = now
            self.ani_idx3 += 1
            self.player_img = self.player_ani[self.ani_idx3 % len(self.player_ani)]
        
    def ttl_run(self):
        pygame.init()
        
        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(FPS)
            self.update_bg(self.menu_win, self.page)
            self.draw_ttl(self.menu_win, self.page)
            
            if self.page == 1:
                self.update_player(self.menu_win)
            elif self.page == 0:
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
                    if event.button == 1:
                        self.page += 1
                    elif event.button == 3:
                        self.page -= 1
                        self.page = max(self.page, 0)
                        
            if self.page == len(ttl_ani['tutorial']):
                game = Game()
                game.game_run()
                run = False
                
            pygame.display.update()