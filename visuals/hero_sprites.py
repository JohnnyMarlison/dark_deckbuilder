import math
import arcade
from config import BORDER_GOLD


def draw_hero_sprite(role: str, cx: float, cy: float, s: float, d: int, b: float, t: float, weapon_angle: float):
    """Рисует детализированную фигурку выбранного героя."""
    if role == "Воин":
        cape_wave = math.sin(t * 5.0) * 5 * s
        arcade.draw_polygon_filled(((cx - 8 * d * s, cy + 12 * s), (cx - 28 * d * s + cape_wave, cy - 38 * s), (cx + 6 * d * s, cy - 36 * s)), (95, 22, 26))
        arcade.draw_rect_filled(arcade.XYWH(cx - 8 * s, cy - 34 * s, 9 * s, 18 * s), (55, 58, 65))
        arcade.draw_rect_filled(arcade.XYWH(cx + 8 * s, cy - 34 * s, 9 * s, 18 * s), (55, 58, 65))
        arcade.draw_rect_filled(arcade.XYWH(cx, cy - 8 * s, 32 * s, 40 * s), (52, 72, 92))
        arcade.draw_rect_outline(arcade.XYWH(cx, cy - 8 * s, 32 * s, 40 * s), (150, 155, 165), 2)
        arcade.draw_circle_filled(cx - 16 * s, cy + 8 * s + b * 0.5, 10 * s, (85, 92, 102))
        arcade.draw_circle_filled(cx + 16 * s, cy + 8 * s + b * 0.5, 10 * s, (85, 92, 102))
        arcade.draw_circle_filled(cx, cy + 25 * s, 15 * s, (140, 145, 152))
        arcade.draw_rect_filled(arcade.XYWH(cx + 5 * d * s, cy + 25 * s, 14 * s, 5 * s), (15, 15, 20))
        arcade.draw_ellipse_filled(cx - 4 * d * s, cy + 42 * s, 22 * s, 11 * s, (145, 32, 36))
        swing = weapon_angle * 0.4 * d * s
        arcade.draw_line(cx + 18 * d * s, cy - 10 * s, cx + 38 * d * s + swing, cy + 32 * s, (210, 215, 220), 5)
        arcade.draw_line(cx + 13 * d * s, cy - 4 * s, cx + 25 * d * s, cy - 12 * s, BORDER_GOLD, 4)
        arcade.draw_ellipse_filled(cx - 14 * d * s, cy - 8 * s, 22 * s, 32 * s, (115, 82, 48))
        arcade.draw_ellipse_outline(cx - 14 * d * s, cy - 8 * s, 22 * s, 32 * s, BORDER_GOLD, 2)

    elif role == "Элементалист":
        robe = ((cx - 22 * s, cy - 40 * s), (cx + 22 * s, cy - 40 * s), (cx + 10 * s, cy + 16 * s), (cx - 10 * s, cy + 16 * s))
        arcade.draw_polygon_filled(robe, (105, 24, 24))
        arcade.draw_line(cx - 20 * s, cy - 38 * s, cx + 20 * s, cy - 38 * s, BORDER_GOLD, 3)
        arcade.draw_circle_filled(cx, cy - 6 * s, 6 * s, (210, 110, 30))
        arcade.draw_circle_filled(cx, cy + 22 * s, 13 * s, (205, 175, 150))
        hat = ((cx - 24 * s, cy + 30 * s), (cx + 24 * s, cy + 30 * s), (cx - 6 * d * s, cy + 60 * s))
        arcade.draw_polygon_filled(hat, (38, 26, 62))
        arcade.draw_line(cx - 22 * s, cy + 30 * s, cx + 22 * s, cy + 30 * s, BORDER_GOLD, 3)
        pulse = math.sin(t * 8.0) * 3 * s
        sx = cx + 22 * d * s
        arcade.draw_line(sx, cy - 40 * s, sx, cy + 34 * s, (78, 48, 28), 4)
        arcade.draw_circle_filled(sx, cy + 38 * s, 11 * s + pulse, (210, 80, 20, 120))
        arcade.draw_circle_filled(sx, cy + 38 * s, 6 * s, (235, 150, 40))

    elif role == "Паладин":
        wing_flap = math.sin(t * 4.0) * 4 * s
        arcade.draw_ellipse_filled(cx - 20 * d * s, cy + 12 * s + wing_flap, 30 * s, 14 * s, (215, 205, 175, 170))
        arcade.draw_rect_filled(arcade.XYWH(cx, cy - 8 * s, 32 * s, 44 * s), BORDER_GOLD)
        arcade.draw_rect_filled(arcade.XYWH(cx, cy - 10 * s, 16 * s, 38 * s), (215, 210, 198))
        arcade.draw_line(cx, cy - 22 * s, cx, cy + 4 * s, (140, 30, 35), 3)
        arcade.draw_line(cx - 6 * s, cy - 6 * s, cx + 6 * s, cy - 6 * s, (140, 30, 35), 3)
        arcade.draw_circle_filled(cx, cy + 25 * s, 14 * s, (215, 200, 175))
        arcade.draw_ellipse_outline(cx, cy + 45 * s + b * 0.5, 26 * s, 8 * s, (215, 180, 75), 3)
        mx = cx + 22 * d * s
        arcade.draw_line(mx, cy - 30 * s, mx, cy + 24 * s, (82, 52, 30), 4)
        arcade.draw_rect_filled(arcade.XYWH(mx, cy + 24 * s, 24 * s, 14 * s), (120, 155, 185))

    elif role == "Ассасин":
        cloak = ((cx - 22 * s, cy - 38 * s), (cx + 22 * s, cy - 38 * s), (cx + 12 * s, cy + 16 * s), (cx - 12 * s, cy + 16 * s))
        arcade.draw_polygon_filled(cloak, (30, 32, 38))
        scarf_wave = math.sin(t * 7.0) * 6 * s
        arcade.draw_rect_filled(arcade.XYWH(cx, cy + 13 * s, 24 * s, 7 * s), (130, 28, 34))
        arcade.draw_line(cx - 10 * d * s, cy + 13 * s, cx - 26 * d * s + scarf_wave, cy + 4 * s, (130, 28, 34), 5)
        arcade.draw_circle_filled(cx, cy + 24 * s, 15 * s, (15, 15, 20))
        arcade.draw_circle_filled(cx + 6 * d * s, cy + 24 * s, 3 * s, (75, 205, 125))
        arcade.draw_line(cx + 18 * d * s, cy - 10 * s, cx + 36 * d * s, cy + 8 * s, (90, 195, 125), 3)
        arcade.draw_line(cx - 18 * d * s, cy - 10 * s, cx - 34 * d * s, cy + 8 * s, (150, 155, 160), 3)
