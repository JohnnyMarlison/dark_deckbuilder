import arcade
from visuals.locations.common import draw_horizon_base, draw_candle_holder, draw_skull_pile


def draw_obsidian_citadel(t: float):
    draw_horizon_base((20, 15, 22), (18, 15, 20), (65, 32, 38))
    for y in range(615, 1080, 44):
        arcade.draw_line(0, y, 1920, y, (38, 26, 40), 2)
        offset = 55 if ((y - 615) // 44) % 2 == 0 else 0
        for x in range(offset, 1920, 110):
            arcade.draw_line(x, y, x, y + 44, (38, 26, 40), 2)

    for wx in (420, 960, 1500):
        arcade.draw_rect_filled(arcade.XYWH(wx, 825, 90, 175), (52, 16, 22))
        arcade.draw_rect_outline(arcade.XYWH(wx, 825, 90, 175), (82, 34, 42), 3)

    for cx in (280, 740, 1180, 1640):
        draw_candle_holder(cx, 615, t, flame_color=(235, 75, 35))
    for sx in (340, 690, 1230, 1590):
        draw_skull_pile(sx, 615, scale=1.15)


def draw_undead_dungeon(t: float):
    draw_horizon_base((15, 21, 35), (15, 19, 28), (38, 52, 78))
    for y in range(615, 1080, 44):
        arcade.draw_line(0, y, 1920, y, (28, 38, 60), 2)
        offset = 55 if ((y - 615) // 44) % 2 == 0 else 0
        for x in range(offset, 1920, 110):
            arcade.draw_line(x, y, x, y + 44, (28, 38, 60), 2)

    for gx in (450, 1470):
        arcade.draw_rect_filled(arcade.XYWH(gx, 795, 130, 175), (8, 10, 16))
        for bar in range(gx - 50, gx + 60, 25):
            arcade.draw_line(bar, 708, bar, 882, (62, 74, 92), 4)

    for cx in (300, 760, 1160, 1620):
        draw_candle_holder(cx, 615, t, flame_color=(65, 210, 185))
    for sx in (360, 710, 1210, 1560):
        draw_skull_pile(sx, 615, scale=1.2)


def draw_ice_crown(t: float):
    draw_horizon_base(sky_color=(16, 25, 38), ground_color=(20, 28, 38), line_color=(72, 105, 135))
    peaks = (
        ((120, 615), (420, 960), (720, 615)),
        ((580, 615), (960, 1020), (1340, 615)),
        ((1180, 615), (1520, 945), (1860, 615)),
    )
    for p1, p2, p3 in peaks:
        arcade.draw_polygon_filled((p1, p2, p3), (32, 52, 76))
        cap_l = ((p1[0] + p2[0]) * 0.5, (p1[1] + p2[1]) * 0.5)
        cap_r = ((p3[0] + p2[0]) * 0.5, (p3[1] + p2[1]) * 0.5)
        arcade.draw_polygon_filled((cap_l, p2, cap_r), (150, 185, 215, 165))

    arcade.draw_ellipse_filled(360, 615, 460, 64, (130, 165, 195, 140))
    arcade.draw_ellipse_filled(1560, 615, 460, 64, (130, 165, 195, 140))

    for kx in (330, 1590):
        arcade.draw_rect_filled(arcade.XYWH(kx, 765, 54, 300), (64, 102, 138, 215))
        arcade.draw_rect_outline(arcade.XYWH(kx, 765, 54, 300), (145, 200, 235), 2)
        draw_skull_pile(kx, 615, scale=1.1)
        draw_candle_holder(kx + (55 if kx < 960 else -55), 615, t, flame_color=(95, 200, 255))


    for i in range(50):
        sx = (i * 173 - t * (190 + (i % 4) * 35)) % 1920
        sy = 460 + (i * 97 - t * (90 + (i % 3) * 25)) % 610
        arcade.draw_circle_filled(sx, sy, 2 + (i % 2), (210, 235, 255, 150))
