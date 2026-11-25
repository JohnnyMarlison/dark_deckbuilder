import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT, PANEL_DARK, BORDER_GOLD, TEXT_PARCHMENT, TEXT_MUTED
from core.events import bus


class BattlePauseMenu:
    """Меню паузы во время боя с доступом к энциклопедиям и подтверждением выхода."""

    def __init__(self, view):
        self.v = view
        self.state: str = "CLOSED"  # "CLOSED" | "MAIN" | "CONFIRM_EXIT"

        cx = SCREEN_WIDTH / 2
        self.buttons = [
            ("RESUME", "Продолжить бой", (cx, 620, 380, 58), (38, 68, 52)),
            ("BESTIARY", "Бестиарий персонажей", (cx, 545, 380, 58), (36, 44, 62)),
            ("CARDS", "Энциклопедия карт", (cx, 470, 380, 58), (36, 44, 62)),
            ("EXIT", "Выйти в главное меню", (cx, 385, 380, 58), (105, 36, 36)),
        ]
        self.confirm_yes_btn = (cx - 125, 430, 210, 54)
        self.confirm_no_btn = (cx + 125, 430, 210, 54)
        self.hovered_id: str | None = None

    @property
    def is_open(self) -> bool:
        return self.state != "CLOSED"

    def open(self):
        self.state = "MAIN"
        self.hovered_id = None
        bus.emit("ui_click")

    def close(self):
        self.state = "CLOSED"
        self.hovered_id = None
        bus.emit("ui_click")

    def handle_escape(self):
        if self.state == "CONFIRM_EXIT":
            self.state = "MAIN"
            bus.emit("ui_click")
        elif self.state == "MAIN":
            self.close()
        else:
            self.open()

    @staticmethod
    def _in_rect(x: float, y: float, rect: tuple[float, float, float, float]) -> bool:
        rx, ry, rw, rh = rect
        return rx - rw / 2 <= x <= rx + rw / 2 and ry - rh / 2 <= y <= ry + rh / 2

    def on_mouse_motion(self, x: float, y: float):
        if not self.is_open:
            return
        self.hovered_id = None
        if self.state == "MAIN":
            for btn_id, _, rect, _ in self.buttons:
                if self._in_rect(x, y, rect):
                    self.hovered_id = btn_id
                    break
        elif self.state == "CONFIRM_EXIT":
            if self._in_rect(x, y, self.confirm_yes_btn):
                self.hovered_id = "YES"
            elif self._in_rect(x, y, self.confirm_no_btn):
                self.hovered_id = "NO"

    def handle_click(self, x: float, y: float) -> bool:
        if not self.is_open:
            return False

        if self.state == "MAIN":
            for btn_id, _, rect, _ in self.buttons:
                if self._in_rect(x, y, rect):
                    bus.emit("ui_click")
                    if btn_id == "RESUME":
                        self.close()
                    elif btn_id == "BESTIARY":
                        from views.menu.heroes_encyclopedia_view import HeroesEncyclopediaView
                        self.v.window.show_view(HeroesEncyclopediaView(return_view=self.v))
                    elif btn_id == "CARDS":
                        from views.menu.cards_catalog_view import CardsCatalogView
                        self.v.window.show_view(CardsCatalogView(return_view=self.v))
                    elif btn_id == "EXIT":
                        self.state = "CONFIRM_EXIT"
                        self.hovered_id = None
                    return True
            return True

        if self.state == "CONFIRM_EXIT":
            if self._in_rect(x, y, self.confirm_yes_btn):
                bus.emit("ui_click")
                self.state = "CLOSED"
                from views.menu.menu_view import MenuView
                self.v.window.show_view(MenuView())
            elif self._in_rect(x, y, self.confirm_no_btn):
                bus.emit("ui_click")
                self.state = "MAIN"
                self.hovered_id = None
            return True

        return True

        if self.state == "CONFIRM_EXIT":
            if self._in_rect(x, y, self.confirm_yes_btn):
                bus.emit("ui_click")
                self.state = "CLOSED"
                from views.menu.menu_view import MenuView
                self.v.window.show_view(MenuView())
            elif self._in_rect(x, y, self.confirm_no_btn):
                bus.emit("ui_click")
                self.state = "MAIN"
                self.hovered_id = None
            return True

        return True

    def draw(self):
        if not self.is_open:
            return

        ui = self.v.ui_text
        cx, cy = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2

        # Затемнение фона боя
        arcade.draw_rect_filled(arcade.XYWH(cx, cy, SCREEN_WIDTH, SCREEN_HEIGHT), (8, 8, 12, 215))

        if self.state == "MAIN":
            arcade.draw_rect_filled(arcade.XYWH(cx, 520, 480, 420), PANEL_DARK)
            arcade.draw_rect_outline(arcade.XYWH(cx, 520, 480, 420), BORDER_GOLD, 3)

            ui.draw("ПАУЗА", cx, 688, BORDER_GOLD, 30, bold=True, anchor_x="center")
            arcade.draw_line(cx - 200, 666, cx + 200, 666, (75, 62, 48), 1.5)

            for btn_id, label, (bx, by, bw, bh), base_col in self.buttons:
                is_hov = (self.hovered_id == btn_id)
                bg = tuple(min(255, c + 28) for c in base_col) if is_hov else base_col
                border = arcade.color.YELLOW if is_hov else BORDER_GOLD
                arcade.draw_rect_filled(arcade.XYWH(bx, by, bw, bh), bg)
                arcade.draw_rect_outline(arcade.XYWH(bx, by, bw, bh), border, 3 if is_hov else 1.8)
                ui.draw(label, bx, by, TEXT_PARCHMENT, 18, bold=True, anchor_x="center", anchor_y="center")

        elif self.state == "CONFIRM_EXIT":
            arcade.draw_rect_filled(arcade.XYWH(cx, 520, 560, 290), (22, 16, 22))
            arcade.draw_rect_outline(arcade.XYWH(cx, 520, 560, 290), (195, 65, 55), 3)

            ui.draw("ПОКИНУТЬ ПОХОД?", cx, 615, (235, 95, 75), 26, bold=True, anchor_x="center")
            ui.draw(
                "Весь прогресс текущего забега будет безвозвратно потерян.\nВы действительно хотите выйти в главное меню?",
                cx, 540, TEXT_PARCHMENT, 16, width=500, align="center", anchor_x="center", anchor_y="center", multiline=True,
            )

            for btn_id, label, (bx, by, bw, bh), base_col in (
                ("YES", "Да, выйти", self.confirm_yes_btn, (125, 36, 36)),
                ("NO", "Остаться", self.confirm_no_btn, (42, 68, 52)),
            ):
                is_hov = (self.hovered_id == btn_id)
                bg = tuple(min(255, c + 28) for c in base_col) if is_hov else base_col
                border = arcade.color.YELLOW if is_hov else BORDER_GOLD
                arcade.draw_rect_filled(arcade.XYWH(bx, by, bw, bh), bg)
                arcade.draw_rect_outline(arcade.XYWH(bx, by, bw, bh), border, 3 if is_hov else 1.8)
                ui.draw(label, bx, by, TEXT_PARCHMENT, 17, bold=True, anchor_x="center", anchor_y="center")
