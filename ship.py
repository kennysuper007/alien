import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen):

        #初始化飛船並設置其初始位置
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #加載飛船圖像並獲取其外接矩形
        self.image = pygame.image.load('figures\images\ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #將每艘飛船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom


        #將飛船屬性center中存儲小數值
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

        #移動標誌
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """根據移動標誌調整飛船位置"""
        #更新飛船的center值，而不是rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.centerx -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.centery -= self.ai_settings.ship_speed_factor

        #根據self.center更新rect對象
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def blitme(self):
            """在指定位置繪製飛船"""
            self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """讓飛船在屏幕上居中"""
        self.center = self.screen_rect.centerx
