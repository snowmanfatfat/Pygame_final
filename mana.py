from setting import *

class Mana:
    def __init__(self):
        self.max_time = 60 * FPS # 過了60秒，也就是3600幀
        self.total_time = 60 * FPS
        # self.activated = False

    def is_ready(self) -> bool:
        if self.total_time >= self.max_time:
            return True
        else:
            return False

    def update(self):
        self.total_time += 1 # 每次更新都加1，所以total是幀數
        if self.total_time >= self.max_time:
            self.total_time = self.max_time

        # key_pressed = pygame.key.get_pressed()
        # if key_pressed[pygame.K_LSHIFT] and self.is_ready():
        #     play_sound("sfx\smb3_raccoon_transform.wav")
        #     self.activated = True
        #     self.total_time = 0

        # # 效果時間12秒
        # if self.total_time >= (self.max_time // 5):
        #     self.activated = False
