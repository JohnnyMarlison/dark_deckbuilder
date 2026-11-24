import math
import arcade
from visuals.locations.common import draw_horizon_base


def draw_dark_forest(t: float):
    draw_horizon_base((12, 18, 16), (15, 20, 17), (36, 48, 38))
    arcade.draw_circle_filled(960, 955, 62, (165, 185, 165, 45))
    arcade.draw_circle_filled(960, 955, 44, (195, 210, 190, 90))
    arcade.draw_ellipse_filled(330, 602, 360, 46, (24, 52, 36, 220))
    arcade.draw_ellipse_filled(1590, 602, 380, 50, (24, 52, 36, 220))

    for i, tx in enumerate((130, 290, 460, 780, 1140, 1450, 1630, 1810)):
        w = 26 if i % 2 == 0 else 18
        arcade.draw_rect_filled(arcade.XYWH(tx, 845, w, 460), (20, 25, 21))
        arcade.draw_line(tx, 860, tx - 65, 930, (20, 25, 21), 6)
        arcade.draw_line(tx, 900, tx + 70, 970, (20, 25, 21), 5)
        arcade.draw_circle_filled(tx, 1040, 115, (14, 24, 18, 235))

    for wx, wy in ((375, 890), (1540, 900)):
        for r in (20, 40, 60):
            arcade.draw_arc_outline(wx, wy, r * 2, r * 2, (170, 175, 175, 75), 180, 360, 1.5)
        arcade.draw_line(wx - 60, wy, wx + 60, wy, (170, 175, 175, 75), 1)
        arcade.draw_line(wx, wy, wx - 42, wy - 42, (170, 175, 175, 75), 1)
        arcade.draw_line(wx, wy, wx + 42, wy - 42, (170, 175, 175, 75), 1)

    drift = math.sin(t * 0.7) * 65
    arcade.draw_ellipse_filled(620 + drift, 625, 680, 65, (120, 145, 130, 28))
    arcade.draw_ellipse_filled(1300 - drift, 620, 740, 72, (120, 145, 130, 28))


def draw_abandoned_village(t: float):
    draw_horizon_base((16, 16, 22), (19, 18, 23), (55, 48, 42))
    for hx, hw, hh in ((340, 240, 180), (1580, 250, 190)):
        arcade.draw_rect_filled(arcade.XYWH(hx, 615 + hh / 2, hw, hh), (38, 34, 32))
        arcade.draw_rect_outline(arcade.XYWH(hx, 615 + hh / 2, hw, hh), (62, 54, 48), 2)
        roof = ((hx - hw / 2 - 20, 615 + hh), (hx + hw / 2 + 20, 615 + hh), (hx - 15, 615 + hh + 105))
        arcade.draw_polygon_filled(roof, (28, 24, 22))
        arcade.draw_rect_filled(arcade.XYWH(hx - 45, 615 + hh * 0.55, 40, 48), (10, 10, 14))
        arcade.draw_rect_filled(arcade.XYWH(hx + 45, 615 + hh * 0.55, 40, 48), (10, 10, 14))

    for fx in range(160, 1780, 46):
        if 480 <= fx <= 1430:
            continue
        tilt = math.sin(fx) * 7
        arcade.draw_line(fx, 615, fx + tilt, 615 + 56 + (fx % 3) * 12, (58, 44, 32), 5)
    arcade.draw_line(150, 650, 475, 646, (52, 40, 28), 3)
    arcade.draw_line(1435, 646, 1770, 652, (52, 40, 28), 3)

    for gx in (210, 485, 690, 1230, 1430, 1710):
        for blade in (-10, -4, 3, 9):
            sway = math.sin(t * 2.5 + gx) * 4
            arcade.draw_line(gx + blade, 615, gx + blade * 1.6 + sway, 655, (44, 62, 36), 3)


def draw_bandit_camp(t: float):
    draw_horizon_base((18, 15, 16), (22, 18, 18), (62, 46, 36))
    for tx, tw, th in ((340, 260, 165), (1580, 270, 175)):
        tent = ((tx - tw / 2, 615), (tx + tw / 2, 615), (tx, 615 + th))
        arcade.draw_polygon_filled(tent, (78, 38, 30))
        arcade.draw_polygon_outline(tent, (110, 62, 46), 2)
        door = ((tx - 32, 615), (tx + 32, 615), (tx, 615 + th * 0.58))
        arcade.draw_polygon_filled(door, (14, 12, 14))

    for bx, by in ((505, 632), (545, 628), (522, 665), (1390, 632), (1432, 628)):
        arcade.draw_rect_filled(arcade.XYWH(bx, by, 38, 34), (88, 60, 38))
        arcade.draw_rect_outline(arcade.XYWH(bx, by, 38, 34), (48, 32, 20), 2)

    for px in (720, 1200):
        arcade.draw_line(px, 615, px, 825, (64, 44, 30), 7)
        arcade.draw_circle_filled(px, 833, 12, (195, 186, 168))

    arcade.draw_line(960, 615, 960, 895, (68, 48, 32), 8)
    wave = math.sin(t * 4.5) * 10
    flag = ((964, 890), (1075, 875 + wave), (1055, 845 + wave * 0.6), (1080, 820 + wave), (964, 815))
    arcade.draw_polygon_filled(flag, (128, 26, 26))
