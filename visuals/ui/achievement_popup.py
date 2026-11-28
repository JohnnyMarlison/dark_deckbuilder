import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BORDER_GOLD, TEXT_PARCHMENT, TEXT_MUTED
from core.records import PENDING_ACHIEVEMENT_POPUPS
from visuals.ui.icons import draw_card_icon
from visuals.ui.text_cache import TextCache

class AchievementToastManager:
    """Менеджер всплывающих уведомлений о получении достижений в правом нижнем углу."""

    def __init__(self):
        self.current: dict | None = None
        self.timer = 0.0
        self.x = SCREEN_WIDTH + 240
        self.y = SCREEN_HEIGHT - 88
        self.width = 430
        self.height = 105
        self.ui_text = TextCache()

    def update(self, dt: float):
        if self.current is None and PENDING_ACHIEVEMENT_POPUPS:
            self.current = PENDING_ACHIEVEMENT_POPUPS.pop(0)
            self.timer = 3.2
            self.x = SCREEN_WIDTH + 240

        if self.current is not None:
            self.timer -= dt
            target_x = SCREEN_WIDTH - 245 if self.timer > 0.45 else SCREEN_WIDTH + 250
            self.x += (target_x - self.x) * min(1.0, dt * 11.0)
            if self.timer <= 0:
                self.current = None

    def draw(self):
        if self.current is None:
            return

        arcade.draw_rect_filled(arcade.XYWH(self.x, self.y, self.width, self.height), (20, 18, 28, 245))
        arcade.draw_rect_outline(arcade.XYWH(self.x, self.y, self.width, self.height), BORDER_GOLD, 2.5)

        # Иконка достижения слева
        icon_x = self.x - self.width / 2 + 48
        arcade.draw_circle_filled(icon_x, self.y, 30, (42, 36, 28))
        arcade.draw_circle_outline(icon_x, self.y, 30, BORDER_GOLD, 2)
        draw_card_icon(self.current.get("icon", "Атака"), icon_x, self.y, size=22)

        # Текст уведомления
        text_x = icon_x + 45
        self.ui_text.draw("ДОСТИЖЕНИЕ ПОЛУЧЕНО!", text_x, self.y + 28, BORDER_GOLD, 12, bold=True, anchor_x="left")
        self.ui_text.draw(self.current["title"], text_x, self.y + 4, TEXT_PARCHMENT, 15, bold=True, anchor_x="left")
        self.ui_text.draw(
            self.current["desc"], text_x, self.y - 24, TEXT_MUTED, 12,
            width=310, anchor_x="left", anchor_y="center", multiline=True
        )
