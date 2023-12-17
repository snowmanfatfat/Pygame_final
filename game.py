import pygame
import random
import os
import time

from setting_menu import SettingMenu
from rock import new_rock, rocks, screen
from ground import Ground
from fire import new_fire, fires
from building import new_building, buildings, all_sprites
from power import Power, powers
from explosion import Explosion
from soundset import play_sound
from setting import *
from buttons import Buttons
from player import Player, bullets
from mana import Mana
from ultimate import Ultimate, WaterPower
from boss import Boss, fireballs

end_img = pygame.transform.scale(pygame.image.load(os.path.join("img/end", f"end.png")),(285, 100))
again_img = pygame.transform.scale(pygame.image.load(os.path.join("img/end", f"again.png")),(285, 100))
mouse_img = pygame.transform.scale(pygame.image.load(os.path.join("img", f"mouse.png")),(80, 80))
tips_list = [pygame.transform.scale(pygame.image.load(os.path.join("img/end/tips", f"tips-{i}.png")), (WIDTH, HEIGHT)) for i in range(23)] # 死掉的畫面有不同圖片
talk_list = ["本喵喘口氣 . . . 喵呼 . . .", # 暫停的對話
            "本喵喝口水，休息一下 . . . ",
            "好累 . . . 突然好想吃罐罐 . . . ",
            "喵呼 . . . 累得跟貓一樣 . . . ",
            "呼嚕 . . . 呼嚕 . . . ",
            "休息是為了吃更多罐罐喵 . . . "]
wins_list = [pygame.transform.scale(pygame.image.load(os.path.join("img/end/wins", f"wins-{i}.png")), (WIDTH, HEIGHT)) for i in range(3)] # 獲勝的畫面有不同圖片
BAR_LENGTH = 200
BAR_HEIGHT = 20

class Game:
    def __init__(self):
        # 設定字型
        self.font_name = os.path.join("ttf","HanyiSentyPagoda.ttf")
        self.update_rate = 0.5 # 生成補給品的機率
        self.time = 0 # 按下重來後的時間戳記
        self.stop_time_count = 0

        self.speedup = 0 # 速度加快
        self.pause = False # 暫停
        self.running = True # 要不要繼續遊戲
        self.close = False # 掛了
        self.change = True # 背景圖片更換
        self.last_change = time.time() # 上次換背景的時間

        self.score = 0 # 算分

        self.show_ready = True # 要不要倒數
        self.kill_all = False # 要不要通殺

        # button
        self.end_btn = Buttons(end_img, 95, 680)  # x, y, width, height
        self.again_btn = Buttons(again_img, 95, 580)
        self.mouse_img = mouse_img
        
        self.talk_list = talk_list
        self.rand_num = 0 # 隨機對話
        self.tips_list = tips_list
        self.rand_num2 = 0 # 隨機死亡畫面
        self.wins_list = wins_list
        self.rand_num3 = 0 # 隨機獲勝畫面
        
        self.is_shooting = False
        self.shooting_time = 0
        self.gun_time = 0
        
        self.ultimate = Ultimate()
        self.boss = Boss()
        self.is_boss = False
        
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
    def draw_health(self, surf, hp, x, y):
        hp = max(hp, 0)
        fill = (hp/100) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        if fill > (80/100)*BAR_LENGTH:
            pygame.draw.rect(surf, GREEN, fill_rect)
        elif (79/100)*BAR_LENGTH > fill > (40/100)*BAR_LENGTH :
            pygame.draw.rect(surf, ORANGE, fill_rect)
        else:
            pygame.draw.rect(surf, RED, fill_rect)

        pygame.draw.rect(surf, WHITE, outline_rect, 2) # 若有填數字例如2，則會變成邊框寬度為2的矩形，若沒有填則會變成實心矩形

    def draw_mana_time(self, surf, t, total_t, x, y):
        colorlist = [(111, 159, 255), # 顏色漸層 這是藍色
                     (94, 137, 255),
                     (64, 94, 152),
                     (43, 62, 101),
                     (15, 22, 36)]
        fill = (t/total_t) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        if fill == BAR_LENGTH:
            pygame.draw.rect(surf, (240, 240, 240), fill_rect)
        elif fill >= (80/100)*BAR_LENGTH:
            pygame.draw.rect(surf, colorlist[0], fill_rect)
        elif fill >= (60/100)*BAR_LENGTH :
            pygame.draw.rect(surf, colorlist[1], fill_rect)
        elif fill >= (40/100)*BAR_LENGTH :
            pygame.draw.rect(surf, colorlist[2], fill_rect)
        elif fill >= (20/100)*BAR_LENGTH :
            pygame.draw.rect(surf, colorlist[3], fill_rect)
        else:
            pygame.draw.rect(surf, colorlist[4], fill_rect)
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
    def draw_pause(self, surf, num=0, size_big=80, size_small=40):
        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surface, (128, 128, 128, 160), [0, 0, WIDTH, HEIGHT]) # 128,128,128是灰色，160是透明度
        
        font = pygame.font.Font(self.font_name, size_big)
        text_surf_1 = font.render(self.talk_list[num], True, WHITE) # True是開啟反鋸齒
        text_rect_1 = text_surf_1.get_rect()
        text_rect_1.centerx = WIDTH / 2
        text_rect_1.top = HEIGHT / 2 - 90

        font = pygame.font.Font(self.font_name, size_small)
        text_surf_2 = font.render("按下 p 鍵可繼續遊戲", True, WHITE) 
        text_rect_2 = text_surf_2.get_rect()
        text_rect_2.centerx = WIDTH / 2
        text_rect_2.top = HEIGHT / 2 + 60

        if not self.show_ready:
            surf.blit(surface, (0, 0))
            surf.blit(text_surf_1, text_rect_1)
            surf.blit(text_surf_2, text_rect_2)
            self.stop_time = pygame.time.get_ticks() # get_ticks()是回傳從初始化__init__到現在使用get_ticks()的毫秒數
            if self.setting_menu.setting_show(screen):
                self.pause = False
                self.stop_time_count += pygame.time.get_ticks() - self.stop_time # 因為一開始都會停4秒，所以把4秒保留在裡面
        else:
            sec = self.ready_time()
            countdown = str(3 - sec)
            if sec > 2:
                countdown = "GO!"
            font = pygame.font.Font(self.font_name, 400)
            text_surf = font.render(countdown, True, WHITE)
            text_rect = text_surf.get_rect()
            text_rect.centerx = WIDTH / 2 - 20
            text_rect.top = HEIGHT / 2 - 320
            surf.blit(surface, (0, 0))
            surf.blit(text_surf, text_rect)

    # 畫gameover頁面
    def draw_close(self, surf, num=0):
        font = pygame.font.Font(self.font_name, 60)
        text_surf_1 = font.render("本次挑戰分數", True, RED1)
        text_rect_1 = text_surf_1.get_rect()
        text_rect_1.left = 60
        text_rect_1.top = 380

        text_surf_2 = font.render(f"「{self.score}分」", True, RED1)
        text_rect_2 = text_surf_2.get_rect()
        text_rect_2.centerx = text_rect_1.centerx
        text_rect_2.top = 480
        
        if self.player.health <= 0:
            surf.blit(self.tips_list[num], (0, 0))
        elif self.score >= 10:
            surf.blit(self.wins_list[num], (0, 0))
        surf.blit(text_surf_1, text_rect_1)
        surf.blit(text_surf_2, text_rect_2)
        surf.blit(self.again_btn.img, (100, 580))
        surf.blit(self.end_btn.img, (100, 680))
        
    def get_new_entity(self, group):
        if group == rocks:
            return new_rock
        elif group == fires:
            return new_fire
        elif group == buildings:
            return new_building
        else:
            return lambda: None

    def player_collision(self, group, damage, sound, explosion_type): # 判斷石頭與主角相撞，player用self.player，而石頭就要用rocks，因為石頭是一個list，而player是一個物件
        hits = pygame.sprite.spritecollide(self.player, group, True, pygame.sprite.collide_circle) # 檢測圓形邊界是否相撞，有相撞的話就刪除(True)，且回傳一個list
        for hit in hits: # 檢查單一物件和組之間的碰撞
            new_entity = self.get_new_entity(group)
            new_entity()
            play_sound(sound)
            self.player.health -= damage
            expl = Explosion(hit.rect.center, explosion_type)
            all_sprites.add(expl)
            if self.player.health <= 0:
                self.player.health = 0
                self.death_expl = Explosion(self.player.rect.center, 'player')
                all_sprites.add(self.death_expl)
                play_sound("sfx\dead1.wav")
                
    def calculate_score(self):
        if (self.score % 100 == 0) and (self.score != 0):
            for _ in range(1):
                new_rock()
                new_fire()
                new_building()
            self.speedup += 2
            self.ground.ground_speed += 2
            self.update_rate -= 0.02
        
    def other_collision(self, name, group, sound):
        if name == self.ultimate:
            hits = pygame.sprite.spritecollide(self.ultimate, group, True)
        else:
            hits = pygame.sprite.groupcollide(name, group, True, True, pygame.sprite.collide_circle) # 檢查組跟組之間的碰撞
        for hit in hits:
            self.score += 1
            new_entity = self.get_new_entity(group)
            new_entity()
            play_sound(sound)
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            self.calculate_score()
            if group == rocks:
                if random.random() > self.update_rate:
                    pow = Power(hit.rect.center)
                    all_sprites.add(pow)
                    powers.add(pow)

    # 類變量，不用實例化就可以使用，對於不會改變的變量，可以直接寫在類裡面，若改變了則會影響所有實例
    setting_menu = SettingMenu()
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

            while self.close: # 掛了的時候才會變成True
                pygame.event.set_grab(False)
                
                self.rand_num3 = random.randrange(len(self.wins_list))
                self.rand_num2 = random.randrange(len(self.tips_list))
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
                            self.boss.kill()
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
                        
                    if event.key == pygame.K_p:
                        self.pause = not self.pause
                        self.rand_num = random.randrange(len(self.talk_list))
                        if self.pause == True:
                            play_sound("sfx/smb_pause.wav")

                    '''通殺test'''
                    if event.key == pygame.K_LCTRL:
                        if not self.pause:
                            self.kill_all = True
                            f_num, r_num = 0, 0
                            for f in fires.sprites():
                                f_num += 1
                                f.kill()
                                self.score += 1
                            for r in rocks.sprites():
                                r_num += 1
                                r.kill()
                                self.score += 1
                            for b in buildings.sprites():
                                b.kill()
                                self.score += 1
                            for fb in fireballs.sprites():
                                fb.kill()
                                self.score += 1
                            self.boss.kill()
                            for _ in range(f_num):
                                new_fire()
                            for _ in range(r_num):
                                new_rock()
                            for _ in range(1):
                                new_building()
                            
                    if event.key == pygame.K_r:
                        self.close = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.pause:
                        if event.button == 1:
                            self.player.shoot()
                            if self.player.gun == 2:
                                self.shooting_time = self.time
                                self.is_shooting = True
                        elif event.button == 3 and self.mana.is_ready():
                            play_sound("sfx\smb3_raccoon_transform.wav")
                            # self.mana.activated = True
                            self.mana.total_time = 0
                            self.ultimate = Ultimate(self.player.rect.centerx, self.player.rect.centery)
                            waterpower = WaterPower(self.player.rect.centerx, self.player.rect.centery)
                            all_sprites.add(self.ultimate)
                            
                if event.type == pygame.MOUSEBUTTONUP:
                    if not self.pause:
                        if event.button == 1:
                            self.is_shooting = False
              
            # 畫面顯示
            screen.fill(BLACK)
            self.ground.draw(screen)
            all_sprites.draw(screen)
            if self.ultimate.alive():
                waterpower.draw(screen)

            # 倒數畫面
            if self.show_ready:
                play_sound("sfx\countdown.wav")
                self.pause = True
                ready_time = self.ready_time()
                if ready_time >= 4:
                    self.show_ready = False
                    self.pause = False
                    self.stop_time_count = 4 * 1000

            # 更新遊戲
            if self.running and not self.pause:
                self.time = pygame.time.get_ticks() - self.stop_time_count - self.init_time # self.init_time是遊戲開始的時間戳記，不然pygame.time.get_ticks()會從第一次init開始算
                all_sprites.update()
                self.ground.update()
                self.mana.update()
                if self.player.gun == 2:
                    if self.time - self.gun_time > 5000:
                        self.player.gun = 1
                        self.gun_time = self.time
                    if self.is_shooting and self.time - self.shooting_time > 50:
                        self.shooting_time = self.time
                        self.player.shoot()
            
                if self.score >= 50 and not self.is_boss:
                    self.is_boss = True
                    all_sprites.add(self.boss)
                    self.boss_time = self.time
                if self.is_boss:
                    if self.time - self.boss_time > 500 and self.boss.hp > 0:
                        self.boss_time = self.time
                        self.boss.attack() 
                
                # 更換背景，2分鐘換一次
            if (self.time//1000 % 5 == 0 and self.time//1000 != 0)  and self.change:
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

            self.player_collision(rocks, 34, "sfx/smb_bump.wav", 'sm') 
            self.player_collision(fires, 17, "sfx/smb_bump.wav", 'sm') # 判斷火與主角相撞
            self.player_collision(buildings, 17, "sfx/smb_bump.wav", 'sm') # 判斷建築物與主角相撞
            
            self.other_collision(self.ultimate, rocks, "sfx/smb_breakblock.wav")
            self.other_collision(self.ultimate, fires, "sfx/smb_bowserfire.wav")
            self.other_collision(self.ultimate, buildings, "sfx/smb_breakblock.wav")
            
            self.other_collision(bullets, rocks, "sfx/smb_breakblock.wav")
            self.other_collision(bullets, fires, "sfx/smb_bowserfire.wav")
            
            # 判斷子彈被建築擋住
            hits = pygame.sprite.groupcollide(bullets, buildings, True, False) # False表示buildings不刪除
            for hit in hits:
                play_sound("sfx/smb_bump.wav")

            # 判斷寶物與主角相撞
            hits = pygame.sprite.spritecollide(self.player, powers, True)
            for hit in hits:
                if hit.type == 'blood':
                    play_sound("sfx/smb_1-up.wav")
                    if self.player.health > 0:
                        self.player.health += 34
                        self.player.health = min(self.player.health, 100)
                elif hit.type == 'gun':
                    play_sound("sfx/smb_powerup_appears.wav")
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
            if (self.player.health <= 0) and not (self.death_expl.alive()) : # or self.score>=1000
                self.close = True
                self.show_ready = True

            # 防護罩
            # self.player.protected = self.protect.activated
            # if self.protect.activated:
            #     self.player.draw_protect(screen)
            #     self.player.p_trans -= 0.1 # 減去透明度
            # else:
            #     self.player.p_trans = 90

            # 通殺
            if self.kill_all:
                self.player.draw_kill_all(screen)
                if self.player.k_range == 100:
                    self.kill_all = False
            
            self.draw_health(screen, self.player.health, 50, 20)
            self.draw_mana_time(screen, self.mana.total_time, self.mana.max_time, 50, 50)
            self.draw_text(screen, BLACK, self.time_text(), 40, WIDTH / 2 - 10, 15)
            self.draw_text(screen, BLACK, str(self.score).zfill(6), 40, WIDTH - 150, 15) # 分數轉文字再補齊6位數
            
            # 滑鼠控制
            if self.pause:
                pygame.event.set_grab(False)
                pygame.mouse.set_visible(True)
                self.draw_pause(screen, self.rand_num)
            else:
                x, y = pygame.mouse.get_pos()
                x = max(0, min(x, WIDTH))
                y = max(0, min(y, HEIGHT))
                pygame.event.set_grab(True) # 限制滑鼠在視窗內
                if not self.close:
                    pygame.mouse.set_visible(False)
                    self.draw_mouse(screen, x, y)
            
            if self.close:
                pygame.event.set_grab(False)
                pygame.mouse.set_visible(True)
                self.draw_close(screen, self.rand_num2)

            pygame.display.update()

        # pygame.quit()
        