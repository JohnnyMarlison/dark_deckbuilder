import arcade
from config import SCREEN_WIDTH, BG_DARK, BORDER_GOLD, TEXT_PARCHMENT, TEXT_MUTED
from core.run_state import RunState
from visuals.ui.card_widget import CardWidget
from visuals.ui.achievement_popup import AchievementToastManager
from visuals.ui.text_cache import TextCache

class BossRewardView(arcade.View):
    """Выбор 2 из 4 усиленных карт в колоду после победы над Боссом."""

    def __init__(self, run: RunState, is_final_boss: bool = True):
        super().__init__()
        self.run = run
        self.is_final_boss = is_final_boss
        self.toast_manager = AchievementToastManager()

        choices = self.run.generate_boss_card_choices(4)
        self.widgets: list[CardWidget] = []
        self.selected_indices: set[int] = set()

        spacing = 310
        start_x = SCREEN_WIDTH / 2 - (len(choices) - 1) * spacing / 2
        for i, card in enumerate(choices):
            w = CardWidget(card, x=start_x + i * spacing, y=540)
            w.width = 230
            w.height = 325
            self.widgets.append(w)

        self.confirm_btn = (SCREEN_WIDTH / 2, 210, 420, 68)

    def on_show_view(self):
        arcade.set_background_color(BG_DARK)

    def on_update(self, delta_time: float):
        self.toast_manager.update(delta_time)
        for w in self.widgets:
            w.update(delta_time)

    def on_draw(self):
        self.clear()
        arcade.draw_text("ТРОФЕИ ВЛАДЫКИ ТЬМЫ", SCREEN_WIDTH / 2, 950, BORDER_GOLD, 38, bold=True, anchor_x="center")
        arcade.draw_text(
            f"Выберите 2 усиленные карты в вашу колоду (Выбрано: {len(self.selected_indices)} / 2)",
            SCREEN_WIDTH / 2, 895, TEXT_PARCHMENT, 19, anchor_x="center"
        )

        for i, w in enumerate(self.widgets):
            w.draw(can_afford=True)
            if i in self.selected_indices:
                arcade.draw_rect_outline(arcade.XYWH(w.x, w.y, w.width + 18, w.height + 18), (95, 215, 130), 4)
                arcade.draw_text("ВЫБРАНО", w.x, w.y - w.height / 2 - 28, (95, 215, 130), 16, bold=True, anchor_x="center")

        ready = (len(self.selected_indices) == 2)
        bx, by, bw, bh = self.confirm_btn
        btn_col = (38, 68, 52) if ready else (35, 34, 42)
        border_col = BORDER_GOLD if ready else (75, 70, 65)

        arcade.draw_rect_filled(arcade.XYWH(bx, by, bw, bh), btn_col)
        arcade.draw_rect_outline(arcade.XYWH(bx, by, bw, bh), border_col, 2.5)

        next_text = f"Отправиться в НГ+{self.run.ng_level + 1} →" if self.is_final_boss else f"Перейти в Мир {self.run.stage + 1} →"
        arcade.draw_text(
            next_text if ready else "Выберите 2 карты",
            bx, by, TEXT_PARCHMENT if ready else TEXT_MUTED, 19, bold=True, anchor_x="center", anchor_y="center"
        )

        self.toast_manager.draw()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        for w in self.widgets:
            w.hovered = w.is_clicked(x, y)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        for i, w in enumerate(self.widgets):
            if w.is_clicked(x, y):
                if i in self.selected_indices:
                    self.selected_indices.remove(i)
                elif len(self.selected_indices) < 2:
                    self.selected_indices.add(i)
                return

        if len(self.selected_indices) == 2:
            bx, by, bw, bh = self.confirm_btn
            if bx - bw / 2 <= x <= bx + bw / 2 and by - bh / 2 <= y <= by + bh / 2:
                chosen_cards = [self.widgets[i].data for i in self.selected_indices]
                self.run.add_cards_to_deck(chosen_cards)
                if self.is_final_boss:
                    self.run.start_new_game_plus()
                else:
                    self.run.hero.heal(int(self.run.hero.max_hp * 0.35))
                    self.run.advance_step()
                from views.battle.battle_view import BattleView
                self.window.show_view(BattleView(self.run))
