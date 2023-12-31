from setting import *

class Mana:
    def __init__(self):
        self.max_time = 60 * FPS # 過了60秒，也就是3600幀
        self.total_time = 30 * FPS

    def is_ready(self) -> bool:
        if self.total_time >= self.max_time:
            return True
        else:
            return False

    def update(self):
        self.total_time += 3 # 每次更新都加1，所以total是幀數
        if self.total_time >= self.max_time:
            self.total_time = self.max_time
