import math
import arcade


def draw_horizon_base(sky_color, ground_color, line_color):
    """Отрисовывает небо/стены (y = 615..1080) и землю под ареной (y = 410..615)."""
    arcade.draw_rect_filled(arcade.XYWH(960, 848, 1920, 465), sky_color)
    arcade.draw_rect_filled(arcade.XYWH(960, 512, 1920, 205), ground_color)
    arcade.draw_line(0, 615, 1920, 615, line_color, 2)


def draw_candle_holder(x: float, y: float, t: float, flame_color=(245, 165, 45)):
    """Кованый подсвечник с мерцающим пламенем."""
    arcade.draw_rect_filled(arcade.XYWH(x, y + 18, 8, 36), (65, 60, 58))
    arcade.draw_rect_filled(arcade.XYWH(x, y + 36, 22, 5), (85, 78, 72))
    for dx in (-8, 0, 8):
        arcade.draw_rect_filled(arcade.XYWH(x + dx, y + 44, 4, 12), (210, 200, 180))
        flicker = math.sin(t * 11.0 + x + dx) * 1.8
        arcade.draw_circle_filled(x + dx, y + 54, 5 + flicker * 0.4, (*flame_color, 110))
        arcade.draw_circle_filled(x + dx, y + 53, 3, (255, 235, 160))


def draw_skull_pile(x: float, y: float, scale: float = 1.0):
    """Груда костей и черепов у подножия стен."""
    s = scale
    arcade.draw_line(x - 24 * s, y - 4 * s, x + 22 * s, y + 8 * s, (175, 168, 152), 4)
    arcade.draw_line(x - 18 * s, y + 10 * s, x + 26 * s, y - 3 * s, (155, 148, 134), 4)
    for cx, cy, r in ((x - 8 * s, y + 6 * s, 9 * s), (x + 11 * s, y + 3 * s, 8 * s)):
        arcade.draw_circle_filled(cx, cy, r, (195, 188, 172))
        arcade.draw_circle_filled(cx - 3 * s, cy, 2 * s, (20, 18, 22))
        arcade.draw_circle_filled(cx + 3 * s, cy, 2 * s, (20, 18, 22))
