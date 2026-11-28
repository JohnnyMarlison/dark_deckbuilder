import math
import arcade


def _draw_warrior_knight(cx: float, cy: float, s: float, d: float, t: float, b: float):
    """Детализированный спрайт Воина по референсу (индиговое сюрко с орлами, меч наперевес, гербовый щит)."""
    shield_sway = math.sin(t * 2.0) * 1.2 * s
    cloth_sway = math.sin(t * 2.2) * 1.8 * s

    indigo_mid = (72, 74, 102)
    indigo_dark = (44, 46, 68)
    indigo_light = (98, 102, 134)
    steel_light = (186, 192, 200)
    steel_mid = (124, 130, 140)
    steel_dark = (58, 62, 70)
    chainmail = (76, 80, 88)
    leather = (68, 52, 42)
    eagle_silver = (218, 224, 232)

    def _draw_mini_eagle(ex: float, ey: float, es: float):
        """Стилизованный серебряный геральдический орёл."""
        arcade.draw_ellipse_filled(ex, ey, 3.2 * es, 7.5 * es, eagle_silver)
        arcade.draw_circle_filled(ex, ey + 5 * es, 2.0 * es, eagle_silver)
        left_wing = (
            (ex - 1 * es, ey + 3 * es),
            (ex - 9 * es, ey + 5 * es),
            (ex - 10 * es, ey - 2 * es),
            (ex - 2 * es, ey - 2 * es),
        )
        right_wing = (
            (ex + 1 * es, ey + 3 * es),
            (ex + 9 * es, ey + 5 * es),
            (ex + 10 * es, ey - 2 * es),
            (ex + 2 * es, ey - 2 * es),
        )
        arcade.draw_polygon_filled(left_wing, eagle_silver)
        arcade.draw_polygon_filled(right_wing, eagle_silver)
        tail = ((ex - 3 * es, ey - 3 * es), (ex + 3 * es, ey - 3 * es), (ex, ey - 8 * es))
        arcade.draw_polygon_filled(tail, eagle_silver)

    # 1. Тёмно-индиговый плащ за спиной
    cloak = (
        (cx - 19 * d * s, cy + 28 * s + b),
        (cx + 18 * d * s, cy + 28 * s + b),
        (cx + 28 * d * s + cloth_sway, cy - 46 * s),
        (cx - 32 * d * s + cloth_sway, cy - 48 * s),
    )
    arcade.draw_polygon_filled(cloak, indigo_dark)
    arcade.draw_polygon_outline(cloak, (32, 34, 48), 1.5)

    # 2. Кольчуга и стальные поножи с тёмными сабатонами
    for side, lx, shift_x in ((-1, cx - 11 * d * s, -4), (1, cx + 10 * d * s, 5)):
        kx = lx + shift_x * 0.4 * d * s
        ky = cy - 22 * s
        fx = lx + shift_x * d * s
        fy = cy - 48 * s

        arcade.draw_line(lx, cy - 4 * s, kx, ky, chainmail, 9.5)
        arcade.draw_line(kx, ky, fx, fy, steel_mid if side > 0 else steel_dark, 9)
        arcade.draw_line(kx + 2 * d * s, ky, fx + 2 * d * s, fy, steel_light, 1.8)
        arcade.draw_ellipse_filled(kx + 1 * d * s, ky, 10 * s, 9 * s, steel_mid)

        boot = (
            (fx - 4 * s, cy - 52 * s),
            (fx + 10 * d * s, cy - 52 * s),
            (fx + 7 * d * s, cy - 45 * s),
            (fx - 4 * s, cy - 46 * s),
        )
        arcade.draw_polygon_filled(boot, (28, 30, 34))

    # 3. Расходящиеся полы тёмно-индигового сюрко с серебряными орлами и кольчугой под ними
    arcade.draw_polygon_filled(
        ((cx - 8 * d * s, cy - 4 * s), (cx + 8 * d * s, cy - 4 * s), (cx + 11 * d * s, cy - 30 * s), (cx - 10 * d * s, cy - 30 * s)),
        chainmail,
    )

    left_flap = (
        (cx - 14 * d * s, cy - 2 * s),
        (cx - 1 * d * s, cy - 2 * s),
        (cx - 5 * d * s + cloth_sway * 0.4, cy - 38 * s),
        (cx - 23 * d * s + cloth_sway * 0.5, cy - 36 * s),
    )
    right_flap = (
        (cx + 2 * d * s, cy - 2 * s),
        (cx + 15 * d * s, cy - 2 * s),
        (cx + 21 * d * s + cloth_sway * 0.5, cy - 36 * s),
        (cx + 7 * d * s + cloth_sway * 0.4, cy - 38 * s),
    )
    arcade.draw_polygon_filled(left_flap, indigo_mid)
    arcade.draw_polygon_outline(left_flap, leather, 1.4)
    arcade.draw_polygon_filled(right_flap, indigo_dark)
    arcade.draw_polygon_outline(right_flap, leather, 1.4)

    # Малые серебряные орлы на обеих полах сюрко
    _draw_mini_eagle(cx - 12 * d * s + cloth_sway * 0.3, cy - 27 * s, 0.72 * s)
    _draw_mini_eagle(cx + 12 * d * s + cloth_sway * 0.3, cy - 27 * s, 0.68 * s)

    # 4. Кираса-сюрко с орлом на груди, двойной кожаный пояс и ножны кинжала
    torso = (
        (cx - 14 * d * s, cy - 1 * s),
        (cx - 19 * d * s, cy + 28 * s + b),
        (cx + 19 * d * s, cy + 28 * s + b),
        (cx + 14 * d * s, cy - 1 * s),
    )
    arcade.draw_polygon_filled(torso, indigo_mid)
    arcade.draw_polygon_outline(torso, indigo_dark, 1.6)

    # Гербовый орёл на груди
    _draw_mini_eagle(cx + 1 * d * s, cy + 14 * s + b * 0.85, 0.95 * s)

    # Двойной кожаный пояс с пряжкой и ножны кинжала на бедре
    belt_y = cy - 1 * s + b * 0.4
    arcade.draw_line(cx - 15 * d * s, belt_y + 2 * s, cx + 15 * d * s, belt_y - 2 * s, leather, 4.5)
    arcade.draw_line(cx - 15 * d * s, belt_y - 3 * s, cx + 15 * d * s, belt_y + 1 * s, (42, 30, 24), 4)
    arcade.draw_rect_outline(arcade.XYWH(cx + 2 * d * s, belt_y - 1 * s, 5 * s, 5.5 * s), steel_light, 1.4)

    # Ножны кинжала слева у пояса
    arcade.draw_line(cx - 9 * d * s, belt_y + 2 * s, cx - 14 * d * s, belt_y - 18 * s, (46, 34, 28), 3.8)
    arcade.draw_line(cx - 12 * d * s, belt_y + 1 * s, cx - 6 * d * s, belt_y + 3 * s, steel_mid, 2.5)

    # 5. Тёмный кольчужный воротник, сегментированные наплечники и круглый безаг с орлом
    arcade.draw_ellipse_filled(cx, cy + 28 * s + b, 30 * s, 10 * s, (38, 40, 46))
    arcade.draw_ellipse_outline(cx, cy + 28 * s + b, 30 * s, 10 * s, chainmail, 1.4)

    for side in (-1, 1):
        px = cx + side * 19 * d * s
        py = cy + 25 * s + b
        for tier in range(3):
            ty = py - tier * 4.2 * s
            plate = (
                (px - side * 5 * d * s, ty + 4 * s),
                (px + side * (11 - tier * 0.8) * d * s, ty + 2 * s),
                (px + side * (12 - tier * 0.8) * d * s, ty - 3 * s),
                (px - side * 4 * d * s, ty - 2 * s),
            )
            arcade.draw_polygon_filled(plate, steel_light if side < 0 else steel_mid)
            arcade.draw_polygon_outline(plate, steel_dark, 1.3)

    # Круглый гербовый щиток-безаг на правом плече (фирменная деталь с арта)
    bes_x = cx - 13 * d * s
    bes_y = cy + 19 * s + b * 0.9
    arcade.draw_circle_filled(bes_x, bes_y, 6.5 * s, indigo_dark)
    arcade.draw_circle_outline(bes_x, bes_y, 6.5 * s, steel_light, 1.6)
    _draw_mini_eagle(bes_x, bes_y - 0.5 * s, 0.45 * s)

    # 6. Закрытый цилиндрический топхельм
    hx = cx
    hy = cy + 41 * s + b
    helm = (
        (hx - 8.5 * s, hy - 7 * s),
        (hx - 8.5 * s, hy + 9 * s),
        (hx, hy + 13 * s),
        (hx + 8.5 * s, hy + 9 * s),
        (hx + 8.5 * s, hy - 7 * s),
        (hx, hy - 10 * s),
    )
    arcade.draw_polygon_filled(helm, steel_mid)
    arcade.draw_polygon_outline(helm, steel_dark, 1.6)
    arcade.draw_arc_filled(hx, hy + 8 * s, 16 * s, 7 * s, steel_light, 0, 180)

    # Вертикальный наносник, глазная щель и вентиляционные отверстия
    arcade.draw_line(hx, hy + 12 * s, hx, hy - 9 * s, steel_dark, 2.2)
    arcade.draw_line(hx - 7.5 * s, hy + 2.5 * s, hx + 7.5 * s, hy + 2.5 * s, (22, 22, 26), 2.5)
    for vx in (-4.5, -2.2, 2.2, 4.5):
        for vy in (-1.5, -4.5):
            arcade.draw_circle_filled(hx + vx * s, hy + vy * s, 0.8 * s, (26, 26, 30))

    # 7. Правая рука с длинным мечом наперевес (по диагонали вверх вправо перед грудью)
    sh_rx, sh_ry = cx - 19 * d * s, cy + 21 * s + b
    el_rx, el_ry = cx - 27 * d * s, cy + 12 * s + b * 0.8
    hd_rx, hd_ry = cx - 18 * d * s, cy + 4 * s + b * 0.6

    arcade.draw_line(sh_rx, sh_ry, el_rx, el_ry, steel_mid, 8)
    arcade.draw_ellipse_filled(el_rx, el_ry, 8 * s, 7 * s, steel_light)
    arcade.draw_line(el_rx, el_ry, hd_rx, hd_ry, steel_light, 7.5)

    # Длинный прямой клинок наперевес вверх вправо (как на референсе)
    tip_x = cx + 29 * d * s
    tip_y = cy + 28 * s + b * 0.9
    blade_top = ((hd_rx + 2 * d * s, hd_ry + 2.5 * s), (hd_rx + 3.5 * d * s, hd_ry + 0.5 * s), (tip_x, tip_y))
    blade_bot = ((hd_rx + 3.5 * d * s, hd_ry + 0.5 * s), (hd_rx + 5 * d * s, hd_ry - 1.5 * s), (tip_x, tip_y))
    arcade.draw_polygon_filled(blade_top, steel_light)
    arcade.draw_polygon_filled(blade_bot, steel_mid)
    arcade.draw_polygon_outline(
        ((hd_rx + 2 * d * s, hd_ry + 2.5 * s), (tip_x, tip_y), (hd_rx + 5 * d * s, hd_ry - 1.5 * s)),
        steel_dark,
        1.4,
    )

    # Изогнутая гарда, рукоять и латная рукавица
    arcade.draw_line(hd_rx + 1 * d * s, hd_ry + 8 * s, hd_rx + 6 * d * s, hd_ry - 6 * s, steel_mid, 4.2)
    arcade.draw_line(hd_rx + 2 * d * s, hd_ry + 1 * s, hd_rx - 8 * d * s, hd_ry - 4 * s, (42, 34, 30), 3.8)
    arcade.draw_circle_filled(hd_rx - 9 * d * s, hd_ry - 4.5 * s, 2.8 * s, steel_light)
    arcade.draw_circle_filled(hd_rx, hd_ry, 4.5 * s, steel_mid)
    arcade.draw_circle_outline(hd_rx, hd_ry, 4.5 * s, steel_dark, 1.3)

    # 8. Высокий заострённый щит в левой руке (двухцветный индиго/графит + крупный серебряный орёл)
    sx = cx + 21 * d * s
    sy = cy - 4 * s + b * 0.6 + shield_sway

    shield_outer = (
        (sx - 13 * d * s, sy + 24 * s),
        (sx + 13 * d * s, sy + 16 * s),
        (sx + 16 * d * s, sy - 26 * s),
        (sx + 2 * d * s, sy - 16 * s),
        (sx - 13 * d * s, sy - 6 * s),
    )
    # Делаем классический каплевидно-треугольный щит как на фото
    shield_outer = (
        (sx - 13 * d * s, sy + 24 * s),
        (sx + 13 * d * s, sy + 16 * s),
        (sx + 16 * d * s, sy - 27 * s),
        (sx + 1 * d * s, sy - 18 * s),
        (sx - 13 * d * s, sy - 6 * s),
    )
    shield_outer = (
        (sx - 14 * d * s, sy + 24 * s),
        (sx + 12 * d * s, sy + 16 * s),
        (sx + 15 * d * s, sy - 26 * s),
        (sx - 12 * d * s, sy - 7 * s),
    )
    # Левая половина щита (индиго) и правая половина (тёмный графит)
    mid_top = (sx - 1 * d * s, sy + 20 * s)
    mid_bot = (sx + 15 * d * s, sy - 26 * s)
    left_half = ((sx - 14 * d * s, sy + 24 * s), mid_top, mid_bot, (sx - 12 * d * s, sy - 7 * s))
    right_half = (mid_top, (sx + 12 * d * s, sy + 16 * s), mid_bot)

    arcade.draw_polygon_filled(left_half, indigo_light)
    arcade.draw_polygon_filled(right_half, indigo_dark)
    arcade.draw_polygon_outline(shield_outer, steel_light, 2.0)



def _draw_elementalist(cx: float, cy: float, s: float, d: float, t: float, b: float):
    """Детализированный спрайт Элементалиста по референсу (рогатый воротник, 3 сферы стихий)."""
    orb_bob1 = math.sin(t * 3.0) * 3.0 * s
    orb_bob2 = math.sin(t * 3.0 + 2.1) * 3.0 * s
    orb_bob3 = math.sin(t * 3.0 + 4.2) * 3.0 * s
    cloak_sway = math.sin(t * 2.0) * 2.5 * s

    robe_dark = (28, 18, 28)
    robe_plum = (58, 30, 48)
    robe_mid = (84, 42, 64)
    bronze = (176, 134, 96)
    bronze_light = (224, 184, 142)
    skin_pale = (228, 198, 182)
    hair_silver = (232, 232, 236)

    # 1. Тяжёлый тёмно-сливовый плащ за спиной с бронзовой каймой
    back_cape = (
        (cx - 24 * d * s, cy + 28 * s + b),
        (cx + 22 * d * s, cy + 28 * s + b),
        (cx + 34 * d * s + cloak_sway * 0.5, cy - 48 * s),
        (cx - 38 * d * s + cloak_sway, cy - 52 * s),
        (cx - 44 * d * s + cloak_sway, cy - 36 * s),
    )
    arcade.draw_polygon_filled(back_cape, robe_dark)
    arcade.draw_polygon_outline(back_cape, bronze, 1.6)

    # 2. Высокие изогнутые рога-дуги воротника за плечами (фирменный силуэт с арта)
    left_horn = (
        (cx - 12 * d * s, cy + 26 * s + b),
        (cx - 32 * d * s, cy + 36 * s + b),
        (cx - 34 * d * s, cy + 62 * s + b),
        (cx - 22 * d * s, cy + 56 * s + b),
        (cx - 22 * d * s, cy + 38 * s + b),
        (cx - 8 * d * s, cy + 31 * s + b),
    )
    right_horn = (
        (cx + 10 * d * s, cy + 28 * s + b),
        (cx + 24 * d * s, cy + 42 * s + b),
        (cx + 22 * d * s, cy + 62 * s + b),
        (cx + 31 * d * s, cy + 55 * s + b),
        (cx + 30 * d * s, cy + 34 * s + b),
        (cx + 14 * d * s, cy + 24 * s + b),
    )
    arcade.draw_polygon_filled(left_horn, robe_plum)
    arcade.draw_polygon_outline(left_horn, bronze_light, 1.8)
    arcade.draw_polygon_filled(right_horn, robe_plum)
    arcade.draw_polygon_outline(right_horn, bronze_light, 1.8)

    # 3. Ноги в тёмных сапогах и длинный кафтан с центральным табардом
    for lx, fx in ((cx - 11 * d * s, cx - 15 * d * s), (cx + 11 * d * s, cx + 16 * d * s)):
        arcade.draw_line(lx, cy - 4 * s, fx, cy - 49 * s, (22, 16, 24), 9)
        arcade.draw_ellipse_filled(fx + 3 * d * s, cy - 50 * s, 13 * s, 6 * s, (18, 14, 20))

    # Боковые фалды мантии
    skirt_sides = (
        (cx - 15 * d * s, cy - 1 * s),
        (cx + 15 * d * s, cy - 1 * s),
        (cx + 25 * d * s, cy - 42 * s),
        (cx - 23 * d * s, cy - 42 * s),
    )
    arcade.draw_polygon_filled(skirt_sides, robe_dark)
    arcade.draw_polygon_outline(skirt_sides, robe_mid, 1.4)

    # Центральная заострённая пола-табард с бронзовой каймой и ромбами
    tabard = (
        (cx - 8 * d * s, cy - 2 * s),
        (cx + 8 * d * s, cy - 2 * s),
        (cx + 13 * d * s + cloak_sway * 0.3, cy - 35 * s),
        (cx + 1 * d * s + cloak_sway * 0.3, cy - 47 * s),
        (cx - 11 * d * s + cloak_sway * 0.3, cy - 35 * s),
    )
    arcade.draw_polygon_filled(tabard, robe_plum)
    arcade.draw_polygon_outline(tabard, bronze_light, 1.8)
    # Ромбовидный узор внизу табарда
    dy = cy - 37 * s
    dx = cx + 1 * d * s + cloak_sway * 0.3
    arcade.draw_polygon_outline(
        ((dx, dy + 6 * s), (dx + 5 * s, dy), (dx, dy - 6 * s), (dx - 5 * s, dy)),
        bronze_light,
        1.5,
    )

    # Цепь на поясе слева
    for i in range(5):
        arcade.draw_circle_outline(cx - (6 + i * 2.2) * d * s, cy - (4 + i * 4.5) * s, 2.2 * s, bronze, 1.3)

    # 4. Нагрудник с бронзовым орнаментом и пояс с самоцветами
    chest = (
        (cx - 15 * d * s, cy - 1 * s),
        (cx - 21 * d * s, cy + 26 * s + b),
        (cx + 21 * d * s, cy + 26 * s + b),
        (cx + 15 * d * s, cy - 1 * s),
    )
    arcade.draw_polygon_filled(chest, robe_plum)
    arcade.draw_polygon_outline(chest, bronze, 1.6)
    # Бронзовый V-образный нагрудный узор
    arcade.draw_line(cx - 13 * d * s, cy + 24 * s + b, cx + 1 * d * s, cy + 5 * s + b * 0.6, bronze_light, 2.2)
    arcade.draw_line(cx + 13 * d * s, cy + 24 * s + b, cx + 1 * d * s, cy + 5 * s + b * 0.6, bronze_light, 2.2)

    # Пояс с двумя круглыми медальонами
    belt_y = cy - 1 * s + b * 0.4
    arcade.draw_line(cx - 16 * d * s, belt_y + 1 * s, cx + 16 * d * s, belt_y - 1 * s, (46, 24, 34), 5.5)
    arcade.draw_circle_filled(cx + 1 * d * s, belt_y, 3.8 * s, (168, 42, 58))
    arcade.draw_circle_outline(cx + 1 * d * s, belt_y, 3.8 * s, bronze_light, 1.4)
    arcade.draw_circle_filled(cx + 7 * d * s, belt_y, 3.0 * s, (168, 42, 58))
    arcade.draw_circle_outline(cx + 7 * d * s, belt_y, 3.0 * s, bronze_light, 1.2)

    # 5. Массивные изогнутые наплечники и широкие расклешённые рукава
    for side in (-1, 1):
        px = cx + side * 22 * d * s
        py = cy + 25 * s + b
        pauldron = (
            (px - side * 7 * d * s, py + 6 * s),
            (px + side * 15 * d * s, py + 4 * s),
            (px + side * 17 * d * s, py - 9 * s),
            (px - side * 5 * d * s, py - 7 * s),
        )
        arcade.draw_polygon_filled(pauldron, robe_dark)
        arcade.draw_polygon_outline(pauldron, bronze_light, 1.8)
        # Изогнутые бронзовые когти-накладки на груди
        claw = (
            (px - side * 4 * d * s, py - 2 * s),
            (px - side * 11 * d * s, py - 11 * s),
            (px - side * 5 * d * s, py - 13 * s),
        )
        arcade.draw_polygon_filled(claw, bronze_light)

    # Левый (задний) широкий рукав и раскрытая ладонь
    sh_lx, sh_ly = cx - 21 * d * s, cy + 18 * s + b
    hd_lx, hd_ly = cx - 32 * d * s, cy + 2 * s + b * 0.6
    sleeve_l = (
        (sh_lx, sh_ly + 4 * s),
        (hd_lx + 2 * d * s, hd_ly + 6 * s),
        (hd_lx - 6 * d * s, hd_ly - 14 * s),
        (cx - 18 * d * s, cy + 1 * s + b * 0.5),
    )
    arcade.draw_polygon_filled(sleeve_l, robe_plum)
    arcade.draw_polygon_outline(sleeve_l, bronze, 1.5)
    arcade.draw_circle_filled(hd_lx, hd_ly, 4.2 * s, skin_pale)

    # Правый (передний) широкий рукав с синим отворотом и вытянутой рукой
    sh_rx, sh_ry = cx + 21 * d * s, cy + 18 * s + b
    hd_rx, hd_ry = cx + 41 * d * s, cy + 6 * s + b * 0.6
    sleeve_r = (
        (sh_rx, sh_ry + 4 * s),
        (hd_rx - 3 * d * s, hd_ry + 5 * s),
        (hd_rx - 8 * d * s, hd_ry - 15 * s),
        (cx + 18 * d * s, cy + 2 * s + b * 0.5),
    )
    arcade.draw_polygon_filled(sleeve_r, robe_plum)
    arcade.draw_polygon_outline(sleeve_r, bronze, 1.5)
    arcade.draw_circle_filled(hd_rx, hd_ry, 4.0 * s, skin_pale)

    # 6. Голова, длинные платиновые волосы и светящиеся белые глаза
    hx = cx + 1 * d * s
    hy = cy + 37 * s + b
    arcade.draw_ellipse_filled(hx, hy, 12 * s, 15 * s, skin_pale)
    # Светящиеся белые глаза
    arcade.draw_circle_filled(hx - 2.5 * d * s, hy + 1.5 * s, 1.6 * s, (255, 255, 255))
    arcade.draw_circle_filled(hx + 3.2 * d * s, hy + 1.5 * s, 1.6 * s, (255, 255, 255))

    # Длинные платиново-белые волосы, спадающие на плечи и грудь
    hair_l = (
        (hx - 6 * d * s, hy + 6 * s),
        (hx - 10 * d * s, hy - 14 * s),
        (hx - 6 * d * s, hy - 22 * s),
        (hx - 3 * d * s, hy - 2 * s),
    )
    hair_r = (
        (hx + 6 * d * s, hy + 6 * s),
        (hx + 11 * d * s, hy - 16 * s),
        (hx + 6 * d * s, hy - 24 * s),
        (hx + 3 * d * s, hy - 2 * s),
    )
    arcade.draw_polygon_filled(hair_l, hair_silver)
    arcade.draw_polygon_filled(hair_r, hair_silver)
    arcade.draw_arc_filled(hx, hy + 5 * s, 14 * s, 10 * s, hair_silver, 0, 180)

    # 7. ТРИ ПАРЯЩИЕ СТИХИЙНЫЕ СФЕРЫ (Огонь слева, Молния сверху, Лёд справа)
    # Сфера 1: Огненная (слева)
    o1x, o1y = cx - 44 * d * s, cy + 32 * s + orb_bob1
    arcade.draw_circle_filled(o1x, o1y, 14 * s, (255, 145, 25, 65))
    arcade.draw_circle_filled(o1x, o1y, 9.5 * s, (42, 22, 16, 210))
    arcade.draw_circle_filled(o1x - 1.5 * d * s, o1y, 7 * s, (255, 165, 32))
    arcade.draw_circle_filled(o1x - 1.5 * d * s, o1y, 4 * s, (255, 245, 165))

    # Сфера 2: Тайная пурпурная (сверху над головой)
    o2x, o2y = cx - 10 * d * s, cy + 72 * s + orb_bob2
    arcade.draw_circle_filled(o2x, o2y, 15 * s, (215, 75, 245, 65))
    arcade.draw_circle_filled(o2x, o2y, 9 * s, (195, 65, 235, 210))
    arcade.draw_circle_filled(o2x, o2y, 4.5 * s, (255, 195, 255))

    # Сфера 3: Ледяная голубая (справа)
    o3x, o3y = cx + 48 * d * s, cy + 28 * s + orb_bob3
    arcade.draw_circle_filled(o3x, o3y, 15 * s, (45, 165, 255, 65))
    arcade.draw_circle_filled(o3x, o3y, 9.5 * s, (42, 155, 245, 215))
    arcade.draw_circle_filled(o3x, o3y, 4.8 * s, (185, 240, 255))

    # Энергетические нити от сфер к чародею
    arcade.draw_line(o1x + 6 * d * s, o1y + 4 * s, o2x - 6 * d * s, o2y - 4 * s, (235, 135, 225, 110), 1.5)
    arcade.draw_line(o3x - 6 * d * s, o3y + 4 * s, cx + 24 * d * s, cy + 44 * s + b, (115, 205, 255, 130), 1.6)


def _draw_paladin(cx: float, cy: float, s: float, d: float, t: float, b: float):
    """Детализированный спрайт Паладина по референсу (золотой нимб, боевой молот, башенный щит)."""
    halo_pulse = math.sin(t * 3.0) * 1.5 * s
    cape_sway = math.sin(t * 2.2) * 3.5 * s
    shield_sway = math.sin(t * 2.0) * 1.2 * s

    armor_dark = (36, 38, 44)
    armor_mid = (72, 76, 84)
    armor_light = (148, 156, 168)
    gold = (228, 178, 62)
    gold_bright = (255, 224, 115)
    gold_dark = (146, 102, 28)
    cloak_ivory = (236, 228, 206)
    cloak_gold = (212, 168, 72)

    # 1. Сияющий золотой нимб и мягкая аура света за спиной
    hx = cx + 1 * d * s
    hy = cy + 42 * s + b
    arcade.draw_circle_filled(hx, hy + 2 * s, 26 * s + halo_pulse, (255, 205, 65, 45))
    arcade.draw_circle_outline(hx, hy + 2 * s, 21 * s + halo_pulse * 0.5, (255, 215, 85, 140), 4.5)
    arcade.draw_circle_outline(hx, hy + 2 * s, 21 * s + halo_pulse * 0.5, gold_bright, 2.0)

    # 2. Широкий развевающийся бело-золотой плащ за спиной
    cape = (
        (cx - 18 * d * s, cy + 28 * s + b),
        (cx + 16 * d * s, cy + 28 * s + b),
        (cx + 22 * d * s + cape_sway * 0.5, cy - 48 * s),
        (cx - 12 * d * s + cape_sway * 0.8, cy - 46 * s),
        (cx - 38 * d * s + cape_sway, cy - 38 * s),
        (cx - 46 * d * s + cape_sway, cy - 22 * s),
    )
    arcade.draw_polygon_filled(cape, cloak_gold)
    arcade.draw_polygon_outline(cape, cloak_ivory, 1.8)
    # Светлая драпировка плаща сверху
    cape_top = (
        (cx - 18 * d * s, cy + 28 * s + b),
        (cx + 14 * d * s, cy + 28 * s + b),
        (cx - 16 * d * s + cape_sway * 0.6, cy - 18 * s),
        (cx - 38 * d * s + cape_sway, cy - 22 * s),
    )
    arcade.draw_polygon_filled(cape_top, cloak_ivory)

    # 3. Поднятая правая рука с массивным двуручным боевым молотом Света
    sh_rx, sh_ry = cx - 18 * d * s, cy + 22 * s + b
    el_rx, el_ry = cx - 28 * d * s, cy + 12 * s + b * 0.8
    hd_rx, hd_ry = cx - 34 * d * s, cy + 22 * s + b * 0.9

    arcade.draw_line(sh_rx, sh_ry, el_rx, el_ry, armor_mid, 7.5)
    arcade.draw_line(el_rx, el_ry, hd_rx, hd_ry, armor_dark, 7)
    arcade.draw_line(el_rx - 2 * d * s, el_ry, hd_rx - 2 * d * s, hd_ry, gold, 1.5)

    # Длинная рукоять молота с золотыми кольцами
    shaft_bot = (hd_rx + 2 * d * s, hd_ry - 28 * s)
    shaft_top = (hd_rx - 3 * d * s, hd_ry + 36 * s)
    arcade.draw_line(*shaft_bot, *shaft_top, (88, 56, 38), 4.5)
    for ry in (-24, -12, 12, 22):
        arcade.draw_circle_filled(hd_rx - (ry * 0.08) * d * s, hd_ry + ry * s, 3.2 * s, gold)

    # Тяжёлый прямоугольный боёк молота с золотой резьбой и навершием
    mx = hd_rx - 2.5 * d * s
    my = hd_ry + 29 * s
    arcade.draw_rect_filled(arcade.XYWH(mx, my, 24 * s, 14 * s), (156, 136, 94))
    arcade.draw_rect_outline(arcade.XYWH(mx, my, 24 * s, 14 * s), gold_bright, 1.6)
    # Боковые ударные пластины и узор
    arcade.draw_rect_filled(arcade.XYWH(mx - 12 * s, my, 4 * s, 16 * s), gold_dark)
    arcade.draw_rect_filled(arcade.XYWH(mx + 12 * s, my, 4 * s, 16 * s), gold_dark)
    arcade.draw_rect_outline(arcade.XYWH(mx, my, 14 * s, 8 * s), gold_bright, 1.2)
    arcade.draw_circle_filled(mx, my + 9 * s, 3 * s, gold_bright)

    # Латная перчатка на рукояти
    arcade.draw_circle_filled(hd_rx, hd_ry, 4.5 * s, armor_mid)
    arcade.draw_circle_outline(hd_rx, hd_ry, 4.5 * s, gold, 1.3)

    # 4. Латные ноги в динамичном шаге, наколенники и белая набедренная пола
    # Задняя нога
    arcade.draw_line(cx - 8 * d * s, cy - 3 * s, cx - 12 * d * s, cy - 25 * s, armor_dark, 9.5)
    arcade.draw_line(cx - 12 * d * s, cy - 25 * s, cx - 11 * d * s, cy - 49 * s, armor_mid, 8.5)
    arcade.draw_ellipse_filled(cx - 11 * d * s, cy - 25 * s, 10 * s, 9 * s, gold_dark)

    # Передняя опорная нога (выдвинута вперёд)
    fk_x, fk_y = cx + 8 * d * s, cy - 23 * s
    ff_x, ff_y = cx + 6 * d * s, cy - 49 * s
    arcade.draw_line(cx + 7 * d * s, cy - 3 * s, fk_x, fk_y, armor_mid, 10)
    arcade.draw_line(fk_x, fk_y, ff_x, ff_y, armor_light, 9)
    arcade.draw_line(fk_x + 2 * d * s, fk_y, ff_x + 2 * d * s, ff_y, gold_bright, 1.8)
    # Рельефный наколенник с золотой каймой
    arcade.draw_ellipse_filled(fk_x + 1 * d * s, fk_y, 12 * s, 11 * s, armor_mid)
    arcade.draw_ellipse_outline(fk_x + 1 * d * s, fk_y, 12 * s, 11 * s, gold_bright, 1.6)
    # Сабатон
    arcade.draw_polygon_filled(
        ((ff_x - 4 * s, cy - 52 * s), (ff_x + 10 * d * s, cy - 52 * s), (ff_x + 7 * d * s, cy - 44 * s), (ff_x - 4 * s, cy - 45 * s)),
        armor_light,
    )

    # Свисающая бело-золотая пола туники между ног
    tabard = (
        (cx - 8 * d * s, cy - 2 * s),
        (cx + 8 * d * s, cy - 2 * s),
        (cx + 5 * d * s + cape_sway * 0.3, cy - 36 * s),
        (cx - 10 * d * s + cape_sway * 0.3, cy - 32 * s),
    )
    arcade.draw_polygon_filled(tabard, cloak_ivory)
    arcade.draw_polygon_outline(tabard, gold, 1.4)

    # 5. Золотая кираса с солярным диском, пояс с крестом и набедренные щитки
    cuirass = (
        (cx - 13 * d * s, cy - 1 * s),
        (cx - 19 * d * s, cy + 27 * s + b),
        (cx + 19 * d * s, cy + 27 * s + b),
        (cx + 13 * d * s, cy - 1 * s),
    )
    arcade.draw_polygon_filled(cuirass, armor_mid)
    arcade.draw_polygon_outline(cuirass, gold, 1.8)

    # Солярный диск с лучами на груди (фирменная деталь с арта)
    sun_x = cx + 1 * d * s
    sun_y = cy + 16 * s + b * 0.85
    for deg in range(0, 360, 30):
        rad = math.radians(deg)
        rx1 = sun_x + math.cos(rad) * 5 * s
        ry1 = sun_y + math.sin(rad) * 5 * s
        rx2 = sun_x + math.cos(rad) * 12 * s
        ry2 = sun_y + math.sin(rad) * 12 * s
        arcade.draw_line(rx1, ry1, rx2, ry2, gold_bright, 1.8)
    arcade.draw_circle_filled(sun_x, sun_y, 6 * s, armor_dark)
    arcade.draw_circle_outline(sun_x, sun_y, 6 * s, gold_bright, 1.8)

    # Золотой пояс с пряжкой-крестом и боковые тассеты
    belt_y = cy - 1 * s + b * 0.4
    arcade.draw_rect_filled(arcade.XYWH(cx, belt_y, 28 * s, 5.5 * s), gold_dark)
    arcade.draw_rect_outline(arcade.XYWH(cx, belt_y, 28 * s, 5.5 * s), gold_bright, 1.4)
    arcade.draw_circle_filled(cx + 1 * d * s, belt_y, 4.5 * s, gold_bright)
    arcade.draw_line(cx + 1 * d * s, belt_y - 3 * s, cx + 1 * d * s, belt_y + 3 * s, armor_dark, 1.6)
    arcade.draw_line(cx - 2 * d * s, belt_y, cx + 4 * d * s, belt_y, armor_dark, 1.6)

    for side in (-1, 1):
        tasset = (
            (cx + side * 7 * d * s, belt_y - 2 * s),
            (cx + side * 17 * d * s, belt_y - 2 * s),
            (cx + side * 19 * d * s, belt_y - 13 * s),
            (cx + side * 9 * d * s, belt_y - 12 * s),
        )
        arcade.draw_polygon_filled(tasset, armor_dark)
        arcade.draw_polygon_outline(tasset, gold, 1.3)

    # 6. Массивные золочёные наплечники с солярным рельефом и воротник
    arcade.draw_ellipse_filled(cx, cy + 28 * s + b, 32 * s, 9 * s, cloak_ivory)
    for side in (-1, 1):
        px = cx + side * 19 * d * s
        py = cy + 25 * s + b
        pauldron = (
            (px - side * 5 * d * s, py + 6 * s),
            (px + side * 12 * d * s, py + 4 * s),
            (px + side * 13 * d * s, py - 8 * s),
            (px - side * 4 * d * s, py - 6 * s),
        )
        arcade.draw_polygon_filled(pauldron, armor_mid)
        arcade.draw_polygon_outline(pauldron, gold_bright, 1.8)
        arcade.draw_arc_outline(px + side * 4 * d * s, py - 1 * s, 12 * s, 9 * s, gold, 0, 180, 1.5)

    # 7. Шлем Крестоносца с высоким центральным гребнем и золотой маской
    helm = (
        (hx - 7.5 * s, hy - 6 * s),
        (hx - 8 * s, hy + 8 * s),
        (hx, hy + 13 * s),
        (hx + 8 * s, hy + 8 * s),
        (hx + 7.5 * s, hy - 6 * s),
        (hx, hy - 10 * s),
    )
    arcade.draw_polygon_filled(helm, armor_light)
    arcade.draw_polygon_outline(helm, gold_bright, 1.6)

    # Золотая лицевая пластина-маска и высокий центральный гребень
    face_mask = (
        (hx - 5.5 * s, hy + 3 * s),
        (hx + 5.5 * s, hy + 3 * s),
        (hx + 5 * s, hy - 5 * s),
        (hx, hy - 8.5 * s),
        (hx - 5 * s, hy - 5 * s),
    )
    arcade.draw_polygon_filled(face_mask, gold)
    crest = ((hx - 1.5 * s, hy + 3 * s), (hx, hy + 18 * s), (hx + 2 * s, hy + 3 * s))
    arcade.draw_polygon_filled(crest, armor_light)
    arcade.draw_polygon_outline(crest, gold_bright, 1.2)
    # Прорези глаз и дыхания
    arcade.draw_line(hx - 5 * s, hy + 2.5 * s, hx - 1 * s, hy + 2 * s, (24, 22, 20), 2)
    arcade.draw_line(hx + 5 * s, hy + 2.5 * s, hx + 1 * s, hy + 2 * s, (24, 22, 20), 2)
    arcade.draw_line(hx, hy + 1 * s, hx, hy - 7 * s, armor_dark, 1.6)

    # 8. Высокий заострённый башенный щит на левой руке (с золотыми рёбрами и солярным орнаментом)
    sx = cx + 24 * d * s
    sy = cy - 6 * s + b * 0.6 + shield_sway

    shield_outer = (
        (sx - 12 * d * s, sy + 28 * s),
        (sx + 10 * d * s, sy + 20 * s),
        (sx + 18 * d * s, sy - 26 * s),
        (sx + 9 * d * s, sy - 38 * s),
        (sx - 6 * d * s, sy - 14 * s),
    )
    arcade.draw_polygon_filled(shield_outer, armor_dark)
    arcade.draw_polygon_outline(shield_outer, gold, 1.8)

    # Внутреннее полотно щита и золотая рельефная решётка
    shield_inner = (
        (sx - 9.5 * d * s, sy + 24 * s),
        (sx + 8 * d * s, sy + 17 * s),
        (sx + 15 * d * s, sy - 24 * s),
        (sx + 8 * d * s, sy - 33 * s),
        (sx - 4 * d * s, sy - 12 * s),
    )
    arcade.draw_polygon_filled(shield_inner, (64, 72, 68))

    # Центральное вертикальное ребро жёсткости и поперечины
    arcade.draw_line(sx - 1 * d * s, sy + 23 * s, sx + 11 * d * s, sy - 33 * s, gold_bright, 2.4)
    for ry_off in (12, 1, -10):
        arcade.draw_line(
            sx - 7 * d * s + (12 - ry_off) * 0.15 * d * s,
            sy + ry_off * s + 3 * s,
            sx + 9 * d * s + (12 - ry_off) * 0.18 * d * s,
            sy + ry_off * s - 2 * s,
            gold,
            1.6,
        )

def _draw_assassin(cx: float, cy: float, s: float, d: float, t: float, b: float):
    """Детализированный спрайт Ассасина по референсу (белый капюшон, алый кушак, пистолеты, 2 сабли)."""
    sash_sway = math.sin(t * 2.5) * 3.0 * s
    coat_sway = math.sin(t * 2.1) * 1.8 * s

    coat_white = (226, 230, 235)
    coat_blue = (128, 156, 178)
    coat_shade = (88, 112, 134)
    leather_brown = (94, 66, 48)
    leather_dark = (52, 36, 28)
    bracer_dark = (44, 48, 54)
    sash_red = (168, 36, 34)
    sash_dark = (112, 22, 22)
    steel_light = (212, 222, 232)
    steel_mid = (132, 144, 158)
    skin_face = (188, 142, 116)

    # 1. Свисающий хвост алого кушака за бедром
    sash_tail = (
        (cx + 10 * d * s, cy - 3 * s),
        (cx + 18 * d * s, cy - 5 * s),
        (cx + 28 * d * s + sash_sway, cy - 32 * s),
        (cx + 21 * d * s + sash_sway, cy - 35 * s),
    )
    arcade.draw_polygon_filled(sash_tail, sash_dark)
    arcade.draw_polygon_outline(sash_tail, (72, 14, 14), 1.2)

    # 2. Ноги в походных штанах и высоких кожаных сапогах с отворотами
    for side, lx, shift_x in ((-1, cx - 9 * d * s, -3), (1, cx + 8 * d * s, 2)):
        kx = lx + shift_x * 0.4 * d * s
        ky = cy - 22 * s
        fx = lx + shift_x * d * s
        fy = cy - 49 * s

        # Штаны
        arcade.draw_line(lx, cy - 6 * s, kx, ky, (118, 108, 96) if side > 0 else (86, 78, 70), 9.5)
        # Высокий сапог и кожаный отворот на колене
        arcade.draw_line(kx, ky, fx, fy, leather_dark, 9)
        arcade.draw_ellipse_filled(kx + 1 * d * s, ky - 2 * s, 11 * s, 9 * s, leather_brown)
        arcade.draw_ellipse_outline(kx + 1 * d * s, ky - 2 * s, 11 * s, 9 * s, leather_dark, 1.3)

        boot_foot = (
            (fx - 4 * s, cy - 52 * s),
            (fx + 9 * d * s, cy - 52 * s),
            (fx + 6 * d * s, cy - 45 * s),
            (fx - 4 * s, cy - 46 * s),
        )
        arcade.draw_polygon_filled(boot_foot, leather_dark)

    # 3. Расходящиеся нижние полы бело-лазурного камзола
    left_skirt = (
        (cx - 14 * d * s, cy - 2 * s),
        (cx - 1 * d * s, cy - 2 * s),
        (cx - 4 * d * s + coat_sway * 0.4, cy - 34 * s),
        (cx - 21 * d * s + coat_sway * 0.6, cy - 38 * s),
    )
    right_skirt = (
        (cx + 1 * d * s, cy - 2 * s),
        (cx + 15 * d * s, cy - 2 * s),
        (cx + 25 * d * s + coat_sway * 0.6, cy - 36 * s),
        (cx + 6 * d * s + coat_sway * 0.4, cy - 32 * s),
    )
    arcade.draw_polygon_filled(left_skirt, coat_white)
    arcade.draw_polygon_outline(left_skirt, coat_shade, 1.4)
    arcade.draw_polygon_filled(right_skirt, coat_blue)
    arcade.draw_polygon_outline(right_skirt, coat_shade, 1.4)
    # Светлый треугольный подбой спереди
    arcade.draw_polygon_filled(
        ((cx - 8 * d * s, cy - 3 * s), (cx + 7 * d * s, cy - 3 * s), (cx + 1 * d * s, cy - 24 * s)),
        coat_white,
    )

    # 4. Приталенный торс, кожаные лацканы, перевязь с пистолетами и красный кушак
    torso = (
        (cx - 14 * d * s, cy + 1 * s),
        (cx - 18 * d * s, cy + 28 * s + b),
        (cx + 18 * d * s, cy + 28 * s + b),
        (cx + 14 * d * s, cy + 1 * s),
    )
    arcade.draw_polygon_filled(torso, coat_white)
    arcade.draw_polygon_outline(torso, coat_shade, 1.5)

    # Тёмно-синий жилет по центру и коричневые лацканы-наплечники
    arcade.draw_polygon_filled(
        ((cx - 7 * d * s, cy + 26 * s + b), (cx + 7 * d * s, cy + 26 * s + b), (cx + 4 * d * s, cy + 4 * s), (cx - 4 * d * s, cy + 4 * s)),
        coat_shade,
    )
    for side in (-1, 1):
        lapel = (
            (cx + side * 8 * d * s, cy + 29 * s + b),
            (cx + side * 20 * d * s, cy + 27 * s + b),
            (cx + side * 18 * d * s, cy + 14 * s + b * 0.8),
            (cx + side * 7 * d * s, cy + 16 * s + b * 0.8),
        )
        arcade.draw_polygon_filled(lapel, leather_brown)
        arcade.draw_polygon_outline(lapel, leather_dark, 1.4)

    # Перекрещённая кожаная портупея и два кремнёвых пистолета на груди
    arcade.draw_line(cx - 12 * d * s, cy + 26 * s + b, cx + 11 * d * s, cy + 4 * s + b * 0.4, leather_dark, 4)
    arcade.draw_line(cx + 12 * d * s, cy + 26 * s + b, cx - 11 * d * s, cy + 4 * s + b * 0.4, leather_dark, 4)
    # Серебряный череп-пряжка на левой перевязи
    arcade.draw_circle_filled(cx - 7 * d * s, cy + 22 * s + b, 3.2 * s, steel_light)

    # Верхний и нижний кремнёвые пистолеты на груди
    for py_off, tilt in ((17, 3), (10, 2)):
        py = cy + py_off * s + b * 0.7
        arcade.draw_line(cx - 8 * d * s, py - tilt * s, cx + 9 * d * s, py + tilt * s, steel_mid, 3.2)
        arcade.draw_line(cx - 10 * d * s, py - (tilt + 2) * s, cx - 3 * d * s, py - (tilt - 1) * s, leather_brown, 4.5)

    # Широкий многослойный алый кушак на поясе
    belt_y = cy + 1 * s + b * 0.4
    arcade.draw_rect_filled(arcade.XYWH(cx, belt_y, 29 * s, 9 * s), sash_red)
    arcade.draw_rect_outline(arcade.XYWH(cx, belt_y, 29 * s, 9 * s), sash_dark, 1.4)
    arcade.draw_line(cx - 14 * d * s, belt_y + 1.5 * s, cx + 14 * d * s, belt_y - 1 * s, sash_dark, 1.6)
    arcade.draw_line(cx - 14 * d * s, belt_y - 2 * s, cx + 14 * d * s, belt_y + 0.5 * s, sash_dark, 1.6)

    # 5. Голова в остроконечном белом капюшоне ассасина
    hx = cx
    hy = cy + 40 * s + b
    hood = (
        (hx - 11 * s, hy - 8 * s),
        (hx - 10 * s, hy + 7 * s),
        (hx, hy + 17 * s),
        (hx + 10 * s, hy + 7 * s),
        (hx + 11 * s, hy - 8 * s),
    )
    arcade.draw_polygon_filled(hood, coat_white)
    arcade.draw_polygon_outline(hood, coat_blue, 1.6)

    # Лицо и глубокая тень от козырька капюшона
    arcade.draw_ellipse_filled(hx, hy - 1 * s, 11 * s, 14 * s, skin_face)
    hood_shadow = (
        (hx - 6.5 * s, hy + 5 * s),
        (hx + 6.5 * s, hy + 5 * s),
        (hx + 5.5 * s, hy - 1 * s),
        (hx, hy + 1 * s),
        (hx - 5.5 * s, hy - 1 * s),
    )
    arcade.draw_polygon_filled(hood_shadow, (22, 20, 22))

    # 6. Обе руки в тёмных наручах и парные изогнутые абордажные сабли
    for side in (-1, 1):
        sh_x = cx + side * 18 * d * s
        sh_y = cy + 21 * s + b
        el_x = cx + side * 24 * d * s
        el_y = cy + 6 * s + b * 0.7
        hd_x = cx + side * 27 * d * s
        hd_y = cy - 8 * s + b * 0.5

        # Светлый рукав и длинный тёмный наруч с пряжками
        arcade.draw_line(sh_x, sh_y, el_x, el_y, coat_white, 7.5)
        arcade.draw_line(el_x, el_y, hd_x, hd_y, bracer_dark, 7)
        arcade.draw_line(el_x + side * 2 * d * s, el_y, hd_x + side * 2 * d * s, hd_y, steel_mid, 1.5)

        # Изогнутая стальная сабля, направленная вниз и в сторону
        mid_x = hd_x + side * 14 * d * s
        mid_y = hd_y - 22 * s
        tip_x = hd_x + side * 24 * d * s
        tip_y = hd_y - 44 * s

        saber_pts = ((hd_x, hd_y), (mid_x, mid_y), (tip_x, tip_y))
        arcade.draw_line_strip(saber_pts, steel_mid, 4.2)
        arcade.draw_line_strip(
            ((hd_x + side * 1.2 * d * s, hd_y), (mid_x + side * 1.2 * d * s, mid_y), (tip_x, tip_y)),
            steel_light,
            1.8,
        )

        # Гарда-эфес и кисть в перчатке
        arcade.draw_arc_outline(hd_x + side * 2 * d * s, hd_y - 3 * s, 10 * s, 11 * s, steel_light, 0, 360, 1.8)
        arcade.draw_circle_filled(hd_x, hd_y, 4.2 * s, leather_dark)
        arcade.draw_circle_outline(hd_x, hd_y, 4.2 * s, steel_mid, 1.2)


def draw_hero_sprite(role: str, cx: float, cy: float, s: float, d: int, b: float, t: float, weapon_angle: float):
    """Рисует детализированную фигурку выбранного героя."""
    if role == "Воин":
        _draw_warrior_knight(cx, cy, s, d, t, b)
        return


    elif role in ("Элементалист"):
        _draw_elementalist(cx, cy, s, d, t, b)
        return

    elif role == "Паладин":
        _draw_paladin(cx, cy, s, d, t, b)
        return

    elif role == "Ассасин":
        _draw_assassin(cx, cy, s, d, t, b)

        return
