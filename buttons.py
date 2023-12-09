class Buttons:
    def __init__(self, img, x, y):
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y

    def is_clicked(self, x: int, y: int):
        if self.rect.collidepoint(x, y): # 傳入的(x,y)是否在self.rect內
            return True
        return False