import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """表示單個外星人的類"""
    def __init__(self, ai_settings, screen):
        """初始外星人起始位置"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings


        #載入外星人圖片
        self.image = pygame.image.load('figures/images/ET.png')
        self.image = pygame.transform.scale(self.image, (80, 60))
        self.rect = self.image.get_rect()

        #每個外星人最初都在螢幕左上角附近
        self.rect.x = 0
        self.rect.y = 0

        #存儲外星人位置
        self.x = float(self.rect.x)

    def check_edges(self):
        """如果外星人位於屏幕邊緣，返回TRUE"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """向右移動外星人"""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x


    def blitme(self):
        """在指定位置繪製外星人"""
        self.screen.blit(self.image, self.rect)
