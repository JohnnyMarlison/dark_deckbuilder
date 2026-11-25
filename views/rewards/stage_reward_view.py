import random
import arcade
from config import SCREEN_WIDTH, BG_DARK, PANEL_DARK, BORDER_GOLD, TEXT_PARCHMENT, TEXT_MUTED
from core.run_state import RunState
from visuals.ui.icons import draw_card_icon
from visuals.ui.achievement_popup import AchievementToastManager
from visuals.ui.text_cache import TextCache

BUFF_POOL = (
    ("neutral", "damage", 3, "Нейтральная атака (+3)", "Увеличивает урон всех нейтральных атакующих карт на +3 до конца похода.", "Атака"),
    ("neutral", "heal", 3, "Нейтральное лечение (+3)", "Увеличивает исцеление всех нейтральных лечащих карт на +3 до конца похода.", "Исцеление"),
    ("neutral", "block", 2, "Нейтральная защита (+2)", "Увеличивает броню всех нейтральных защитных карт на +2 до конца похода.", "Защита"),
    ("hero", "damage", 3, "Мастерство героя: Атака (+3)", "Увеличивает урон всех личных атакующих карт героя на +3 до конца похода.", "Атака"),
    ("hero", "heal", 3, "Мастерство героя: Лечение (+3)", "Увеличивает исцеление всех личных лечащих карт героя на +3 до конца похода.", "Исцеление"),
    ("hero", "block", 2, "Мастерство героя: Защита (+2)", "Увеличивает броню всех личных защитных карт героя на +2 до конца похода.", "Защита"),
)


class StageRewardView(arcade.View):
    """Экран выбора награды после победы над рядовым врагом (Раунды 1 и 2)."""

    def __init__(self, run: RunState):
        super().__init__()
        self.run = run
        self.ui_text = TextCache()
        self.toast_manager = AchievementToastManager()

        self.buff_scope, self.buff_stat, self.buff_val, buff_title, buff_desc, buff_icon = random.choice(BUFF_POOL)

        self.options = (
            {
                "id": "full_heal",
                "title": "Источник жизни",
                "desc": "Полностью восстанавливает ваше здоровье до максимума.",
                "icon": "Исцеление",
                "x": 460,
            },
            {
                "id": "max_hp",
                "title": "Закалка плоти",
                "desc": "Увеличивает макс. здоровье на 10–12% и исцеляет 10–15% здоровья.",
                "icon": "Защита",
                "x": 960,
            },
            {
                "id": "deck_buff",
                "title": buff_title,
                "desc": buff_desc,
                "icon": buff_icon,
                "x": 1460,
            },
        )
        self.hovered_idx = -1

    def on_show_view(self):
        arcade.set_background_color(BG_DARK)

    def on_update(self, delta_time: float):
        self.toast_manager.update(delta_time)

    def on_draw(self):
        self.clear()
        self.ui_text.draw("ПОБЕДА В СХВАТКЕ!", SCREEN_WIDTH / 2, 950, BORDER_GOLD, 38, bold=True, anchor_x="center")
        self.ui_text.draw(
            f"Выберите награду перед следующим раундом   •   Текущее HP: {self.run.hero.hp} / {self.run.hero.max_hp}",
            SCREEN_WIDTH / 2, 895, TEXT_PARCHMENT, 18, anchor_x="center"
        )

        for idx, opt in enumerate(self.options):
            is_hov = (idx == self.hovered_idx)
            cx, cy = opt["x"], 530
            w, h = 420, 460

            arcade.draw_rect_filled(arcade.XYWH(cx, cy, w, h), (30, 28, 38) if is_hov else PANEL_DARK)
            arcade.draw_rect_outline(arcade.XYWH(cx, cy, w, h), arcade.color.YELLOW if is_hov else BORDER_GOLD, 3.5 if is_hov else 2)

            arcade.draw_circle_filled(cx, cy + 120, 48, (42, 36, 30))
            arcade.draw_circle_outline(cx, cy + 120, 48, BORDER_GOLD, 2)
            draw_card_icon(opt["icon"], cx, cy + 120, size=34)

            self.ui_text.draw(
                opt["title"], cx, cy + 25, BORDER_GOLD, 20,
                width=w - 36, align="center", bold=True, anchor_x="center", anchor_y="center", multiline=True
            )
            self.ui_text.draw(
                opt["desc"], cx, cy - 75, TEXT_PARCHMENT, 16,
                width=w - 50, align="center", anchor_x="center", anchor_y="center", multiline=True
            )
            self.ui_text.draw("Нажмите, чтобы выбрать", cx, cy - 190, TEXT_MUTED, 14, anchor_x="center")

        self.toast_manager.draw()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.hovered_idx = -1
        for idx, opt in enumerate(self.options):
            if opt["x"] - 210 <= x <= opt["x"] + 210 and 300 <= y <= 760:
                self.hovered_idx = idx
                break

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button != arcade.MOUSE_BUTTON_LEFT or self.hovered_idx == -1:
            return

        chosen = self.options[self.hovered_idx]["id"]
        if chosen == "full_heal":
            self.run.apply_full_heal()
        elif chosen == "max_hp":
            self.run.apply_max_hp_boost()
        elif chosen == "deck_buff":
            self.run.apply_deck_buff(self.buff_scope, self.buff_stat, self.buff_val)

        from views.battle.battle_view import BattleView
        self.window.show_view(BattleView(self.run))
