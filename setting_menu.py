import pygame
import os
from setting import *
from buttons import Buttons

sound_img = pygame.transform.scale(pygame.image.load(os.path.join("img/start_menu", f"sound.png")), (60, 60))
mute_img = pygame.transform.scale(pygame.image.load(os.path.join("img/start_menu", f"mute.png")), (60, 60))
end_img = pygame.transform.scale(pygame.image.load(os.path.join("img/start_menu", f"end.png")), (285, 100))
bg_img = pygame.transform.scale(pygame.image.load(os.path.join("img/start_menu", f"bg.png")), (WIDTH, HEIGHT))

class SettingMenu:
    def __init__(self):
        self.font_name = os.path.join("ttf","HanyiSentyPagoda.ttf")
        self.sound_img = sound_img
        self.mute_img = mute_img
        self.bg_img = bg_img
        self.circle_start = 0.4 * (360-90) + 90
        self.volume = 0.4
        self.volume_state = False
        self.sound_btn = Buttons(sound_img, 20, 120)
        self.mute_btn = Buttons(mute_img, 20, 120)
        self.end_btn = Buttons(end_img, 82, 200)
        self.is_mute = False
        self.x = 490
        self.y = 220
        
    def is_clicked(self, x, y):
        if self.circle.collidepoint(x, y):
            return True
        return False
    
    def draw(self, surf):
        surface = pygame.Surface((450,350), pygame.SRCALPHA)
        font = pygame.font.Font(self.font_name, 60)
        text_surface = font.render("Setting", True, BLACK)
        text_rect = text_surface.get_rect()
        text_rect.centerx = 225
        text_rect.top = 30
        surface.blit(text_surface, text_rect)
        
        text_surface2 = font.render(f'{self.volume*100:.0f}', True, BLACK)
        text_rect = text_surface.get_rect()
        text_rect.x = 370
        text_rect.centery = 150
        surface.blit(text_surface2, text_rect)
        
        pygame.draw.line(surface, RED, (90,150), (360,150), 5)
        self.circle = pygame.draw.circle(surface, WHITE, (self.circle_start,150), 10)
        
        if self.is_mute or self.volume == 0:
            surface.blit(self.mute_btn.img, self.mute_btn.rect)
            pygame.mixer.music.pause()
        else:
            surface.blit(self.sound_btn.img, self.sound_btn.rect)
            pygame.mixer.music.unpause()
        surface.blit(self.end_btn.img, self.end_btn.rect)
        surf.blit(self.bg_img, (0,0))
        surf.blit(surface, (self.x, self.y))
        
    def setting_show(self, surf):
        pygame.init()
        run = True
        clock = pygame.time.Clock()
        while run:
            pygame.mixer.music.set_volume(self.volume)
            clock.tick(FPS)
            self.draw(surf)
            x , y = pygame.mouse.get_pos()
            x -= self.x
            y -= self.y
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.is_clicked(x, y):
                        self.is_mute = False
                        pygame.mixer.music.unpause()
                        self.volume_state = True
                    if self.end_btn.is_clicked(x, y):
                        run = False
                        return not run
                    if self.sound_btn.is_clicked(x, y):
                        self.is_mute = not self.is_mute

                if event.type == pygame.MOUSEBUTTONUP and self.volume_state:
                    self.volume_state = False
                    
                if event.type == pygame.QUIT:
                    run = False
                    return not run
            
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        run = False
                        return not run
        
            if self.volume_state:                   
                self.circle_start = x
                if self.circle_start < 90:
                    self.circle_start = 90
                elif self.circle_start > 360:
                    self.circle_start = 360
                self.volume = (self.circle_start - 90) / (360 - 90)
            
            pygame.display.update()
            