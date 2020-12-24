class Settings():
    """存儲所有設置的類"""
    def __init__(self):
        """初始化油遊戲設置"""
        #屏幕設置
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (230, 230, 230)

        #飛船的設置
        self.ship_speed_factor = 3
        self.ship_limit = 3

        #外星人設置
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 50

        #fleet_direction為一表示向右移，為-1表示左移
        self.fleet_direction = 1


        #子彈設置
        self.bullet_speed_factor = 3
        self.bullet_width = 100
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 300

