class GameStats():
    """跟蹤遊戲得統計訊息"""

    def __init__(self, ai_settings):
        "初始化統計訊息"
        self.ai_settings = ai_settings
        self.reset_stats()
        #遊戲剛起啟動時處於活動狀態
        self.game_active = False

    def reset_stats(self):
        """初始化在遊戲運行前間肯能變化的統計訊息"""
        self.ships_left = self.ai_settings.ship_limit