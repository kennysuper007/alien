import sys
import pygame

from time import sleep
from bullet import Bullet
from alien import Alien
from game_stats import GameStats


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """響應按鍵"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
    #創建一顆子彈，並將其加入編組bullets中
            fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.k_q:
        sys.exit()

def check_keyup_events(event, ship):
    """響應鬆開"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False

def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets):
    """響應按鍵和屬標事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y):
        """玩家單擊Play按鈕開始遊戲"""
        button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and not stats.game_active:
            #隱藏光標
            pygame.mouse.set_visible(False)
            """重置遊戲統計訊息"""
            stats.reset_stats()
            stats.game_active = True

            #清空外星人子彈列表
            aliens.empty()
            bullets.empty()

            #創建一群新外星人， 讓飛船居中
            create_fleet(ai_settings, screen, ship, aliens)
            ship.center_ship()

def fire_bullet(ai_settings, screen, ship, bullets):
    """创建新子弹，并将其加入到编组bullets中"""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def get_number_aliens_x(ai_settings, alien_width):
    """計算每行可容納多少外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    "計算屏幕可容納多少外星人"
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):

    #創建一個外星人並放在當行
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width

    # 外星人間距為外星人寬度
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen ,ship, aliens):
    """創建外星人群"""
# 創建一個外星人，並計算一行可以容納多少外星人
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    #創建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def update_bullets(ai_settings, screen, ship, aliens, bullets):
    """更新子弹的位置"""
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
    """檢查是否有子彈擊中外星人"""
    # 如果是這樣，就刪除相應的子彈和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
    #刪除現有得子彈並新建一群外星人
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)

def update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button):
    """update images on the screen and flip to the new screen"""
    screen.fill(ai_settings.bg_color)

    # redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # 如果是非活動狀態，就繪製Play按鈕
    if not stats.game_active:
        play_button.draw_button()

    # 讓最近繪製螢幕可見
    pygame.display.flip()


def update_aliens(ai_settings, aliens):
    """更新外星位置"""
    aliens.update()

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
        #響應飛船被外星人撞
        if stats.ships_left > 1:
            stats.ships_left -= 1

            # 清空外星人列表和子彈列表
            aliens.empty()
            bullets.empty()

            # 創建新外星人，將飛船放到屏幕底部中央
            create_fleet(ai_settings, screen, ship, aliens)
            ship.center_ship()

            # 暫停
            sleep(0.5)
        else:
            stats.game_active = False
            pygame.mouse.set_visible(True)

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """檢查是否有外星人位於邊緣，並更新整群外星人位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    #檢查外星人是否到底端
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)

    #檢測外星人與飛船之間的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

def check_fleet_edges(ai_settings, aliens):
    """有外星人到邊緣時採取措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """將整群外星人下一，並改變方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """檢查是否有外星人到達底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像飛船被撞到一樣處理
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break



