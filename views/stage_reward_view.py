import random
import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BG_DARK, PANEL_DARK, BORDER_GOLD, TEXT_PARCHMENT, TEXT_MUTED
from core.run_state import RunState
from visuals.icons import draw_card_icon
from visuals.achievement_popup import AchievementToastManager


class StageRewardView(arcade.View):
    """Экран выбора награды после победы над врагом 1-го или 2-го уровня."""

    def __init__(self, run: RunState):
        super().__init__()
        self.run = run
        self.toast_manager = AchievementToastManager()

        # Случайно определяем, какое усиление колоды выпадет в 3-м слоте
        self.buff_kind = random.choice(("damage", "heal"))
        self.buff_val = random.randint(2, 3)

        if self.buff_kind == "damage":
            buff_title = f"Заточка клинков (+{self.buff_val})"
            buff_desc = f"Увеличивает урон всех атакующих карт в вашей колоде на +{self.buff_val} до конца забега."
            buff_icon = "Атака"
        else:
            buff_title = f"Благословение жизни (+{self.buff_val})"
            buff_desc = f"Увеличивает лечение всех исцеляющих карт в вашей колоде на +{self.buff_val} до конца забега."
            buff_icon = "Исцеление"

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
                "desc": "Увеличивает макс. здоровье на 10–12% и исцеляет 5–10% здоровья.",
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
        arcade.draw_text("ПОБЕДА В СХВАТКЕ!", SCREEN_WIDTH / 2, 950, BORDER_GOLD, 38, bold=True, anchor_x="center")
        arcade.draw_text(
            f"Выберите награду перед переходом на Этап {self.run.stage + 1} из 3   •   Текущее HP: {self.run.hero.hp} / {self.run.hero.max_hp}",
            SCREEN_WIDTH / 2, 895, TEXT_PARCHMENT, 18, anchor_x="center"
        )

        for idx, opt in enumerate(self.options):
            is_hov = (idx == self.hovered_idx)
            cx, cy = opt["x"], 530
            w, h = 420, 460

            arcade.draw_rect_filled(arcade.XYWH(cx, cy, w, h), (30, 28, 38) if is_hov else PANEL_DARK)
            arcade.draw_rect_outline(arcade.XYWH(cx, cy, w, h), arcade.color.YELLOW if is_hov else BORDER_GOLD, 3.5 if is_hov else 2)

            # Иконка награды
            arcade.draw_circle_filled(cx, cy + 120, 48, (42, 36, 30))
            arcade.draw_circle_outline(cx, cy + 120, 48, BORDER_GOLD, 2)
            draw_card_icon(opt["icon"], cx, cy + 120, size=34)

            arcade.draw_text(opt["title"], cx, cy + 25, BORDER_GOLD, 22, bold=True, anchor_x="center")
            arcade.draw_text(
                opt["desc"], cx, cy - 75, TEXT_PARCHMENT, 16,
                width=w - 50, align="center", anchor_x="center", anchor_y="center", multiline=True
            )
            arcade.draw_text("Нажмите, чтобы выбрать", cx, cy - 190, TEXT_MUTED, 14, anchor_x="center")

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
            self.run.apply_deck_buff(self.buff_kind, self.buff_val)

        from views.battle_view import BattleView
        self.window.show_view(BattleView(self.run))
