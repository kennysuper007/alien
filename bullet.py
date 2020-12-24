import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """一個對飛船發射的子彈進行管理的類"""

    def __init__(self, ai_settings, screen, ship):
        """在飛船所處位置創建一個子彈對象"""
        Sprite.__init__(self)
        self.screen = screen
        self.speed = 10

        #在(0,0)創建一個子彈的的矩形，再設置正確位置
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        self.rect1 = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect1.midleft = ship.rect.midleft
        self.rect1.top = ship.rect.top

        self.rect2 = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect2.midright = ship.rect.midright
        self.rect2.top = ship.rect.top

        #存儲用小數表示的子彈位置
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    """更新屏幕"""
    def update(self):
        """向上移動子彈"""
        #更新表示子彈位置的小數值
        self.y -= self.speed_factor
        #更新表示子彈的rect的位置
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上繪製子彈"""
        pygame.draw.rect(self.screen, self.color, self.rect)