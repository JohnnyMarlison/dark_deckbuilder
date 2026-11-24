import math
import arcade


def draw_location_background(loc_name: str, t: float):
    """Отрисовывает детализированный задний план с выровненным горизонтом (y = 615)."""
    name = str(loc_name).strip().lower()
    if "лес" in name:
        _draw_dark_forest(t)
    elif "деревня" in name:
        _draw_abandoned_village(t)
    elif "лагерь" in name:
        _draw_bandit_camp(t)
    elif "склеп" in name:
        _draw_sand_crypt(t)
    elif "замок" in name or "замка" in name:
        _draw_ruined_castle(t)
    elif "колизей" in name:
        _draw_ruined_colosseum(t)
    elif "цитадель" in name:
        _draw_obsidian_citadel(t)
    elif "подземелье" in name or "мертвецов" in name:
        _draw_undead_dungeon(t)
    elif "ледяная" in name or "корона" in name:
        _draw_ice_crown(t)


def _draw_horizon_base(sky_color, ground_color, line_color):
    """Отрисовывает небо/стены (y = 615..1080) и землю под ареной (y = 410..615)."""
    arcade.draw_rect_filled(arcade.XYWH(960, 848, 1920, 465), sky_color)
    arcade.draw_rect_filled(arcade.XYWH(960, 512, 1920, 205), ground_color)
    arcade.draw_line(0, 615, 1920, 615, line_color, 2)


def _draw_candle_holder(x: float, y: float, t: float, flame_color=(245, 165, 45)):
    """Кованый подсвечник с мерцающим огнем."""
    arcade.draw_rect_filled(arcade.XYWH(x, y + 18, 8, 36), (65, 60, 58))
    arcade.draw_rect_filled(arcade.XYWH(x, y + 36, 22, 5), (85, 78, 72))
    for dx in (-8, 0, 8):
        arcade.draw_rect_filled(arcade.XYWH(x + dx, y + 44, 4, 12), (210, 200, 180))
        flicker = math.sin(t * 11.0 + x + dx) * 1.8
        arcade.draw_circle_filled(x + dx, y + 54, 5 + flicker * 0.4, (*flame_color, 110))
        arcade.draw_circle_filled(x + dx, y + 53, 3, (255, 235, 160))


def _draw_skull_pile(x: float, y: float, scale: float = 1.0):
    """Груда костей и черепов у подножия стен."""
    s = scale
    arcade.draw_line(x - 24 * s, y - 4 * s, x + 22 * s, y + 8 * s, (175, 168, 152), 4)
    arcade.draw_line(x - 18 * s, y + 10 * s, x + 26 * s, y - 3 * s, (155, 148, 134), 4)
    for cx, cy, r in ((x - 8 * s, y + 6 * s, 9 * s), (x + 11 * s, y + 3 * s, 8 * s)):
        arcade.draw_circle_filled(cx, cy, r, (195, 188, 172))
        arcade.draw_circle_filled(cx - 3 * s, cy, 2 * s, (20, 18, 22))
        arcade.draw_circle_filled(cx + 3 * s, cy, 2 * s, (20, 18, 22))


def _draw_dark_forest(t: float):
    _draw_horizon_base((12, 18, 16), (15, 20, 17), (36, 48, 38))
    arcade.draw_circle_filled(960, 955, 62, (165, 185, 165, 45))
    arcade.draw_circle_filled(960, 955, 44, (195, 210, 190, 90))

    # Болотные топи по бокам у кромки леса (y = 605)
    arcade.draw_ellipse_filled(330, 602, 360, 46, (24, 52, 36, 220))
    arcade.draw_ellipse_filled(1590, 602, 380, 50, (24, 52, 36, 220))

    # Мрачные деревья, растущие от линии горизонта y = 615
    trees = (130, 290, 460, 780, 1140, 1450, 1630, 1810)
    for i, tx in enumerate(trees):
        w = 26 if i % 2 == 0 else 18
        arcade.draw_rect_filled(arcade.XYWH(tx, 845, w, 460), (20, 25, 21))
        arcade.draw_line(tx, 860, tx - 65, 930, (20, 25, 21), 6)
        arcade.draw_line(tx, 900, tx + 70, 970, (20, 25, 21), 5)
        arcade.draw_circle_filled(tx, 1040, 115, (14, 24, 18, 235))

    # Паутина между деревьями
    for wx, wy in ((375, 890), (1540, 900)):
        for r in (20, 40, 60):
            arcade.draw_arc_outline(wx, wy, r * 2, r * 2, (170, 175, 175, 75), 180, 360, 1.5)
        arcade.draw_line(wx - 60, wy, wx + 60, wy, (170, 175, 175, 75), 1)
        arcade.draw_line(wx, wy, wx - 42, wy - 42, (170, 175, 175, 75), 1)
        arcade.draw_line(wx, wy, wx + 42, wy - 42, (170, 175, 175, 75), 1)

    # Ползущий болотный туман вдоль горизонта (y = 625)
    drift = math.sin(t * 0.7) * 65
    arcade.draw_ellipse_filled(620 + drift, 625, 680, 65, (120, 145, 130, 28))
    arcade.draw_ellipse_filled(1300 - drift, 620, 740, 72, (120, 145, 130, 28))


def _draw_abandoned_village(t: float):
    _draw_horizon_base((16, 16, 22), (19, 18, 23), (55, 48, 42))

    # Полуразрушенные избы (основание на y = 615)
    for hx, hw, hh in ((340, 240, 180), (1580, 250, 190)):
        arcade.draw_rect_filled(arcade.XYWH(hx, 615 + hh / 2, hw, hh), (38, 34, 32))
        arcade.draw_rect_outline(arcade.XYWH(hx, 615 + hh / 2, hw, hh), (62, 54, 48), 2)
        roof = ((hx - hw / 2 - 20, 615 + hh), (hx + hw / 2 + 20, 615 + hh), (hx - 15, 615 + hh + 105))
        arcade.draw_polygon_filled(roof, (28, 24, 22))
        arcade.draw_rect_filled(arcade.XYWH(hx - 45, 615 + hh * 0.55, 40, 48), (10, 10, 14))
        arcade.draw_rect_filled(arcade.XYWH(hx + 45, 615 + hh * 0.55, 40, 48), (10, 10, 14))

    # Поломанный забор у домов (y = 615)
    for fx in range(160, 1780, 46):
        if 480 <= fx <= 1430:
            continue
        tilt = math.sin(fx) * 7
        h = 56 + (fx % 3) * 12
        arcade.draw_line(fx, 615, fx + tilt, 615 + h, (58, 44, 32), 5)
    arcade.draw_line(150, 650, 475, 646, (52, 40, 28), 3)
    arcade.draw_line(1435, 646, 1770, 652, (52, 40, 28), 3)

    # Пучки высокой травы (y = 615)
    for gx in (210, 485, 690, 1230, 1430, 1710):
        for blade in (-10, -4, 3, 9):
            sway = math.sin(t * 2.5 + gx) * 4
            arcade.draw_line(gx + blade, 615, gx + blade * 1.6 + sway, 655, (44, 62, 36), 3)


def _draw_bandit_camp(t: float):
    _draw_horizon_base((18, 15, 16), (22, 18, 18), (62, 46, 36))

    # Потрепанные палатки разбойников (y = 615)
    for tx, tw, th in ((340, 260, 165), (1580, 270, 175)):
        tent = ((tx - tw / 2, 615), (tx + tw / 2, 615), (tx, 615 + th))
        arcade.draw_polygon_filled(tent, (78, 38, 30))
        arcade.draw_polygon_outline(tent, (110, 62, 46), 2)
        door = ((tx - 32, 615), (tx + 32, 615), (tx, 615 + th * 0.58))
        arcade.draw_polygon_filled(door, (14, 12, 14))

    # Ящики с провизией у палаток (y = 615)
    for bx, by in ((505, 632), (545, 628), (522, 665), (1390, 632), (1432, 628)):
        arcade.draw_rect_filled(arcade.XYWH(bx, by, 38, 34), (88, 60, 38))
        arcade.draw_rect_outline(arcade.XYWH(bx, by, 38, 34), (48, 32, 20), 2)
        arcade.draw_line(bx - 18, by - 16, bx + 18, by + 16, (48, 32, 20), 2)

    # Столбы с атрибутикой (y = 615)
    for px in (720, 1200):
        arcade.draw_line(px, 615, px, 825, (64, 44, 30), 7)
        arcade.draw_circle_filled(px, 833, 12, (195, 186, 168))

    # Флагшток с потрепанным знаменем разбойников по центру заднего плана
    arcade.draw_line(960, 615, 960, 895, (68, 48, 32), 8)
    wave = math.sin(t * 4.5) * 10
    flag = ((964, 890), (1075, 875 + wave), (1055, 845 + wave * 0.6), (1080, 820 + wave), (964, 815))
    arcade.draw_polygon_filled(flag, (128, 26, 26))

def _draw_sand_crypt(t: float):
    # Светлые каменные стены (y = 615..1080) и песчаный пол (y = 410..615)
    _draw_horizon_base((52, 45, 36), (32, 28, 22), (82, 72, 56))
    for y in range(615, 1080, 48):
        arcade.draw_line(0, y, 1920, y, (38, 33, 26), 2)
        offset = 60 if ((y - 615) // 48) % 2 == 0 else 0
        for x in range(offset, 1920, 120):
            arcade.draw_line(x, y, x, y + 48, (38, 33, 26), 2)

    # Каменные саркофаги (гробы) вдоль стены (y = 615)
    for cx in (340, 1580):
        coffin = ((cx - 55, 615), (cx + 55, 615), (cx + 70, 665), (cx - 70, 665))
        arcade.draw_polygon_filled(coffin, (96, 85, 68))
        arcade.draw_polygon_outline(coffin, (145, 128, 98), 2)
        arcade.draw_line(cx - 40, 640, cx + 40, 640, (145, 128, 98), 2)

    # Древние статуи стражей в нишах (y = 615)
    for sx in (680, 1240):
        arcade.draw_rect_filled(arcade.XYWH(sx, 755, 95, 250), (28, 24, 19))
        arcade.draw_rect_filled(arcade.XYWH(sx, 632, 64, 34), (102, 90, 72))
        arcade.draw_rect_filled(arcade.XYWH(sx, 712, 44, 125), (118, 105, 84))
        arcade.draw_circle_filled(sx, 792, 18, (118, 105, 84))
        _draw_candle_holder(sx + (65 if sx < 960 else -65), 615, t, flame_color=(235, 145, 45))


def _draw_ruined_castle(t: float):
    _draw_horizon_base((22, 24, 28), (20, 21, 25), (62, 66, 74))

    # Серые каменные стены с зубцами (основание на y = 615)
    arcade.draw_rect_filled(arcade.XYWH(320, 765, 560, 300), (48, 51, 58))
    arcade.draw_rect_filled(arcade.XYWH(1600, 765, 560, 300), (48, 51, 58))
    for bx in range(60, 580, 75):
        arcade.draw_rect_filled(arcade.XYWH(bx, 935, 45, 40), (48, 51, 58))
    for bx in range(1340, 1880, 75):
        arcade.draw_rect_filled(arcade.XYWH(bx, 935, 45, 40), (48, 51, 58))

    # Пробоины в стене
    arcade.draw_polygon_filled(((390, 700), (465, 720), (440, 810), (375, 785)), (16, 17, 22))
    arcade.draw_polygon_filled(((1480, 690), (1550, 715), (1530, 800), (1465, 770)), (16, 17, 22))

    # Сломанные деревянные ворота по центру (y = 615)
    arcade.draw_arc_outline(960, 615, 320, 430, (68, 72, 80), 0, 180, 18)
    arcade.draw_polygon_filled(((810, 615), (930, 615), (915, 790), (810, 810)), (62, 44, 30))
    arcade.draw_polygon_filled(((1110, 615), (995, 615), (1020, 740), (1110, 775)), (62, 44, 30))

    # Сломанная тележка у стены (y = 615)
    arcade.draw_polygon_filled(((460, 635), (565, 620), (555, 660), (450, 675)), (74, 52, 34))
    arcade.draw_circle_outline(485, 625, 20, (52, 36, 24), 4)
    arcade.draw_circle_outline(555, 618, 15, (52, 36, 24), 3)


def _draw_ruined_colosseum(t: float):
    _draw_horizon_base((26, 22, 20), (24, 21, 19), (66, 58, 50))

    # Ярусы разрушенного амфитеатра (y = 615)
    arcade.draw_arc_outline(960, 615, 1650, 560, (58, 52, 46), 0, 180, 26)
    arcade.draw_arc_outline(960, 615, 1420, 450, (48, 42, 37), 0, 180, 22)
    for ax in range(340, 1620, 160):
        arcade.draw_arc_filled(ax, 745, 75, 105, (16, 14, 15), 0, 180)

    # Разрушенные античные колонны (основание на y = 615)
    columns = ((290, 255), (440, 150), (1480, 175), (1630, 275))
    for cx, ch in columns:
        arcade.draw_rect_filled(arcade.XYWH(cx, 615 + ch / 2, 48, ch), (98, 90, 80))
        arcade.draw_rect_filled(arcade.XYWH(cx, 623, 64, 16), (78, 72, 64))
        arcade.draw_polygon_filled(((cx - 24, 615 + ch), (cx + 24, 615 + ch), (cx - 10, 615 + ch + 22)), (98, 90, 80))

    # Следы битвы у подножия трибун (y = 615)
    arcade.draw_line(740, 615, 760, 670, (155, 160, 165), 4)
    arcade.draw_ellipse_filled(1180, 622, 52, 20, (92, 68, 44))


def _draw_obsidian_citadel(t: float):
    # Темные кирпичные стены (y = 615..1080)
    _draw_horizon_base((20, 15, 22), (18, 15, 20), (65, 32, 38))
    for y in range(615, 1080, 44):
        arcade.draw_line(0, y, 1920, y, (38, 26, 40), 2)
        offset = 55 if ((y - 615) // 44) % 2 == 0 else 0
        for x in range(offset, 1920, 110):
            arcade.draw_line(x, y, x, y + 44, (38, 26, 40), 2)

    # Готические окна цитадели
    for wx in (420, 960, 1500):
        arcade.draw_rect_filled(arcade.XYWH(wx, 825, 90, 175), (52, 16, 22))
        arcade.draw_rect_outline(arcade.XYWH(wx, 825, 90, 175), (82, 34, 42), 3)

    # Подсвечники и груды скелетов вдоль стены (y = 615)
    for cx in (280, 740, 1180, 1640):
        _draw_candle_holder(cx, 615, t, flame_color=(235, 75, 35))
    for sx in (340, 690, 1230, 1590):
        _draw_skull_pile(sx, 615, scale=1.15)


def _draw_undead_dungeon(t: float):
    # Темно-синие кирпичные стены (y = 615..1080)
    _draw_horizon_base((15, 21, 35), (15, 19, 28), (38, 52, 78))
    for y in range(615, 1080, 44):
        arcade.draw_line(0, y, 1920, y, (28, 38, 60), 2)
        offset = 55 if ((y - 615) // 44) % 2 == 0 else 0
        for x in range(offset, 1920, 110):
            arcade.draw_line(x, y, x, y + 44, (28, 38, 60), 2)

    # Решетки темницы
    for gx in (450, 1470):
        arcade.draw_rect_filled(arcade.XYWH(gx, 795, 130, 175), (8, 10, 16))
        for bar in range(gx - 50, gx + 60, 25):
            arcade.draw_line(bar, 708, bar, 882, (62, 74, 92), 4)

    # Подсвечники с бирюзовым огнем и груды черепов (y = 615)
    for cx in (300, 760, 1160, 1620):
        _draw_candle_holder(cx, 615, t, flame_color=(65, 210, 185))
    for sx in (360, 710, 1210, 1560):
        _draw_skull_pile(sx, 615, scale=1.2)


def _draw_ice_crown(t: float):
    # Морозное темно-лазурное небо и ледяная земля (y = 615)
    _draw_horizon_base((16, 25, 38), (20, 28, 38), (72, 105, 135))

    # Ледяные пики гор, вырастающие от линии горизонта y = 615
    peaks = (
        ((120, 615), (420, 960), (720, 615)),
        ((580, 615), (960, 1020), (1340, 615)),
        ((1180, 615), (1520, 945), (1860, 615)),
    )
    for p1, p2, p3 in peaks:
        arcade.draw_polygon_filled((p1, p2, p3), (32, 52, 76))
        cap_l = ((p1 + p2) * 0.5, (p1 + p2) * 0.5)
        cap_r = ((p3 + p2) * 0.5, (p3 + p2) * 0.5)
        arcade.draw_polygon_filled((cap_l, p2, cap_r), (150, 185, 215, 165))

    # Снежные холмы вдоль горизонта (y = 615)
    arcade.draw_ellipse_filled(360, 615, 460, 64, (130, 165, 195, 140))
    arcade.draw_ellipse_filled(1560, 615, 460, 64, (130, 165, 195, 140))

    # Ледяные колонны с черепами и подсвечниками (y = 615)
    for kx in (330, 1590):
        arcade.draw_rect_filled(arcade.XYWH(kx, 765, 54, 300), (64, 102, 138, 215))
        arcade.draw_rect_outline(arcade.XYWH(kx, 765, 54, 300), (145, 200, 235), 2)
        _draw_skull_pile(kx, 615, scale=1.1)
        _draw_candle_holder(kx + (55 if kx < 960 else -55), 615, t, flame_color=(95, 200, 255))

    # Снежная метель по всей верхней зоне
    for i in range(50):
        sx = (i * 173 - t * (190 + (i % 4) * 35)) % 1920
        sy = 460 + (i * 97 - t * (90 + (i % 3) * 25)) % 610
        arcade.draw_circle_filled(sx, sy, 2 + (i % 2), (210, 235, 255, 150))
