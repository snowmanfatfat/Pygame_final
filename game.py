import pygame
import random
import os
import time

from rock import new_rock, rocks, screen
from ground import Ground
from fire import new_fire, fires
from building import new_building, buildings, all_sprites
from power import Power, powers
from explosion import Explosion
from soundset import play_sound, stop_sound
from setting import *
from buttons import Buttons
from player import Player, bullets
from mana import Mana
from ultimate import Ultimate
from boss import Boss, fireballs, fireballs2
from setting_menu import settingmenu

end_img = pygame.transform.scale(pygame.image.load(os.path.join("img/end", f"end.png")),(285, 100))
again_img = pygame.transform.scale(pygame.image.load(os.path.join("img/end", f"again.png")),(285, 100))
mouse_img = pygame.transform.scale(pygame.image.load(os.path.join("img", f"mouse1.png")),(100, 100))
lose_img = pygame.transform.scale(pygame.image.load(os.path.join("img/end/lose/lose0.png")), (WIDTH, HEIGHT))
wins_list = [pygame.transform.scale(pygame.image.load(os.path.join("img/end/wins", f"wins-{i}.png")), (WIDTH, HEIGHT)) for i in range(3)] # 獲勝的畫面有不同圖片
BAR_LENGTH = 200
BAR_HEIGHT = 20

class Game:
    def __init__(self):
        # 設定字型
        self.font_name = os.path.join("ttf","jf-openhuninn-2.0.ttf")
        self.update_rate = 0.9 # 生成補給品的機率
        self.time = 0 # 按下重來後的時間戳記
        self.stop_time_count = 0

        self.speedup = 0 # 速度加快
        self.pause = False # 暫停
        self.running = True # 要不要繼續遊戲
        self.close = False # 掛了
        self.change = True # 背景圖片更換
        self.last_change = time.time() # 上次換背景的時間

        self.score = 0 # 算分
        self.last_score = 0

        # self.show_ready = False # 要不要倒數
        # self.kill_all = False # 要不要通殺

        # button
        self.again_btn = Buttons(again_img, 60, 560)
        self.end_btn = Buttons(end_img, 60, 660)
        self.mouse_img = mouse_img
        self.mouse_img.set_colorkey(WHITE)

        self.lose_img = lose_img
        self.wins_list = wins_list
        self.rand_num3 = 0 # 隨機獲勝畫面
        self.win = False
        
        self.is_shooting = False
        self.shooting_time = 0
        self.gun_time = 0
        
        self.is_boss = False
        self.is_death_expl2 = False
        self.is_death_expl = False
        self.is_ultimate = False
        
        # self.setting_menu = settingmenu
        # self.last_pause = 0
        
    # 顯示文字(時間和分數)
    def draw_text(self, surf, color , text, size, x, y):
        font = pygame.font.Font(self.font_name, size) # size是字體大小
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.centerx = x
        text_rect.top = y
        surf.blit(text_surface, text_rect)

    # 滑鼠圖示
    def draw_mouse(self, surf, x, y):
        x -= self.mouse_img.get_width() / 2
        y -= self.mouse_img.get_height() / 2
        surf.blit(self.mouse_img, (x, y))

    # 畫生命值
    def draw_health(self, surf, hp, x, y, name):
        hp = max(hp, 0)
        bar_lenth = BAR_LENGTH if name == 'player' else BAR_LENGTH*1.8
        fill = (hp/self.player.max_hp) * bar_lenth if name == 'player' else (hp/self.boss.max_hp) * bar_lenth
        outline_rect = pygame.Rect(x, y, bar_lenth, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        if fill > 0.8*bar_lenth:
            pygame.draw.rect(surf, GREEN, fill_rect)
        elif fill > 0.4*bar_lenth:
            pygame.draw.rect(surf, ORANGE, fill_rect)
        else:
            pygame.draw.rect(surf, RED, fill_rect)
        pygame.draw.rect(surf, WHITE, outline_rect, 2) # 若有填數字例如2，則會變成邊框寬度為2的矩形，若沒有填則會變成實心矩形

    def draw_mana_time(self, surf, t, total_t, x, y):
        fill = (t/total_t) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(surf, BLUE, fill_rect)
        pygame.draw.rect(surf, WHITE, outline_rect, 2)

    # 算遊戲時間
    def time_text(self):
        second = self.time // 1000
        minute = str(second // 60).zfill(2)
        second_1 = str(second % 60).zfill(2)
        time_text = f'{minute}:{second_1}'
        return time_text

    # 算準備時間
    def ready_time(self):
        sec = (pygame.time.get_ticks() - self.init_time)//1000
        return sec

    # 顯示暫停畫面
    def draw_pause(self, surf):

        # if not self.show_ready:
        # stop_time = pygame.time.get_ticks() # get_ticks()是回傳從初始化__init__到現在使用get_ticks()的毫秒數
        # self.setting_menu.setting_show(surf)
        # self.pause = False
        # self.stop_time_count += pygame.time.get_ticks() - stop_time # 因為一開始都會停4秒，所以把4秒保留在裡面
        # else:

        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surface, (128, 128, 128, 10), [0, 0, WIDTH, HEIGHT]) # 128,128,128是灰色，160是透明度
        
        # sec = self.ready_time()
        # countdown = str(3 - sec)
        # if sec > 2:
        #     countdown = "GO~"
        
        font = pygame.font.Font(self.font_name, 100)
        text_surf = font.render("按下P鍵繼續遊戲", True, LIGHT_YELLOW)
        text_rect = text_surf.get_rect()
        text_rect.centerx = WIDTH / 2
        text_rect.centery = HEIGHT / 2
        surf.blit(surface, (0, 0))
        surf.blit(text_surf, text_rect)

    # 畫gameover頁面
    def draw_close(self, surf, num=0):
        font = pygame.font.Font(self.font_name, 80)

        text_surf = font.render(f"{int(self.score)}", True, WHITE)
        text_rect = text_surf.get_rect()
        text_rect.centerx = 241
        text_rect.centery = 268
        
        if self.win:
            surf.blit(self.wins_list[num], (0, 0))
            play_sound("sfx\success.wav")
        else:
            surf.blit(self.lose_img, (0, 0))
        surf.blit(text_surf, text_rect)
        
    def get_new_entity(self, group):
        if group == rocks:
            return new_rock
        elif group == fires:
            return new_fire
        elif group == buildings:
            return new_building
        else:
            return lambda: None

    def player_collision(self, group, damage, explosion_type): # 判斷石頭與主角相撞，player用self.player，而石頭就要用rocks，因為石頭是一個list，而player是一個物件
        hits = pygame.sprite.spritecollide(self.player, group, True, pygame.sprite.collide_circle) # 檢測圓形邊界是否相撞，有相撞的話就刪除(True)，且回傳一個list
        for hit in hits: # 檢查單一物件和組之間的碰撞
            if group != fireballs and group != fireballs2:
                new_entity = self.get_new_entity(group)
                new_entity()
            self.player.hp -= damage
            play_sound("sfx/hpdown.wav")
            expl = Explosion(hit.rect.center, explosion_type)
            all_sprites.add(expl)
            if self.player.hp <= 0 and not self.is_death_expl:
                stop_sound("sfx/boss_bgm.wav")
                play_sound("sfx/dead1.wav")
                self.is_death_expl = True
                self.player.hp = 0
                self.death_expl = Explosion(self.player.rect.center, 'player')
                all_sprites.add(self.death_expl)
    
    def boss_collision(self, group, damage, sound, explosion_type):
        hits = pygame.sprite.spritecollide(self.boss, group, True, pygame.sprite.collide_circle)
        for hit in hits: # 檢查單一物件和組之間的碰撞
            play_sound(sound)
            self.boss.hp -= damage
            if self.boss.hp <= 0 and self.boss.is_second and not self.is_death_expl2:
                stop_sound("sfx/boss_bgm.wav")
                play_sound("sfx/dead1.wav")
                self.is_death_expl2 = True
                self.death_expl2 = Explosion(self.boss.rect.center, 'player')
                all_sprites.add(self.death_expl2)
                self.score += 1000
            else:
                expl = Explosion(hit.rect.center, explosion_type)
                all_sprites.add(expl)
        
    def other_collision(self, name, group, sound, explosion_type, volumn=0.5):
        if name == 'ultimate':
                hits = pygame.sprite.spritecollide(self.ultimate, group, True)
        else:
            hits = pygame.sprite.groupcollide(name, group, True, True, pygame.sprite.collide_circle) # 檢查組跟組之間的碰撞
        for hit in hits:
            self.score += 10
            if group != fireballs and group != fireballs2:
                new_entity = self.get_new_entity(group)
                new_entity()
            play_sound(sound, volumn)
            expl = Explosion(hit.rect.center, explosion_type)
            all_sprites.add(expl)
            if group == rocks:
                if random.random() > self.update_rate:
                    pow = Power(hit.rect.center)
                    all_sprites.add(pow)
                    powers.add(pow)
                    
    def calculate_score(self):
        next_score = self.last_score + 500
        if self.score >= next_score:
            for _ in range(1):
                new_rock()
                new_fire()
                new_building()
            if self.speedup >= 10:
                self.speedup = 10
            else:
                self.speedup += 2
            if self.ground.ground_speed >= 10:
                self.ground.ground_speed = 10
            else:
                self.ground.ground_speed += 2
            if self.update_rate <= 0.7:
                self.update_rate = 0.7
            else:
                self.update_rate -= 0.01
            self.last_score += 500

    # 類變量，不用實例化就可以使用，對於不會改變的變量，可以直接寫在類裡面，若改變了則會影響所有實例
    ground = Ground()
    player = Player()
    all_sprites.add(player)
    mana = Mana()
    for i in range(3):
        new_rock()
    for i in range(1):
        new_building()
    for i in range(2):
        new_fire()

    # 遊戲迴圈
    def game_run(self):
        pygame.init()

        clock = pygame.time.Clock()

        self.init_time = pygame.time.get_ticks()
        self.running = True

        while self.running:
            clock.tick(FPS)
            
            while self.close: 
                self.rand_num3 = random.randrange(len(self.wins_list))
                x, y = pygame.mouse.get_pos()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        self.close = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.end_btn.is_clicked(x, y):
                            self.running = False
                            self.close = False

                        if self.again_btn.is_clicked(x, y):
                            pygame.mixer.music.stop()
                            pygame.mixer.music.play()
                            if self.is_boss:
                                self.boss.kill()
                            if self.is_ultimate:
                                self.ultimate.kill()
                            self.__init__()
                            self.mana.__init__() # 沒有實例變量就會搜群類變量
                            self.ground.__init__()
                            self.player.__init__()
                            for g in bullets.sprites():
                                g.kill()
                            for p in powers.sprites():
                                p.kill()
                            for f in fires.sprites():
                                f.kill()
                            for b in buildings.sprites():
                                b.kill()
                            for r in rocks.sprites():
                                r.kill()
                            for fb in fireballs.sprites():
                                fb.kill()
                            for fb2 in fireballs2.sprites():
                                fb2.kill()
                            for _ in range(3):
                                new_rock()
                            for _ in range(1):
                                new_building()
                            for _ in range(2):
                                new_fire()
                            self.init_time = pygame.time.get_ticks()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    
                    now = pygame.time.get_ticks()
                    if event.key == pygame.K_p:
                        self.pause = not self.pause
                        play_sound("sfx/smb_pause.wav")
                        if self.pause:
                            pygame.mixer.music.pause()
                            stop_time = pygame.time.get_ticks() # get_ticks()是回傳從初始化__init__到現在使用get_ticks()的毫秒數
                        else:
                            pygame.mixer.music.unpause()
                            self.stop_time_count += pygame.time.get_ticks() - stop_time # 因為一開始都會停4秒，所以把4秒保留在裡面
                    
                    if event.key == pygame.K_r:
                        self.close = True
                        play_sound("sfx/dead1.wav")
                        pygame.mixer.music.stop()

                    # '''通殺test'''
                    # if event.key == pygame.K_LCTRL:
                    #     if not self.pause:
                    #         self.kill_all = True
                    #         for f in fires.sprites():
                    #             f.kill()
                    #             self.score += 10
                    #         for r in rocks.sprites():
                    #             r.kill()
                    #             self.score += 10
                    #         for b in buildings.sprites():
                    #             b.kill()
                    #             self.score += 10
                    #         for fb in fireballs.sprites():
                    #             fb.kill()
                    #             self.score += 10
                    #         for fb2 in fireballs2.sprites():
                    #             fb2.kill()
                    #             self.score += 10

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.pause:
                        if event.button == 1:
                            self.player.shoot()
                            if self.player.gun == 2:
                                self.shooting_time = self.time
                                self.is_shooting = True
                        elif event.button == 3 and self.mana.is_ready():
                            play_sound("sfx/smb3_raccoon_transform.wav")
                            self.mana.total_time = 0
                            self.ultimate = Ultimate(self.player.rect.centerx, self.player.rect.centery)
                            self.is_ultimate = True
                            all_sprites.add(self.ultimate)
                            
                if event.type == pygame.MOUSEBUTTONUP:
                    if not self.pause:
                        if event.button == 1:
                            self.is_shooting = False

            # 倒數畫面
            # if self.show_ready:
            #     play_sound("sfx\countdown.wav")
            #     self.pause = True
            #     ready_time = self.ready_time()
            #     if ready_time >= 4:
            #         self.show_ready = False
            #         self.pause = False
            #         self.stop_time_count = 4 * 1000
            
            # 更新遊戲
            if not self.pause:
                screen.fill(BLACK)
                self.ground.draw(screen)
                all_sprites.draw(screen)
                
                self.draw_health(screen, self.player.hp, 50, 20, 'player')
                self.draw_mana_time(screen, self.mana.total_time, self.mana.max_time, 50, 50)
                self.draw_text(screen, BLACK, self.time_text(), 40, WIDTH / 2 - 10, 15)
                self.draw_text(screen, BLACK, str(int(self.score)).zfill(6), 40, WIDTH - 150, 15) # 分數轉文字再補齊6位數
                
                x, y = pygame.mouse.get_pos()
                x = max(0, min(x, WIDTH))
                y = max(0, min(y, HEIGHT))
                pygame.event.set_grab(True) # 限制滑鼠在視窗內
                pygame.mouse.set_visible(False)
                self.draw_mouse(screen, x, y)
                
                self.time = pygame.time.get_ticks() - self.stop_time_count - self.init_time # self.init_time是遊戲開始的時間戳記，不然pygame.time.get_ticks()會從第一次init開始算
                all_sprites.update()
                self.ground.update()
                self.mana.update()
                self.score += 0.1
                self.calculate_score()
                if self.player.gun == 2:
                    if self.time - self.gun_time > 3000:
                        self.player.gun = 1
                        self.gun_time = self.time
                    if self.is_shooting and self.time - self.shooting_time > 50:
                        self.shooting_time = self.time
                        self.player.shoot()
            
                if self.score >= 1000 and not self.is_boss:
                    self.is_boss = True
                    self.boss = Boss()
                    all_sprites.add(self.boss)
                    self.boss_time = self.time
                    pygame.mixer.music.pause()
                    play_sound("sfx/boss_bgm.wav",0.4,-1)
                    
                if self.is_boss:
                    if self.boss.is_second and self.boss.hp <= 0:
                        self.boss_dead = True
                        self.draw_text(screen, RED, "DEATH", 80, self.boss.rect.centerx+20, self.boss.rect.top-30)
                    else:
                        self.draw_health(screen, self.boss.hp, 1000, self.boss.rect.top-20 , 'boss')
                        
                    self.boss_collision(bullets, 100, "sfx/smb_breakblock.wav", 'lg')
                    
                    hits = pygame.sprite.spritecollide(self.boss, rocks, True, pygame.sprite.collide_circle) # False表示buildings不刪除
                    for hit in hits:
                        expl = Explosion(hit.rect.center, 'sm')
                        all_sprites.add(expl)
                        play_sound("sfx/smb_bump.wav")
                        new_rock()
                        
                    if self.time - self.boss_time > 500 and self.boss.hp > 0:
                        self.boss_time = self.time
                        self.boss.attack()
                          
                # 更換背景
                if (self.time//1000 % 10 == 0 and self.time//1000 != 0)  and self.change:
                    self.ground.change_ground()
                    self.last_change = time.time()
                    self.change = False
                # 防止重複更換，因為是取整數，所以要加上一個時間限制，不然小數點時間時會一直更換
                if not self.change and (time.time() - self.last_change) > 1: # time()回傳的是秒
                    self.change = True

                for f in fires.sprites():
                    f.speed_fire = SPEED + self.speedup
                for b in buildings.sprites():
                    b.speed_build = SPEED + self.speedup
                for fb in fireballs.sprites():
                    fb.speed = FIREATK_SPEED + self.speedup
                for fb2 in fireballs2.sprites():
                    fb2.speed = FIREATK_SPEED + self.speedup

                self.player_collision(rocks, 10, 'lg') 
                self.player_collision(fires, 10, 'lg') # 判斷火與主角相撞
                self.player_collision(buildings, 20, 'lg') # 判斷建築物與主角相撞
                self.player_collision(fireballs, 15, 'lg') # 判斷火球與主角相撞
                self.player_collision(fireballs2, 30, 'lg') # 判斷火球2與主角相撞
            
                if self.is_ultimate:
                    self.other_collision('ultimate', rocks, "sfx/smb_breakblock.wav", 'lg')
                    self.other_collision('ultimate', buildings, "sfx/smb_breakblock.wav", 'lg')
                    self.other_collision('ultimate', fires, "sfx/fire_clear.wav", 'lg', 0.8)
                    self.other_collision('ultimate', fireballs, "sfx/fire_clear.wav", 'lg', 0.8)
                    self.other_collision('ultimate', fireballs2, "sfx/fire_clear.wav", 'lg', 0.8)
                    if not self.ultimate.alive():
                        self.is_ultimate = False
            
                self.other_collision(bullets, rocks, "sfx/smb_breakblock.wav", 'sm')
                self.other_collision(bullets, fires, "sfx/fire_clear.wav", 'sm', 0.8)
                self.other_collision(bullets, fireballs, "sfx/fire_clear.wav", 'sm', 0.8)
                self.other_collision(bullets, fireballs2, "sfx/fire_clear.wav", 'sm', 0.8)
            
                # 判斷子彈被建築擋住
                hits = pygame.sprite.groupcollide(bullets, buildings, True, False, pygame.sprite.collide_circle) # False表示buildings不刪除
                for hit in hits:
                    expl = Explosion(hit.rect.center, 'sm')
                    all_sprites.add(expl)
                    play_sound("sfx/smb_bump.wav")
            
                # 判斷火球被建築擋住
                hits = pygame.sprite.groupcollide(fireballs, buildings, True, False, pygame.sprite.collide_circle)
                for hit in hits:
                    expl = Explosion(hit.rect.center, 'sm')
                    all_sprites.add(expl)
                    play_sound("sfx/smb_bump.wav")
                    
                # 判斷火球2被建築擋住
                hits = pygame.sprite.groupcollide(fireballs2, buildings, True, False, pygame.sprite.collide_circle)
                for hit in hits:
                    expl = Explosion(hit.rect.center, 'sm')
                    all_sprites.add(expl)
                    play_sound("sfx/smb_bump.wav")

                # 判斷寶物與主角相撞
                hits = pygame.sprite.spritecollide(self.player, powers, True)
                for hit in hits:
                    if hit.type == 'blood':
                        play_sound("sfx/smb_1-up.wav")
                        if self.player.hp > 0:
                            self.player.hp += 30
                            self.player.hp = min(self.player.hp, 100)
                    elif hit.type == 'gun':
                        play_sound("sfx/smb_1-up.wav")
                        self.player.gunup()
                        self.gun_time = self.time
                    elif hit.type == 'mana':
                        play_sound("sfx/smb_1-up.wav")
                        self.mana.total_time += (self.mana.max_time * 0.2)
                        if self.mana.total_time >= self.mana.max_time:
                            self.mana.total_time = self.mana.max_time
                
                # 房子跟火不要撞一起
                hits = pygame.sprite.groupcollide(buildings, fires, False, True)
                for hit in hits:
                    new_fire()

                # 讓動畫播完再結束遊戲
                if (self.player.hp <= 0) and not (self.death_expl.alive()):
                    self.close = True
                    # self.show_ready = True
                elif self.is_boss:
                    if self.boss.hp <= 0 and self.boss.is_second and not (self.death_expl2.alive()):
                        self.close = True
                        # self.show_ready = True
                        self.win = True

                # # 通殺
                # if self.kill_all:
                #     self.player.draw_kill_all(screen)
                #     if self.player.k_range == 100:
                #         self.kill_all = False    
            
            if self.pause:
                pygame.event.set_grab(False)
                pygame.mouse.set_visible(True)
                self.draw_pause(screen)
                # self.setting_menu.setting_show(screen)
                # self.pause = False
            
            if self.close:
                pygame.event.set_grab(False)
                pygame.mouse.set_visible(True)
                if self.win:
                    self.draw_close(screen, self.rand_num3)
                else:
                    self.draw_close(screen)     
            
            pygame.display.update()
        pygame.draw.rect(screen, BLACK, [0, 0, WIDTH, HEIGHT])
        