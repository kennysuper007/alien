import pygame

from pygame.sprite import Group
import game_functions as gf
from settings import Settings
from ship import Ship
from alien import Alien
from game_stats import GameStats
from button import Button

def run_game():
# 初始化遊戲並創建對象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    bg_color = (0, 0, 0)
#創建Play按鈕
    play_button = Button(ai_settings, screen, "Play")

#創建外星人
    alien = Alien(ai_settings, screen)

#創建一艘飛船
    ship = Ship(ai_settings, screen)

#創建一個子彈的編組
    bullets = Group()

#創建一個外星人編組
    aliens = Group()

#創建外星人群
    gf.create_fleet(ai_settings, screen ,ship, aliens)

#創建一個用於存儲遊戲統計訊息實例
    stats = GameStats(ai_settings)

# 开始游戏的主循环
    while True:
        gf.check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button)

run_game()

