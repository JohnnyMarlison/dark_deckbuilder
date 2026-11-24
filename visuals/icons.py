import arcade
import math
from config import BORDER_GOLD


def draw_card_icon(card_type: str, cx: float, cy: float, size: float = 28):
    """Рисует векторную иконку типа карты/действия."""
    if card_type == "Атака":
        arcade.draw_line(cx - size * 0.6, cy - size * 0.6, cx + size * 0.6, cy + size * 0.6, (220, 210, 200), 4)
        arcade.draw_line(cx + size * 0.6, cy - size * 0.6, cx - size * 0.6, cy + size * 0.6, (220, 210, 200), 4)
        arcade.draw_line(cx - size * 0.7, cy - size * 0.3, cx - size * 0.3, cy - size * 0.7, BORDER_GOLD, 3)
        arcade.draw_line(cx + size * 0.7, cy - size * 0.3, cx + size * 0.3, cy - size * 0.7, BORDER_GOLD, 3)

    elif card_type == "Защита":
        points = (
            (cx - size * 0.6, cy + size * 0.6),
            (cx + size * 0.6, cy + size * 0.6),
            (cx + size * 0.5, cy - size * 0.1),
            (cx, cy - size * 0.75),
            (cx - size * 0.5, cy - size * 0.1),
        )
        arcade.draw_polygon_filled(points, (110, 145, 175))
        arcade.draw_polygon_outline(points, (210, 215, 220), 2)

    elif card_type == "Заклинание":
        arcade.draw_circle_filled(cx, cy, size * 0.45, (135, 85, 165))
        arcade.draw_circle_outline(cx, cy, size * 0.65, BORDER_GOLD, 2)
        arcade.draw_line(cx, cy - size * 0.8, cx, cy + size * 0.8, (220, 210, 200), 2)
        arcade.draw_line(cx - size * 0.8, cy, cx + size * 0.8, cy, (220, 210, 200), 2)

    elif card_type == "Исцеление":
        w = size * 0.28
        l = size * 0.7
        arcade.draw_rect_filled(arcade.XYWH(cx, cy, w, l * 1.6), (95, 175, 120))
        arcade.draw_rect_filled(arcade.XYWH(cx, cy, l * 1.6, w), (95, 175, 120))
        arcade.draw_circle_outline(cx, cy, size * 0.75, (200, 210, 200), 2)


def draw_enemy_choice_icons(cx: float, cy: float, time_val: float):
    """Тусклая анимация перебора вариантов действия врага."""
    types = ("Атака", "Защита", "Заклинание", "Исцеление")
    active_idx = int(time_val * 2.0) % 4
    start_x = cx - 48
    for i, t_name in enumerate(types):
        ix = start_x + i * 32
        is_active = (i == active_idx)
        radius = 12 if is_active else 10
        bg = (58, 48, 44, 170) if is_active else (26, 24, 30, 120)
        border = (135, 112, 68, 180) if is_active else (60, 56, 65, 110)

        arcade.draw_circle_filled(ix, cy, radius, bg)
        arcade.draw_circle_outline(ix, cy, radius, border, 1.5)
        draw_card_icon(t_name, ix, cy, size=radius * 0.55)

def draw_stat_icon(stat_type: str, cx: float, cy: float, size: float = 11, angle: float = 0.0):
    """Рисует компактную векторную иконку для параметров UI (HP, Броня, Стамина, Колода, Ход)."""
    if stat_type == "hp":
        # Багровое сердце здоровья
        r = size * 0.45
        arcade.draw_circle_filled(cx - r * 0.85, cy + r * 0.35, r, (215, 65, 70))
        arcade.draw_circle_filled(cx + r * 0.85, cy + r * 0.35, r, (215, 65, 70))
        arcade.draw_polygon_filled(
            ((cx - r * 1.75, cy + r * 0.15), (cx + r * 1.75, cy + r * 0.15), (cx, cy - r * 1.85)),
            (215, 65, 70),
        )

    elif stat_type == "block":
        # Стальной щит брони
        pts = (
            (cx - size * 0.7, cy + size * 0.75),
            (cx + size * 0.7, cy + size * 0.75),
            (cx + size * 0.6, cy - size * 0.15),
            (cx, cy - size * 0.9),
            (cx - size * 0.6, cy - size * 0.15),
        )
        arcade.draw_polygon_filled(pts, (105, 160, 210))
        arcade.draw_polygon_outline(pts, (215, 225, 235), 1.5)

    elif stat_type == "stamina":
        # Золотой ромб/искра стамины
        pts = (
            (cx, cy + size * 0.95),
            (cx + size * 0.7, cy),
            (cx, cy - size * 0.95),
            (cx - size * 0.7, cy),
        )
        arcade.draw_polygon_filled(pts, BORDER_GOLD)
        arcade.draw_polygon_outline(pts, (255, 235, 165), 1.5)

    elif stat_type == "deck":
        # Стопка карт (колода)
        arcade.draw_rect_filled(arcade.XYWH(cx - 2, cy - 2, size * 1.1, size * 1.45), (75, 68, 60))
        arcade.draw_rect_filled(arcade.XYWH(cx + 2, cy + 2, size * 1.1, size * 1.45), (165, 155, 140))
        arcade.draw_rect_outline(arcade.XYWH(cx + 2, cy + 2, size * 1.1, size * 1.45), BORDER_GOLD, 1.5)

    elif stat_type == "discard":
        # Перечеркнутая карта (сброс)
        arcade.draw_rect_filled(arcade.XYWH(cx, cy, size * 1.1, size * 1.45), (52, 48, 56))
        arcade.draw_rect_outline(arcade.XYWH(cx, cy, size * 1.1, size * 1.45), (130, 122, 115), 1.5)
        arcade.draw_line(cx - size * 0.4, cy - size * 0.5, cx + size * 0.4, cy + size * 0.5, (185, 75, 75), 2)



    elif stat_type == "end_turn":
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)

        def rot(dx: float, dy: float) -> tuple[float, float]:
            return (cx + dx * cos_a - dy * sin_a, cy + dx * sin_a + dy * cos_a)

        w = size * 0.65
        h = size * 0.8
        bar_w = size * 0.78

        top = (rot(-w, h), rot(w, h), (cx, cy))
        bot = (rot(-w, -h), rot(w, -h), (cx, cy))

        arcade.draw_polygon_filled(top, BORDER_GOLD)
        arcade.draw_polygon_filled(bot, (225, 215, 195))

        x1, y1 = rot(-bar_w, h)
        x2, y2 = rot(bar_w, h)
        x3, y3 = rot(-bar_w, -h)
        x4, y4 = rot(bar_w, -h)

        arcade.draw_line(x1, y1, x2, y2, BORDER_GOLD, 2)
        arcade.draw_line(x3, y3, x4, y4, BORDER_GOLD, 2)

