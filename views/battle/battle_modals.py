import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT, PANEL_DARK, BORDER_GOLD, TEXT_PARCHMENT, TEXT_MUTED
from visuals.ui.card_widget import CardWidget


class BattleModals:
    """Модальные окна во время боя: просмотр колоды/сброса со скроллом и награды за босса."""

    def __init__(self, view):
        self.v = view
        self.title: str | None = None
        self.widgets: list[CardWidget] = []
        self.base_positions: list[tuple[float, float]] = []
        self.scroll_y: float = 0.0
        self.max_scroll: float = 0.0
        self.close_btn = (SCREEN_WIDTH / 2, 118, 240, 48)
        self.reward_widgets: list[CardWidget] = []

    @property
    def is_open(self) -> bool:
        return self.title is not None

    def open_pile(self, title: str, cards: list):
        self.title = title
        self.widgets.clear()
        self.base_positions.clear()
        self.scroll_y = 0.0

        cols, col_gap, row_gap = 5, 255, 345
        start_y = 735
        for idx, c in enumerate(cards):
            row, col = idx // cols, idx % cols
            items_in_row = min(cols, len(cards) - row * cols)
            row_start_x = SCREEN_WIDTH / 2 - (items_in_row - 1) * col_gap / 2
            bx = row_start_x + col * col_gap
            by = start_y - row * row_gap
            w = CardWidget(c, x=bx, y=by, cost=c.cost)
            self.widgets.append(w)
            self.base_positions.append((bx, by))

        total_rows = (len(cards) + cols - 1) // cols
        self.max_scroll = max(0.0, (total_rows - 2) * row_gap)
        self._apply_scroll()

    def _apply_scroll(self):
        for w, (bx, by) in zip(self.widgets, self.base_positions):
            w.x = bx
            w.y = by + self.scroll_y
            w.target_x = w.x
            w.target_y = w.y

    def close(self):
        self.title = None
        self.widgets.clear()
        self.base_positions.clear()
        self.scroll_y = 0.0

    def setup_boss_rewards(self, reward_cards: list):
        self.reward_widgets.clear()
        self.selected_rewards = []
        self.boss_next_btn = (SCREEN_WIDTH / 2, 215, 340, 58)
        self.boss_next_hovered = False

        gap = 290
        start_x = SCREEN_WIDTH / 2 - (len(reward_cards) - 1) * gap / 2
        for idx, c in enumerate(reward_cards):
            w = CardWidget(c, x=start_x + idx * gap, y=515, cost=c.cost)
            w.scale = 1.0
            self.reward_widgets.append(w)

    def _give_card_to_hero(self, card):
        hero = self.v.hero
        if hasattr(hero, "add_card"):
            hero.add_card(card)
        elif hasattr(hero, "master_deck"):
            hero.master_deck.append(card)
        elif hasattr(hero, "deck"):
            hero.deck.append(card)
        else:
            hero.discard_pile.append(card)

    def handle_click(self, x: float, y: float) -> bool:
        if self.is_open:
            cx, cy, cw, ch = self.close_btn
            if cx - cw / 2 <= x <= cx + cw / 2 and cy - ch / 2 <= y <= cy + ch / 2:
                self.close()
            return True

        if self.v.substate == "BOSS_VICTORY":
            if not hasattr(self, "selected_rewards"):
                self.selected_rewards = []

            for w in self.reward_widgets:
                if w.contains_point(x, y):
                    if w in self.selected_rewards:
                        self.selected_rewards.remove(w)
                    elif len(self.selected_rewards) < 2:
                        self.selected_rewards.append(w)
                    return True

            bx, by, bw, bh = getattr(self, "boss_next_btn", (SCREEN_WIDTH / 2, 215, 340, 58))
            if len(self.selected_rewards) == 2 and (bx - bw / 2 <= x <= bx + bw / 2 and by - bh / 2 <= y <= by + bh / 2):
                for w in self.selected_rewards:
                    self._give_card_to_hero(w.data)
                self.selected_rewards.clear()
                self.v._advance_after_boss()
            return True

        return False


    def on_mouse_scroll(self, scroll_y: float) -> bool:
        if not self.is_open:
            return False
        self.scroll_y = max(0.0, min(self.max_scroll, self.scroll_y - scroll_y * 75.0))
        self._apply_scroll()
        return True

    def on_mouse_motion(self, x: float, y: float):
        if self.is_open:
            in_clip = 165 <= y <= 905
            for w in self.widgets:
                w.hovered = in_clip and w.contains_point(x, y)
        elif self.v.substate == "BOSS_VICTORY":
            for w in self.reward_widgets:
                w.hovered = w.contains_point(x, y)
            bx, by, bw, bh = getattr(self, "boss_next_btn", (SCREEN_WIDTH / 2, 235, 320, 58))
            self.boss_next_hovered = (bx - bw / 2 <= x <= bx + bw / 2 and by - bh / 2 <= y <= by + bh / 2)


    def draw_pile_modal(self):
        if not self.is_open:
            return
        ui = self.v.ui_text
        arcade.draw_rect_filled(arcade.XYWH(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT), (10, 9, 14, 228))
        arcade.draw_rect_filled(arcade.XYWH(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 5, 1520, 920), PANEL_DARK)
        arcade.draw_rect_outline(arcade.XYWH(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 5, 1520, 920), BORDER_GOLD, 3)

        title_txt = f"{self.title.upper()} ({len(self.widgets)} карт)"
        if self.max_scroll > 0:
            title_txt += "  —  листайте колёсиком мыши"
        ui.draw(title_txt, SCREEN_WIDTH / 2, 942, BORDER_GOLD, 24, bold=True, anchor_x="center")

        if not self.widgets:
            ui.draw("В этой стопке пока пусто", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, TEXT_MUTED, 22, anchor_x="center", anchor_y="center")
        else:
            # Обрезаем отрисовку карт строго по внутренней рамке окна (выше кнопки «Закрыть окно»)
            ctx = self.v.window.ctx
            old_scissor = ctx.scissor
            ctx.scissor = (int(SCREEN_WIDTH / 2 - 745), 165, 1490, 740)
            try:
                for w in self.widgets:
                    if not w.hovered and 10 <= w.y <= 1070:
                        w.draw(can_afford=True)
                for w in self.widgets:
                    if w.hovered and 10 <= w.y <= 1070:
                        w.draw(can_afford=True)
            finally:
                ctx.scissor = old_scissor

        cx, cy, cw, ch = self.close_btn
        arcade.draw_rect_filled(arcade.XYWH(cx, cy, cw, ch), (105, 34, 34))
        arcade.draw_rect_outline(arcade.XYWH(cx, cy, cw, ch), BORDER_GOLD, 2)
        ui.draw("Закрыть окно", cx, cy, TEXT_PARCHMENT, 17, bold=True, anchor_x="center", anchor_y="center")

    def draw_boss_victory_overlay(self):
        ui = self.v.ui_text
        if not hasattr(self, "selected_rewards"):
            self.selected_rewards = []
        picks_left = max(0, 2 - len(self.selected_rewards))

        arcade.draw_rect_filled(arcade.XYWH(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT),
                                (10, 9, 14, 238))
        ui.draw("ПОБЕДА НАД БОССОМ!", SCREEN_WIDTH / 2, 835, BORDER_GOLD, 36, bold=True, anchor_x="center")

        sub_txt = (
            f"Выберите 2 усиленные карты в награду (осталось выбрать: {picks_left}):"
            if picks_left > 0
            else "Выбрано 2 карты! Нажмите кнопку ниже, чтобы перейти дальше."
        )
        ui.draw(sub_txt, SCREEN_WIDTH / 2, 780, TEXT_PARCHMENT, 19, anchor_x="center")

        for w in self.reward_widgets:
            is_sel = w in self.selected_rewards
            if is_sel:
                arcade.draw_rect_filled(arcade.XYWH(w.x, w.y, 246, 342), (218, 178, 72, 70))
                arcade.draw_rect_outline(arcade.XYWH(w.x, w.y, 246, 342), arcade.color.YELLOW, 3.5)
            w.draw(can_afford=True)
            if is_sel:
                arcade.draw_rect_filled(arcade.XYWH(w.x, w.y - 180, 164, 30), (38, 86, 48))
                arcade.draw_rect_outline(arcade.XYWH(w.x, w.y - 180, 164, 30), arcade.color.YELLOW, 1.8)
                ui.draw("ВЫБРАНО", w.x, w.y - 180, arcade.color.YELLOW, 14, bold=True, anchor_x="center",
                        anchor_y="center")

        bx, by, bw, bh = getattr(self, "boss_next_btn", (SCREEN_WIDTH / 2, 215, 340, 58))
        ready = len(self.selected_rewards) == 2
        hov = getattr(self, "boss_next_hovered", False) and ready

        btn_bg = (42, 92, 54) if hov else ((32, 72, 42) if ready else (36, 34, 42))
        btn_brd = arcade.color.YELLOW if hov else (BORDER_GOLD if ready else (85, 80, 92))
        btn_txt_col = TEXT_PARCHMENT if ready else TEXT_MUTED
        btn_label = "Следующий мир  >>>" if ready else f"Выберите ещё {picks_left} карт(ы)"

        arcade.draw_rect_filled(arcade.XYWH(bx, by, bw, bh), btn_bg)
        arcade.draw_rect_outline(arcade.XYWH(bx, by, bw, bh), btn_brd, 3 if hov else 2)
        ui.draw(btn_label, bx, by, btn_txt_col, 18, bold=True, anchor_x="center", anchor_y="center")

    def handle_pile_click(self, x: float, y: float) -> bool:
        return self.handle_click(x, y)
