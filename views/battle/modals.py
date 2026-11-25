import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BORDER_GOLD, TEXT_PARCHMENT, TEXT_MUTED
from visuals.ui.card_widget import CardWidget


class BattleModals:
    """Управляет модальными окнами на экране боя (Колода, Сброс, Победа над финальным боссом)."""

    def __init__(self, view):
        self.v = view
        self.mode: str | None = None  # "DRAW" | "DISCARD" | None
        self.widgets: list[CardWidget] = []
        self.scroll_y: float = 0.0
        self.max_scroll: float = 0.0
        self.close_btn = (SCREEN_WIDTH / 2, 144, 260, 50)

    @property
    def is_open(self) -> bool:
        return self.mode is not None

    def open_pile(self, mode: str):
        self.mode = mode
        self.scroll_y = 0.0
        source = self.v.hero.draw_pile if mode == "DRAW" else self.v.hero.discard_pile
        cards = sorted(source, key=lambda c: c.name) if mode == "DRAW" else list(source)
        self.widgets = [CardWidget(c, x=0, y=0) for c in cards]

        cols, row_gap = 5, 345
        rows = (len(self.widgets) + cols - 1) // cols
        self.max_scroll = max(0.0, rows * row_gap - 650)

    def close(self):
        self.mode = None

    def on_scroll(self, scroll_y: float):
        if self.is_open:
            self.scroll_y = max(0.0, min(self.max_scroll, self.scroll_y - scroll_y * 55.0))

    def handle_click(self, x: float, y: float) -> bool:
        """Возвращает True, если клик обработан модальным окном."""
        if not self.is_open:
            return False
        cx, cy, cw, ch = self.close_btn
        in_close = (cx - cw / 2 <= x <= cx + cw / 2 and cy - ch / 2 <= y <= cy + ch / 2)
        outside = not (SCREEN_WIDTH / 2 - 760 <= x <= SCREEN_WIDTH / 2 + 760 and 100 <= y <= 980)
        if in_close or outside:
            self.close()
        return True

    def draw_pile_modal(self):
        if not self.is_open:
            return
        ui = self.v.ui_text
        arcade.draw_rect_filled(arcade.XYWH(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT), (10, 9, 14, 228))

        mw, mh = 1520, 880
        mx, my = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 10
        arcade.draw_rect_filled(arcade.XYWH(mx, my, mw, mh), (20, 18, 26))

        is_draw = (self.mode == "DRAW")
        title = f"ОСТАВШИЕСЯ КАРТЫ В КОЛОДЕ ({len(self.widgets)})" if is_draw else f"СТОПКА СБРОСА ({len(self.widgets)})"
        sub = "Порядок карт перемешан (просмотр без взаимодействия)" if is_draw else "Карты, уже сыгранные в этом бою"

        clip_left, clip_bottom, clip_w, clip_h = int(mx - mw / 2 + 10), 185, mw - 20, 670
        if not self.widgets:
            ui.draw("В этой стопке сейчас пусто", mx, my, TEXT_MUTED, 22, anchor_x="center", anchor_y="center")
        else:
            prev_scissor = self.v.window.ctx.scissor
            self.v.window.ctx.scissor = (clip_left, clip_bottom, clip_w, clip_h)
            try:
                cols, col_gap, row_gap, start_y = 5, 265, 345, 680
                for idx, w in enumerate(self.widgets):
                    row, col = idx // cols, idx % cols
                    items_in_row = min(cols, len(self.widgets) - row * cols)
                    row_start_x = mx - (items_in_row - 1) * col_gap / 2
                    w.x = row_start_x + col * col_gap
                    w.y = start_y - row * row_gap + self.scroll_y
                    if w.y + w.height / 2 >= clip_bottom and w.y - w.height / 2 <= clip_bottom + clip_h:
                        w.draw(can_afford=True)
            finally:
                self.v.window.ctx.scissor = prev_scissor

        ui.draw(title, mx, 922, BORDER_GOLD, 26, bold=True, anchor_x="center")
        ui.draw(sub, mx, 886, TEXT_MUTED, 14, anchor_x="center")
        arcade.draw_line(mx - mw / 2, 862, mx + mw / 2, 862, (75, 62, 48), 1.5)

        arcade.draw_line(mx - mw / 2, 178, mx + mw / 2, 178, (75, 62, 48), 1.5)
        cx, cy, cw, ch = self.close_btn
        arcade.draw_rect_filled(arcade.XYWH(cx, cy, cw, ch), (105, 34, 34))
        arcade.draw_rect_outline(arcade.XYWH(cx, cy, cw, ch), BORDER_GOLD, 2)
        ui.draw("Закрыть [ESC]", cx, cy, TEXT_PARCHMENT, 17, bold=True, anchor_x="center", anchor_y="center")

        if self.max_scroll > 0:
            track_x, track_y = mx + mw / 2 - 22, clip_bottom + clip_h / 2
            arcade.draw_rect_filled(arcade.XYWH(track_x, track_y, 8, clip_h - 20), (32, 30, 40))
            ratio = self.scroll_y / self.max_scroll
            thumb_h = max(55, (clip_h - 20) * 0.35)
            thumb_y = (clip_bottom + clip_h - 10 - thumb_h / 2) - ratio * (clip_h - 20 - thumb_h)
            arcade.draw_rect_filled(arcade.XYWH(track_x, thumb_y, 8, thumb_h), BORDER_GOLD)

        arcade.draw_rect_outline(arcade.XYWH(mx, my, mw, mh), BORDER_GOLD, 3)

    def draw_boss_victory_overlay(self):
        ui = self.v.ui_text
        run = self.v.run
        arcade.draw_rect_filled(arcade.XYWH(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 40, 760, 340), (16, 14, 22, 245))
        arcade.draw_rect_outline(arcade.XYWH(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 40, 760, 340), BORDER_GOLD, 3)

        ui.draw("ВЛАДЫКА ТЬМЫ ПОВЕРЖЕН!", SCREEN_WIDTH / 2, 650, BORDER_GOLD, 32, bold=True, anchor_x="center")
        ui.draw(f"Летопись обновлена! Пройдено за {run.total_turns} ходов (Режим: НГ+{run.ng_level}).", SCREEN_WIDTH / 2, 590, TEXT_PARCHMENT, 16, anchor_x="center")
        ui.draw("Спуститься глубже во тьму (НГ+) или вернуться в главное меню?", SCREEN_WIDTH / 2, 545, TEXT_MUTED, 15, anchor_x="center")

        cx, cy, cw, ch = self.v.ng_continue_btn
        arcade.draw_rect_filled(arcade.XYWH(cx, cy, cw, ch), (38, 68, 52))
        arcade.draw_rect_outline(arcade.XYWH(cx, cy, cw, ch), BORDER_GOLD, 2)
        ui.draw(f"Продолжить (НГ+{run.ng_level + 1})", cx, cy, TEXT_PARCHMENT, 17, bold=True, anchor_x="center", anchor_y="center")

        ex, ey, ew, eh = self.v.ng_exit_btn
        arcade.draw_rect_filled(arcade.XYWH(ex, ey, ew, eh), (36, 52, 74))
        arcade.draw_rect_outline(arcade.XYWH(ex, ey, ew, eh), BORDER_GOLD, 2)
        ui.draw("Выйти в меню", ex, ey, TEXT_PARCHMENT, 17, bold=True, anchor_x="center", anchor_y="center")
