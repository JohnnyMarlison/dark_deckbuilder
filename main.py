import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from views.menu.menu_view import MenuView
from visuals.ui.achievement_popup import AchievementToastManager
from audio.sound_manager import sound_manager


class GameWindow(arcade.Window):
    def __init__(self, width: int, height: int, title: str):
        super().__init__(width, height, title)
        self.toast_manager = AchievementToastManager()

    def on_update(self, delta_time: float):
        super().on_update(delta_time)
        self.toast_manager.update(delta_time)

    def on_draw(self):
        super().on_draw()
        self.toast_manager.draw()


def main():
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.show_view(MenuView())
    arcade.run()


if __name__ == "__main__":
    main()
