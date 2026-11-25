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
        # Стопка карт с анимацией перебора верхней карты при наведении (angle > 0)
        shift = math.sin(angle * 3.0) * 4.5 if angle != 0.0 else 0.0
        arcade.draw_rect_filled(arcade.XYWH(cx - 2, cy - 2, size * 1.1, size * 1.45), (75, 68, 60))
        arcade.draw_rect_filled(arcade.XYWH(cx + 2 + shift, cy + 2 + abs(shift) * 0.3, size * 1.1, size * 1.45),
                                (165, 155, 140))
        arcade.draw_rect_outline(arcade.XYWH(cx + 2 + shift, cy + 2 + abs(shift) * 0.3, size * 1.1, size * 1.45),
                                 BORDER_GOLD, 1.5)


    elif stat_type == "discard":
        # Стопка сброса с анимацией перебора карты при наведении
        shift = math.sin(angle * 3.0) * 4.5 if angle != 0.0 else 0.0
        arcade.draw_rect_filled(arcade.XYWH(cx - 2, cy - 2, size * 1.1, size * 1.45), (38, 35, 42))
        arcade.draw_rect_filled(arcade.XYWH(cx + shift, cy + abs(shift) * 0.3, size * 1.1, size * 1.45), (52, 48, 56))
        arcade.draw_rect_outline(arcade.XYWH(cx + shift, cy + abs(shift) * 0.3, size * 1.1, size * 1.45),
                                 (130, 122, 115), 1.5)
        arcade.draw_line(

            cx - size * 0.4 + shift, cy - size * 0.5,
            cx + size * 0.4 + shift, cy + size * 0.5,
            (185, 75, 75), 2

        )

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

def draw_hourglass_icon(cx: float, cy: float, angle: float = 0.0, size: float = 13.0):
    """Рисует иконку песочных часов для кнопки завершения хода."""
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)

    def rot(dx: float, dy: float) -> tuple[float, float]:
        return cx + dx * cos_a - dy * sin_a, cy + dx * sin_a + dy * cos_a

    gold = (228, 185, 85)
    sand = (235, 195, 110)

    top_tri = (rot(-size * 0.7, size), rot(size * 0.7, size), rot(0, 0))
    bot_tri = (rot(-size * 0.7, -size), rot(size * 0.7, -size), rot(0, 0))
    sand_bot = (rot(-size * 0.55, -size * 0.9), rot(size * 0.55, -size * 0.9), rot(0, -size * 0.15))

    arcade.draw_polygon_filled(sand_bot, sand)
    arcade.draw_polygon_outline(top_tri, gold, 1.8)
    arcade.draw_polygon_outline(bot_tri, gold, 1.8)
    arcade.draw_line(*rot(-size * 0.85, size), *rot(size * 0.85, size), gold, 2.5)
    arcade.draw_line(*rot(-size * 0.85, -size), *rot(size * 0.85, -size), gold, 2.5)


def draw_pile_icon(cx: float, cy: float, anim_time: float = 0.0, size: float = 13.0, is_discard: bool = False):
    """Рисует разные анимированные иконки для Колоды добора и Стопки сброса."""
    w, h = size * 1.25, size * 1.65

    if not is_discard:
        # КОЛОДА ДОБОРА: золотая ровная стопка со светящейся руной и верхней картой, тянущейся вверх
        lift = abs(math.sin(anim_time * 2.4)) * 3.2
        arcade.draw_rect_filled(arcade.XYWH(cx - 3, cy - 2, w, h), (38, 35, 48))
        arcade.draw_rect_outline(arcade.XYWH(cx - 3, cy - 2, w, h), (155, 130, 75), 1.3)

        top_x = cx + 2
        top_y = cy + 1 + lift
        arcade.draw_rect_filled(arcade.XYWH(top_x, top_y, w, h), (28, 25, 36))
        arcade.draw_rect_outline(arcade.XYWH(top_x, top_y, w, h), (235, 192, 85), 1.7)
        # Золотой ромб-руна на рубашке верхней карты
        r = size * 0.28
        diamond = ((top_x, top_y + r), (top_x + r, top_y), (top_x, top_y - r), (top_x - r, top_y))
        arcade.draw_polygon_filled(diamond, (235, 192, 85))
    else:
        # СБРОС: веер из двух отыгранных пепельно-медных карт с крестом/погасшим контуром
        sway = math.sin(anim_time * 2.2) * 2.0
        # Нижняя отброшенная карта со сдвигом
        arcade.draw_rect_filled(arcade.XYWH(cx - 4 - sway * 0.4, cy + 2, w, h), (44, 34, 38))
        arcade.draw_rect_outline(arcade.XYWH(cx - 4 - sway * 0.4, cy + 2, w, h), (135, 88, 78), 1.3)

        # Верхняя карта сброса с диагональной чертой отбоя
        top_x = cx + 3 + sway * 0.5
        top_y = cy - 2
        arcade.draw_rect_filled(arcade.XYWH(top_x, top_y, w, h), (32, 26, 30))
        arcade.draw_rect_outline(arcade.XYWH(top_x, top_y, w, h), (185, 115, 95), 1.6)
        arcade.draw_line(top_x - w * 0.28, top_y + h * 0.28, top_x + w * 0.28, top_y - h * 0.28, (185, 115, 95), 1.5)
        arcade.draw_line(top_x + w * 0.28, top_y + h * 0.28, top_x - w * 0.28, top_y - h * 0.28, (185, 115, 95), 1.5)
