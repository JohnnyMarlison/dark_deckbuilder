import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BG_DARK, PANEL_DARK, BORDER_GOLD, TEXT_PARCHMENT, TEXT_MUTED
from core.records import load_records, DEFAULT_HEROES, ACHIEVEMENTS_CATALOG
from visuals.ui.icons import draw_card_icon


class RecordsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.data = load_records()
        self.back_btn = (150, SCREEN_HEIGHT - 65, 200, 50)

    def on_show_view(self):
        arcade.set_background_color(BG_DARK)

    def on_draw(self):
        self.clear()
        bx, by, bw, bh = self.back_btn
        arcade.draw_rect_filled(arcade.XYWH(bx, by, bw, bh), PANEL_DARK)
        arcade.draw_rect_outline(arcade.XYWH(bx, by, bw, bh), BORDER_GOLD, 2)
        arcade.draw_text("← В меню", bx, by, TEXT_PARCHMENT, 17, bold=True, anchor_x="center", anchor_y="center")

        arcade.draw_text("ЛЕТОПИСЬ ПОБЕД И ДОСТИЖЕНИЯ", SCREEN_WIDTH / 2, SCREEN_HEIGHT - 75, BORDER_GOLD, 34, bold=True, anchor_x="center")

        self._draw_left_records_table()
        self._draw_right_achievements()

    def _draw_left_records_table(self):
        # Левая половина экрана (центр X = 480, ширина = 840)
        tx = 480
        arcade.draw_text("СТАТИСТИКА ГЕРОЕВ", tx, 890, TEXT_PARCHMENT, 22, bold=True, anchor_x="center")

        header_y = 825
        arcade.draw_rect_filled(arcade.XYWH(tx, header_y, 840, 56), PANEL_DARK)
        arcade.draw_rect_outline(arcade.XYWH(tx, header_y, 840, 56), BORDER_GOLD, 2)

        cols = (165, 325, 455, 600, 775)
        headers = ("Герой", "Боев", "Побед", "Макс. НГ+", "Рекорд")
        for cx, title in zip(cols, headers):
            arcade.draw_text(title, cx, header_y, BORDER_GOLD, 16, bold=True, anchor_x="center", anchor_y="center")

        heroes_data = self.data.get("heroes", {})
        for i, hero_name in enumerate(DEFAULT_HEROES):
            row_y = 740 - i * 95
            row_color = (20, 18, 26) if i % 2 == 0 else (28, 25, 36)
            arcade.draw_rect_filled(arcade.XYWH(tx, row_y, 840, 80), row_color)
            arcade.draw_rect_outline(arcade.XYWH(tx, row_y, 840, 80), (65, 58, 52), 1)

            rec = heroes_data.get(hero_name, {"wins": 0, "games": 0, "best_turns": None, "max_ng": 0})
            best = f"{rec['best_turns']} ход." if rec["best_turns"] is not None else "—"
            ng_str = f"НГ+{rec.get('max_ng', 0)}" if rec.get("max_ng", 0) > 0 else "Обычный"
            values = (hero_name, str(rec["games"]), str(rec["wins"]), ng_str, best)

            for cx, val in zip(cols, values):
                arcade.draw_text(val, cx, row_y, TEXT_PARCHMENT, 16, bold=(cx == 165), anchor_x="center", anchor_y="center")

    def _draw_right_achievements(self):
        # Правая половина экрана (2 колонки по 7 карточек достижений)
        unlocked = set(self.data.get("achievements", []))
        total = len(ACHIEVEMENTS_CATALOG)
        arcade.draw_text(f"ДОСТИЖЕНИЯ ({len(unlocked)} / {total})", 1400, 890, TEXT_PARCHMENT, 22, bold=True, anchor_x="center")

        start_x = 1175
        col_gap = 455
        start_y = 815
        row_gap = 104

        for idx, ach in enumerate(ACHIEVEMENTS_CATALOG):
            col = idx // 7
            row = idx % 7
            cx = start_x + col * col_gap
            cy = start_y - row * row_gap
            is_done = ach["id"] in unlocked

            bg = (28, 26, 36) if is_done else (18, 17, 22)
            border = BORDER_GOLD if is_done else (52, 48, 56)
            arcade.draw_rect_filled(arcade.XYWH(cx, cy, 435, 90), bg)
            arcade.draw_rect_outline(arcade.XYWH(cx, cy, 435, 90), border, 2 if is_done else 1)

            # Иконка достижения
            ix = cx - 175
            arcade.draw_circle_filled(ix, cy, 26, (48, 40, 30) if is_done else (26, 25, 30))
            arcade.draw_circle_outline(ix, cy, 26, border, 1.5)
            if is_done:
                draw_card_icon(ach["icon"], ix, cy, size=19)
            else:
                arcade.draw_text("?", ix, cy, TEXT_MUTED, 18, bold=True, anchor_x="center", anchor_y="center")

            # Заголовок и описание
            tx = ix + 40
            title_col = BORDER_GOLD if is_done else TEXT_MUTED
            desc_col = TEXT_PARCHMENT if is_done else (95, 90, 88)
            arcade.draw_text(ach["title"], tx, cy + 16, title_col, 14, bold=True, anchor_x="left")
            arcade.draw_text(ach["desc"], tx, cy - 14, desc_col, 12, width=335, anchor_x="left", anchor_y="center", multiline=True)

    def _go_back(self):
        from views.menu.menu_view import MenuView
        self.window.show_view(MenuView())

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return
        bx, by, bw, bh = self.back_btn
        if bx - bw / 2 <= x <= bx + bw / 2 and by - bh / 2 <= y <= by + bh / 2:
            self._go_back()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self._go_back()
