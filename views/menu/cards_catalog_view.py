import math
import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BG_DARK, PANEL_DARK, BORDER_GOLD, TEXT_PARCHMENT, TEXT_MUTED
from core.hero import load_hero_templates
from core.card import load_card_library
from core.records import load_records
from visuals.ui.card_widget import CardWidget
from visuals.ui.text_cache import TextCache


class CardsCatalogView(arcade.View):
    """Каталог нейтральных карт (базовых и выпадающих в походе) с прокруткой сетки."""

    def __init__(self, return_view: arcade.View | None = None):
        super().__init__()
        self.return_view = return_view
        self.ui_text = TextCache()
        self.back_btn = (150, SCREEN_HEIGHT - 55, 200, 48)
        self.seen_cards = set(load_records().get("seen_cards", []))




        templates = load_hero_templates()
        library = load_card_library()

        # Собираем ID всех карт, привязанных к личным колодам героев
        hero_bound_ids: set[str] = set()
        for info in templates.values():
            hero_bound_ids.update(info.get("deck", []))

        # Оставляем только нейтральные карты (не привязанные к героям)
        neutral_cards = [
            card for cid, card in library.items()
            if card.neutral or cid not in hero_bound_ids
        ]

        self.cols = 6
        self.col_gap = 250
        self.row_gap = 360
        self.top_y = 770

        self.card_widgets: list[CardWidget] = []
        start_x = SCREEN_WIDTH / 2 - (self.cols - 1) * self.col_gap / 2
        for idx, card in enumerate(neutral_cards):
            col = idx % self.cols
            cx = start_x + col * self.col_gap
            w = CardWidget(card, x=cx, y=0)
            self.card_widgets.append(w)

        rows = math.ceil(len(self.card_widgets) / self.cols) if self.card_widgets else 0
        total_h = rows * self.row_gap
        visible_h = SCREEN_HEIGHT - 160
        self.scroll_y = 0.0
        self.max_scroll = max(0.0, total_h - visible_h)

    def _draw_locked_card(self, w: CardWidget):
        arcade.draw_rect_filled(arcade.XYWH(w.x, w.y, w.width, w.height), (22, 20, 28))
        arcade.draw_rect_outline(arcade.XYWH(w.x, w.y, w.width, w.height), (65, 60, 68), 2)
        arcade.draw_rect_outline(arcade.XYWH(w.x, w.y, w.width - 20, w.height - 20), (42, 40, 48), 1)
        arcade.draw_circle_filled(w.x, w.y + 15, 34, (16, 15, 20))
        self.ui_text.draw("?", w.x, w.y + 15, TEXT_MUTED, 36, bold=True, anchor_x="center", anchor_y="center")
        self.ui_text.draw("НЕ ИЗУЧЕНО", w.x, w.y - 60, TEXT_MUTED, 14, bold=True, anchor_x="center")
        self.ui_text.draw("Вытяните карту в бою", w.x, w.y - 88, (95, 90, 90), 12, anchor_x="center")


    def on_show_view(self):
        arcade.set_background_color(BG_DARK)

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        self.scroll_y = max(0.0, min(self.max_scroll, self.scroll_y - scroll_y * 55.0))

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        if y > SCREEN_HEIGHT - 110:
            for w in self.card_widgets:
                w.hovered = False
            return

        for w in self.card_widgets:
            w.hovered = (
                w.x - w.width / 2 <= x <= w.x + w.width / 2
                and w.y - w.height / 2 <= y <= w.y + w.height / 2
            )

    def on_draw(self):
        self.clear()

        if not self.card_widgets:
            self.ui_text.draw(
                "Нейтральные карты пока не добавлены в data/cards.json",
                SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, TEXT_MUTED, 22, anchor_x="center", anchor_y="center"
            )
        else:
            # Сначала рисуем обычные карты, потом увеличенную при наведении
            hovered_card = None
            for idx, w in enumerate(self.card_widgets):
                row = idx // self.cols
                w.y = self.top_y - row * self.row_gap + self.scroll_y
                if w.y + w.height / 2 < 0 or w.y - w.height / 2 > SCREEN_HEIGHT:
                    continue

                is_seen = (w.data.card_id in self.seen_cards)
                if not is_seen:
                    self._draw_locked_card(w)
                elif w.hovered:
                    hovered_card = w
                else:
                    w.draw(can_afford=True)
                    self.ui_text.draw(
                        f"×{w.data.pool_count} в пуле", w.x, w.y - w.height / 2 - 22,
                        BORDER_GOLD, 14, bold=True, anchor_x="center"
                    )

            if hovered_card:
                hovered_card.draw(can_afford=True)
                scaled_half_h = (hovered_card.height * 1.07) / 2
                self.ui_text.draw(
                    f"×{hovered_card.data.pool_count} в пуле",
                    hovered_card.x,
                    hovered_card.y - scaled_half_h - 22,
                    arcade.color.YELLOW,
                    15,
                    bold=True,
                    anchor_x="center",
                )

        # Закрепленная верхняя шапка экрана
        arcade.draw_rect_filled(arcade.XYWH(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 55, SCREEN_WIDTH, 110), (14, 13, 18, 250))
        arcade.draw_line(0, SCREEN_HEIGHT - 110, SCREEN_WIDTH, SCREEN_HEIGHT - 110, BORDER_GOLD, 2)

        bx, by, bw, bh = self.back_btn
        arcade.draw_rect_filled(arcade.XYWH(bx, by, bw, bh), PANEL_DARK)
        arcade.draw_rect_outline(arcade.XYWH(bx, by, bw, bh), BORDER_GOLD, 2)
        self.ui_text.draw("← В меню", bx, by, TEXT_PARCHMENT, 17, bold=True, anchor_x="center", anchor_y="center")

        # Считаем статистику нейтральной колоды
        unique_total = len(self.card_widgets)
        copies_total = sum(w.data.pool_count for w in self.card_widgets)
        opened_count = sum(1 for w in self.card_widgets if w.data.card_id in self.seen_cards)
        locked_count = unique_total - opened_count

        self.ui_text.draw(
            "НЕЙТРАЛЬНАЯ КОЛОДА КАРТ",
            SCREEN_WIDTH / 2, SCREEN_HEIGHT - 42, BORDER_GOLD, 30, bold=True, anchor_x="center", anchor_y="center"
        )
        self.ui_text.draw(
            f"Уникальных карт: {unique_total} (всего в колоде: {copies_total} шт.)   •   Открыто: {opened_count}  |  Скрыто: {locked_count}",
            SCREEN_WIDTH / 2, SCREEN_HEIGHT - 82, TEXT_PARCHMENT, 16, anchor_x="center", anchor_y="center"
        )

        self.ui_text.draw("Карты, не привязанные к героям", SCREEN_WIDTH - 230, SCREEN_HEIGHT - 58, TEXT_MUTED, 14, anchor_x="center", anchor_y="center")

        if self.max_scroll > 0:
            track_h = SCREEN_HEIGHT - 160
            track_y = (SCREEN_HEIGHT - 110) / 2
            arcade.draw_rect_filled(arcade.XYWH(SCREEN_WIDTH - 24, track_y, 10, track_h), (28, 26, 34))
            ratio = self.scroll_y / self.max_scroll
            thumb_h = max(60, track_h * 0.45)
            thumb_y = (SCREEN_HEIGHT - 125 - thumb_h / 2) - ratio * (track_h - thumb_h - 30)
            arcade.draw_rect_filled(arcade.XYWH(SCREEN_WIDTH - 24, thumb_y, 10, thumb_h), BORDER_GOLD)

    def _go_back(self):
        if self.return_view is not None:
            self.window.show_view(self.return_view)
        else:
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
        elif key == arcade.key.DOWN:
            self.scroll_y = min(self.max_scroll, self.scroll_y + 80)
        elif key == arcade.key.UP:
            self.scroll_y = max(0.0, self.scroll_y - 80)
