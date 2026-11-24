import arcade
from visuals.locations.common import draw_horizon_base, draw_candle_holder


def draw_sand_crypt(t: float):
    draw_horizon_base((52, 45, 36), (32, 28, 22), (82, 72, 56))
    for y in range(615, 1080, 48):
        arcade.draw_line(0, y, 1920, y, (38, 33, 26), 2)
        offset = 60 if ((y - 615) // 48) % 2 == 0 else 0
        for x in range(offset, 1920, 120):
            arcade.draw_line(x, y, x, y + 48, (38, 33, 26), 2)

    for cx in (340, 1580):
        coffin = ((cx - 55, 615), (cx + 55, 615), (cx + 70, 665), (cx - 70, 665))
        arcade.draw_polygon_filled(coffin, (96, 85, 68))
        arcade.draw_polygon_outline(coffin, (145, 128, 98), 2)

    for sx in (680, 1240):
        arcade.draw_rect_filled(arcade.XYWH(sx, 755, 95, 250), (28, 24, 19))
        arcade.draw_rect_filled(arcade.XYWH(sx, 632, 64, 34), (102, 90, 72))
        arcade.draw_rect_filled(arcade.XYWH(sx, 712, 44, 125), (118, 105, 84))
        arcade.draw_circle_filled(sx, 792, 18, (118, 105, 84))
        draw_candle_holder(sx + (65 if sx < 960 else -65), 615, t, flame_color=(235, 145, 45))


def draw_ruined_castle(t: float):
    draw_horizon_base((22, 24, 28), (20, 21, 25), (62, 66, 74))
    arcade.draw_rect_filled(arcade.XYWH(320, 765, 560, 300), (48, 51, 58))
    arcade.draw_rect_filled(arcade.XYWH(1600, 765, 560, 300), (48, 51, 58))
    for bx in range(60, 580, 75):
        arcade.draw_rect_filled(arcade.XYWH(bx, 935, 45, 40), (48, 51, 58))
    for bx in range(1340, 1880, 75):
        arcade.draw_rect_filled(arcade.XYWH(bx, 935, 45, 40), (48, 51, 58))

    arcade.draw_polygon_filled(((390, 700), (465, 720), (440, 810), (375, 785)), (16, 17, 22))
    arcade.draw_polygon_filled(((1480, 690), (1550, 715), (1530, 800), (1465, 770)), (16, 17, 22))

    arcade.draw_arc_outline(960, 615, 320, 430, (68, 72, 80), 0, 180, 18)
    arcade.draw_polygon_filled(((810, 615), (930, 615), (915, 790), (810, 810)), (62, 44, 30))
    arcade.draw_polygon_filled(((1110, 615), (995, 615), (1020, 740), (1110, 775)), (62, 44, 30))

    arcade.draw_polygon_filled(((460, 635), (565, 620), (555, 660), (450, 675)), (74, 52, 34))
    arcade.draw_circle_outline(485, 625, 20, (52, 36, 24), 4)
    arcade.draw_circle_outline(555, 618, 15, (52, 36, 24), 3)


def draw_ruined_colosseum(t: float):
    draw_horizon_base((26, 22, 20), (24, 21, 19), (66, 58, 50))
    arcade.draw_arc_outline(960, 615, 1650, 560, (58, 52, 46), 0, 180, 26)
    arcade.draw_arc_outline(960, 615, 1420, 450, (48, 42, 37), 0, 180, 22)
    for ax in range(340, 1620, 160):
        arcade.draw_arc_filled(ax, 745, 75, 105, (16, 14, 15), 0, 180)

    for cx, ch in ((290, 255), (440, 150), (1480, 175), (1630, 275)):
        arcade.draw_rect_filled(arcade.XYWH(cx, 615 + ch / 2, 48, ch), (98, 90, 80))
        arcade.draw_rect_filled(arcade.XYWH(cx, 623, 64, 16), (78, 72, 64))
        arcade.draw_polygon_filled(((cx - 24, 615 + ch), (cx + 24, 615 + ch), (cx - 10, 615 + ch + 22)), (98, 90, 80))

    arcade.draw_line(740, 615, 760, 670, (155, 160, 165), 4)
    arcade.draw_ellipse_filled(1180, 622, 52, 20, (92, 68, 44))
