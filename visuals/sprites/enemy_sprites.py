import math
import arcade


def _draw_supreme_lich(cx: float, cy: float, s: float, d: float, t: float, breath: float):
    """Детализированный спрайт Верховного Лича по концепт-арту (синяя мантия, костяная корона, зелёный огонь)."""
    sway = math.sin(t * 2.2) * 3.0 * s
    robe_dark = (22, 42, 74)
    robe_mid = (34, 68, 112)
    robe_trim = (145, 210, 205)
    bone = (218, 212, 192)
    bone_shadow = (155, 148, 130)
    gold = (212, 175, 85)
    fel_green = (55, 235, 95)

    # 1. Развевающиеся седые волосы и плащ за спиной
    hair_pts = (
        (cx - 16 * d * s, cy + 48 * s + breath),
        (cx - 34 * d * s + sway, cy + 12 * s),
        (cx - 28 * d * s - sway, cy - 32 * s),
        (cx + 28 * d * s + sway, cy - 30 * s),
        (cx + 32 * d * s - sway, cy + 15 * s),
        (cx + 16 * d * s, cy + 48 * s + breath),
    )
    arcade.draw_polygon_filled(hair_pts, (185, 190, 180, 215))

    # 2. Многослойная мантия с рваным низом
    robe_pts = (
        (cx - 22 * d * s, cy + 26 * s + breath),
        (cx + 22 * d * s, cy + 26 * s + breath),
        (cx + 34 * d * s + sway * 0.7, cy - 52 * s),
        (cx + 18 * d * s, cy - 45 * s),
        (cx + 6 * d * s - sway * 0.5, cy - 56 * s),
        (cx - 10 * d * s, cy - 46 * s),
        (cx - 28 * d * s + sway * 0.7, cy - 54 * s),
    )
    arcade.draw_polygon_filled(robe_pts, robe_dark)
    arcade.draw_polygon_outline(robe_pts, robe_trim, 1.5)

    # Центральная панель мантии с руническим узором
    tabard = (
        (cx - 10 * d * s, cy + 6 * s + breath),
        (cx + 10 * d * s, cy + 6 * s + breath),
        (cx + 14 * d * s + sway * 0.4, cy - 50 * s),
        (cx - 12 * d * s + sway * 0.4, cy - 50 * s),
    )
    arcade.draw_polygon_filled(tabard, robe_mid)
    arcade.draw_polygon_outline(tabard, gold, 1.5)
    for ry in (-8, -20, -32, -42):
        arcade.draw_line(cx - 6 * d * s, cy + ry * s, cx + 6 * d * s, cy + (ry - 4) * s, robe_trim, 1.5)

    # Рёбра и грудной камень
    for ry in (14, 19, 24):
        arcade.draw_line(cx - 11 * d * s, cy + ry * s + breath, cx + 11 * d * s, cy + ry * s + breath, bone_shadow, 2)
    arcade.draw_polygon_filled(
        ((cx, cy + 31 * s + breath), (cx + 4 * s, cy + 27 * s + breath), (cx, cy + 23 * s + breath), (cx - 4 * s, cy + 27 * s + breath)),
        (85, 215, 235),
    )

    # 3. Золотой пояс с пряжкой-черепом и цепью
    arcade.draw_line(cx - 19 * d * s, cy + 4 * s + breath, cx + 19 * d * s, cy + 4 * s + breath, gold, 4)
    arcade.draw_circle_filled(cx, cy + 4 * s + breath, 6.5 * s, bone)
    arcade.draw_circle_filled(cx - 2.2 * s, cy + 5 * s + breath, 1.5 * s, (20, 18, 22))
    arcade.draw_circle_filled(cx + 2.2 * s, cy + 5 * s + breath, 1.5 * s, (20, 18, 22))
    # Цепь на поясе
    for i in range(5):
        lx = cx - (4 + i * 3.5) * d * s
        ly = cy + (2 - i * 4.5) * s + breath
        arcade.draw_circle_outline(lx, ly, 2.5 * s, (165, 175, 180), 1.5)

    # 4. Шипастые костяные наплечники
    for side in (-1, 1):
        px = cx + side * 22 * d * s
        py = cy + 27 * s + breath
        arcade.draw_ellipse_filled(px, py, 20 * s, 13 * s, robe_mid)
        arcade.draw_ellipse_outline(px, py, 20 * s, 13 * s, gold, 1.5)
        # Рогатые шипы вверх и вбок
        spike1 = ((px, py + 4 * s), (px + side * 14 * d * s, py + 22 * s), (px + side * 6 * d * s, py + 2 * s))
        spike2 = ((px + side * 6 * d * s, py), (px + side * 18 * d * s, py + 10 * s), (px + side * 8 * d * s, py - 4 * s))
        arcade.draw_polygon_filled(spike1, bone)
        arcade.draw_polygon_filled(spike2, bone_shadow)

    # 5. Череп, длинная седая борода и высокая костяная корона
    head_y = cy + 42 * s + breath
    # Борода
    beard = ((cx - 6 * d * s, head_y - 4 * s), (cx + 6 * d * s, head_y - 4 * s), (cx + sway * 0.5, head_y - 24 * s))
    arcade.draw_polygon_filled(beard, (225, 228, 220))
    # Череп
    arcade.draw_circle_filled(cx, head_y, 11 * s, bone)
    arcade.draw_rect_filled(arcade.XYWH(cx, head_y - 7 * s, 11 * s, 7 * s), bone_shadow)
    # Светящиеся зелёные глазницы
    arcade.draw_circle_filled(cx - 4 * d * s, head_y + 1 * s, 2.6 * s, fel_green)
    arcade.draw_circle_filled(cx + 4 * d * s, head_y + 1 * s, 2.6 * s, fel_green)
    # Корона с 5 зубцами
    crown_base = head_y + 8 * s
    arcade.draw_rect_filled(arcade.XYWH(cx, crown_base, 22 * s, 5 * s), gold)
    for dx, h_tooth in ((-9, 12), (-4.5, 16), (0, 21), (4.5, 16), (9, 12)):
        tooth = ((cx + (dx - 2) * s, crown_base + 2 * s), (cx + (dx + 2) * s, crown_base + 2 * s), (cx + dx * s, crown_base + h_tooth * s))
        arcade.draw_polygon_filled(tooth, bone)
        arcade.draw_polygon_outline(tooth, gold, 1)

    # 6. Посох с изумрудной сферой (сзади по направлению взгляда)
    staff_x = cx - 32 * d * s
    arcade.draw_line(staff_x, cy - 52 * s, staff_x, cy + 56 * s + breath, (175, 155, 110), 4)
    # Ветвистое навершие посоха
    arcade.draw_arc_outline(staff_x, cy + 58 * s + breath, 18 * s, 24 * s, gold, 160, 380, 2.5)
    orb_pulse = math.sin(t * 5.0) * 1.5 * s
    arcade.draw_circle_filled(staff_x, cy + 60 * s + breath, 8 * s + orb_pulse, (45, 225, 95, 95))
    arcade.draw_circle_filled(staff_x, cy + 60 * s + breath, 5.5 * s, (25, 155, 65))
    arcade.draw_circle_outline(staff_x, cy + 60 * s + breath, 5.5 * s, (175, 255, 185), 1.5)

    # 7. Живое зелёное пламя в форме змеи в передней руке
    flame_x = cx + 31 * d * s
    flame_y = cy + 22 * s + breath + math.sin(t * 4.5) * 3 * s
    arcade.draw_circle_filled(flame_x, flame_y + 6 * s, 16 * s, (55, 245, 95, 75))
    for i in range(4):
        fy = flame_y + i * 6 * s
        fx = flame_x + math.sin(t * 8.0 + i) * 3 * s
        r = (11 - i * 1.8) * s
        arcade.draw_circle_filled(fx, fy, r, (70, 245, 95, 190))
    # Змеиный силуэт и клыки внутри огня
    arcade.draw_circle_filled(flame_x + 2 * d * s, flame_y + 12 * s, 5 * s, (215, 255, 130))
    arcade.draw_line(flame_x + 4 * d * s, flame_y + 11 * s, flame_x + 7 * d * s, flame_y + 7 * s, (255, 255, 220), 2)

def _draw_crystal_dragon(cx: float, cy: float, s: float, d: float, t: float, b: float):
    """Кристально-полигональный Кристальный дракон по двум референсам (5 конструктивных акцентов)."""
    # Изначально смотрит вправо (d = 1), в бою d = -1 отражает влево на героя
    breathe = b if b else math.sin(t * 2.5) * 1.8 * s
    core_pulse = math.sin(t * 5.0) * 2.2 * s
    claw_twitch = math.sin(t * 3.2) * 1.5 * s

    c_ruby_dark = (116, 16, 18)
    c_ruby = (176, 28, 24)
    c_ruby_bright = (224, 52, 36)
    c_facet_line = (248, 128, 96, 150)
    c_claw = (226, 214, 206)
    c_claw_sh = (158, 144, 138)

    # --- 1. ГРАНЁНЫЙ РУБИНОВЫЙ КОРПУС И ЗАОСТРЁННЫЙ ХВОСТ ---
    tail_tip = (cx - 64 * d * s, cy - 30 * s)
    tail_mid_top = (cx - 28 * d * s, cy - 10 * s)
    tail_mid_bot = (cx - 26 * d * s, cy - 22 * s)
    hip_top = (cx - 6 * d * s, cy + 4 * s + breathe * 0.4)
    hip_bot = (cx - 4 * d * s, cy - 20 * s)
    chest_top = (cx + 12 * d * s, cy + 16 * s + breathe * 0.7)
    chest_front = (cx + 24 * d * s, cy + 4 * s + breathe * 0.6)
    chest_bot = (cx + 14 * d * s, cy - 14 * s + breathe * 0.3)

    body_facets = (
        ((tail_tip, tail_mid_top, tail_mid_bot), c_ruby_dark),
        ((tail_mid_top, hip_top, tail_mid_bot), c_ruby),
        ((tail_mid_bot, hip_top, hip_bot), c_ruby_dark),
        ((hip_top, chest_top, hip_bot), c_ruby),
        ((hip_bot, chest_top, chest_bot), c_ruby_dark),
        ((chest_top, chest_front, chest_bot), c_ruby_bright),
    )
    for tri, col in body_facets:
        arcade.draw_polygon_filled(tri, col)
        arcade.draw_polygon_outline(tri, c_facet_line, 1.0)

    # --- 2. ПЫЛАЮЩЕЕ ОГНЕННО-ЗОЛОТОЕ ЯДРО В ГРУДИ ---
    core_x = cx + 14 * d * s
    core_y = cy + 3 * s + breathe * 0.6
    arcade.draw_circle_filled(core_x, core_y, 16 * s + core_pulse, (255, 110, 30, 65))
    arcade.draw_circle_filled(core_x, core_y, 10 * s + core_pulse * 0.6, (255, 175, 55, 165))
    arcade.draw_circle_filled(core_x, core_y, 5.2 * s, (255, 248, 210, 240))

    # --- 3. ИЗОГНУТАЯ ШЕЯ И КРИСТАЛЬНЫЕ ШИПЫ ВДОЛЬ СПИНЫ И ШЕИ ---
    neck_mid_b = (cx + 7 * d * s, cy + 34 * s + breathe * 0.85)
    neck_mid_f = (cx + 21 * d * s, cy + 30 * s + breathe * 0.85)
    neck_top_b = (cx + 14 * d * s, cy + 48 * s + breathe)
    neck_top_f = (cx + 25 * d * s, cy + 43 * s + breathe)

    neck_facets = (
        ((chest_top, neck_mid_b, chest_front), c_ruby),
        ((chest_front, neck_mid_b, neck_mid_f), c_ruby_bright),
        ((neck_mid_b, neck_top_b, neck_mid_f), c_ruby_dark),
        ((neck_mid_f, neck_top_b, neck_top_f), c_ruby_bright),
    )
    for tri, col in neck_facets:
        arcade.draw_polygon_filled(tri, col)
        arcade.draw_polygon_outline(tri, c_facet_line, 1.0)

    # Ряд острых кристальных шипов вдоль спины и шеи
    spine_spikes = (
        (-34, -12, -39, -3),
        (-24, -7, -29, 3),
        (-14, -1, -18, 10),
        (-4, 5, -6, 17),
        (5, 11, 4, 23),
        (10, 23, 2, 31),
        (8, 35, -1, 42),
        (12, 44, 3, 52),
    )
    for bx_o, by_o, tx_o, ty_o in spine_spikes:
        bx_s = cx + bx_o * d * s
        by_s = cy + by_o * s + (breathe * 0.5 if by_o > 0 else 0)
        tx_s = cx + tx_o * d * s
        ty_s = cy + ty_o * s + (breathe * 0.5 if by_o > 0 else 0)
        arcade.draw_triangle_filled(bx_s - 2.5 * d * s, by_s - 2 * s, bx_s + 2.5 * d * s, by_s + 2 * s, tx_s, ty_s, c_ruby_bright)
        arcade.draw_line(bx_s, by_s, tx_s, ty_s, c_facet_line, 1.0)

    # --- 4. ДВУНОГИЕ ХИЩНЫЕ ЛАПЫ И ПЕРЕДНИЕ КОГТИСТЫЕ ЛАПЫ ---
    # Задние двуногие лапы с обратным сгибом (дальняя и ближняя)
    for off_x, off_y, col_l in ((8, 3, c_ruby_dark), (-4, 0, c_ruby_bright)):
        hx, hy = cx + off_x * d * s, cy - 10 * s + off_y * s
        kx, ky = hx + 9 * d * s, hy - 14 * s
        ax, ay = hx - 2 * d * s, hy - 26 * s
        fx, fy = hx + 7 * d * s, cy - 48 * s + off_y * s
        arcade.draw_line(hx, hy, kx, ky, col_l, 8.5 * s)
        arcade.draw_line(kx, ky, ax, ay, col_l, 5.5 * s)
        arcade.draw_line(ax, ay, fx, fy, col_l, 4.5 * s)
        for c_i in range(2):
            cx_c = fx + c_i * 3.5 * d * s
            arcade.draw_triangle_filled(cx_c, fy + 1.5 * s, cx_c, fy - 1.5 * s, cx_c + 7 * d * s, fy - 4 * s, c_claw if off_x < 0 else c_claw_sh)

    # Две вытянутые вперёд передние лапы с крупными изогнутыми когтями
    for off_x, off_y, col_a in ((20, 4, c_ruby_dark), (13, 0, c_ruby_bright)):
        sx, sy = cx + off_x * d * s, cy + 4 * s + off_y * s + breathe * 0.5
        ex, ey = sx + 7 * d * s, sy - 10 * s
        wx, wy = sx + 17 * d * s, sy - 3 * s + claw_twitch
        arcade.draw_line(sx, sy, ex, ey, col_a, 5.5 * s)
        arcade.draw_line(ex, ey, wx, wy, col_a, 4.5 * s)
        for f_ang in (-25, 10, 42):
            rad = math.radians(f_ang)
            tx_c = wx + math.cos(rad) * 9 * d * s
            ty_c = wy + math.sin(rad) * 9 * s
            arcade.draw_line(wx, wy, tx_c, ty_c, c_claw if off_x < 18 else c_claw_sh, 2.0 * s)

    # --- 5. КРИСТАЛЬНАЯ ГОЛОВА, ПУЧОК ДЛИННЫХ РОГОВ И ОСКАЛЕННАЯ ПАСТЬ ---
    hx = cx + 22 * d * s
    hy = cy + 48 * s + breathe

    # Пучок длинных кристальных рогов, устремлённых назад и вверх
    horns = (
        ((hx - 2 * d * s, hy + 5 * s), (hx + 3 * d * s, hy + 4 * s), (hx - 14 * d * s, hy + 28 * s), c_ruby_bright),
        ((hx - 4 * d * s, hy + 3 * s), (hx + 1 * d * s, hy + 1 * s), (hx - 21 * d * s, hy + 22 * s), c_ruby),
        ((hx - 5 * d * s, hy), (hx - 1 * d * s, hy - 3 * s), (hx - 22 * d * s, hy + 12 * s), c_ruby_dark),
        ((hx - 4 * d * s, hy - 2 * s), (hx, hy - 5 * s), (hx - 18 * d * s, hy + 3 * s), c_ruby_bright),
    )
    for p1, p2, p3, h_col in horns:
        arcade.draw_polygon_filled((p1, p2, p3), h_col)
        arcade.draw_line(p1[0], p1[1], p3[0], p3[1], c_facet_line, 1.0)

    # Вытянутая гранёная верхняя челюсть
    skull_b = (hx - 5 * d * s, hy + 5 * s)
    skull_t = (hx + 8 * d * s, hy + 7 * s)
    snout_t = (hx + 24 * d * s, hy + 5 * s)
    snout_b = (hx + 23 * d * s, hy + 1 * s)
    jaw_hinge = (hx + 4 * d * s, hy - 2 * s)

    head_facets = (
        ((skull_b, skull_t, jaw_hinge), c_ruby),
        ((skull_t, snout_t, jaw_hinge), c_ruby_bright),
        ((snout_t, snout_b, jaw_hinge), c_ruby_dark),
    )
    for tri, col in head_facets:
        arcade.draw_polygon_filled(tri, col)
        arcade.draw_polygon_outline(tri, c_facet_line, 1.0)

    # Широко раскрытая нижняя челюсть с острым кристальным шипом на подбородке
    chin_f = (hx + 20 * d * s, hy - 12 * s)
    chin_b = (hx + 12 * d * s, hy - 13 * s)
    chin_spike = (hx + 9 * d * s, hy - 16 * s)
    arcade.draw_polygon_filled((jaw_hinge, chin_f, chin_b), c_ruby_dark)
    arcade.draw_polygon_filled((chin_b, chin_f, chin_spike), c_ruby_bright)
    arcade.draw_polygon_outline((jaw_hinge, chin_f, chin_b), c_facet_line, 1.0)

    # Ряды острых белых клыков в пасти
    for k_i in range(4):
        frac = (k_i + 1) / 5.0
        ux = jaw_hinge[0] + (snout_b[0] - jaw_hinge[0]) * frac
        uy = jaw_hinge[1] + (snout_b[1] - jaw_hinge[1]) * frac
        arcade.draw_line(ux, uy, ux + 0.5 * d * s, uy - 2.6 * s, c_claw, 1.2)
        lx = jaw_hinge[0] + (chin_f[0] - jaw_hinge[0]) * frac
        ly = jaw_hinge[1] + (chin_f[1] - jaw_hinge[1]) * frac
        arcade.draw_line(lx, ly, lx + 0.5 * d * s, ly + 2.6 * s, c_claw, 1.2)

    # Яркий светящийся золотой глаз
    eye_p1 = (hx + 5 * d * s, hy + 2.5 * s)
    eye_p2 = (hx + 11 * d * s, hy + 2.2 * s)
    eye_p3 = (hx + 8 * d * s, hy + 0.6 * s)
    arcade.draw_polygon_filled((eye_p1, eye_p2, eye_p3), (255, 224, 52))


def _draw_black_skeleton_mage(cx: float, cy: float, s: float, d: float, t: float, b: float):
    """Детализированный спрайт Элитного Чёрного Скелета-Мага в тёмном капюшоне с костяным посохом."""
    sway = math.sin(t * 2.0) * 2.5 * s
    cloak_dark = (18, 22, 32)
    cloak_mid = (28, 35, 50)
    cloak_edge = (58, 70, 94)
    bone = (212, 202, 182)
    bone_shadow = (148, 138, 120)

    # 1. Задний развевающийся плащ с рваным подолом
    back_cloak = (
        (cx - 18 * d * s, cy + 36 * s + b),
        (cx + 18 * d * s, cy + 36 * s + b),
        (cx + 32 * d * s + sway, cy - 52 * s),
        (cx + 16 * d * s, cy - 45 * s),
        (cx + 4 * d * s - sway * 0.5, cy - 54 * s),
        (cx - 12 * d * s, cy - 46 * s),
        (cx - 28 * d * s + sway, cy - 53 * s),
    )
    arcade.draw_polygon_filled(back_cloak, cloak_dark)
    arcade.draw_polygon_outline(back_cloak, cloak_edge, 1.5)

    # 2. Кости ног (бёдра, колени, голени и ступни)
    for side, leg_x in ((-1, cx - 7 * d * s), (1, cx + 8 * d * s)):
        knee_x = leg_x + side * 2 * d * s
        knee_y = cy - 22 * s
        foot_x = leg_x + side * 3 * d * s
        foot_y = cy - 50 * s

        # Бедренная и берцовая кости
        arcade.draw_line(leg_x, cy - 2 * s, knee_x, knee_y, bone, 4)
        arcade.draw_line(knee_x, knee_y, foot_x, foot_y, bone, 3.5)
        # Коленный сустав
        arcade.draw_circle_filled(knee_x, knee_y, 3.2 * s, bone_shadow)
        # Ступня с пальцами
        arcade.draw_line(foot_x, foot_y, foot_x + 7 * d * s, foot_y - 2 * s, bone, 3)

    # 3. Тазовая кость и рваная тёмная повязка на бёдрах
    arcade.draw_ellipse_filled(cx, cy - 1 * s + b * 0.5, 22 * s, 9 * s, bone_shadow)
    loincloth = (
        (cx - 14 * d * s, cy + 2 * s + b * 0.5),
        (cx + 14 * d * s, cy + 2 * s + b * 0.5),
        (cx + 17 * d * s + sway * 0.4, cy - 20 * s),
        (cx + 6 * d * s, cy - 13 * s),
        (cx - 4 * d * s, cy - 22 * s),
        (cx - 15 * d * s + sway * 0.4, cy - 15 * s),
    )
    arcade.draw_polygon_filled(loincloth, cloak_mid)
    arcade.draw_polygon_outline(loincloth, cloak_edge, 1.2)

    # 4. Позвоночник и открытая грудная клетка с рёбрами
    arcade.draw_line(cx, cy + 2 * s, cx, cy + 38 * s + b, bone_shadow, 4)
    for idx, ry in enumerate((10, 15, 20, 25, 30)):
        rib_w = (10 + idx * 1.1) * s
        arcade.draw_arc_outline(cx, cy + ry * s + b, rib_w * 2, 7 * s, bone, 190, 350, 2.2)

    # 5. Тёмный балахон-накидка по бокам торса и драпировка на шее
    for side in (-1, 1):
        flap = (
            (cx + side * 12 * d * s, cy + 34 * s + b),
            (cx + side * 23 * d * s, cy + 28 * s + b),
            (cx + side * 27 * d * s + sway * 0.5, cy - 26 * s),
            (cx + side * 13 * d * s, cy - 18 * s),
        )
        arcade.draw_polygon_filled(flap, cloak_mid)
        arcade.draw_polygon_outline(flap, cloak_edge, 1.2)

    # Шарф-воротник
    arcade.draw_ellipse_filled(cx, cy + 34 * s + b, 34 * s, 10 * s, cloak_mid)
    arcade.draw_ellipse_outline(cx, cy + 34 * s + b, 34 * s, 10 * s, cloak_edge, 1.5)

    # 6. Глубокий капюшон и череп внутри него
    head_y = cy + 45 * s + b
    hood = (
        (cx - 15 * d * s, head_y - 10 * s),
        (cx - 13 * d * s, head_y + 12 * s),
        (cx, head_y + 18 * s),
        (cx + 13 * d * s, head_y + 12 * s),
        (cx + 15 * d * s, head_y - 10 * s),
    )
    arcade.draw_polygon_filled(hood, cloak_dark)
    arcade.draw_polygon_outline(hood, cloak_edge, 1.5)

    # Череп, скулы, челюсть и тёмные глазницы
    arcade.draw_circle_filled(cx + 1 * d * s, head_y + 2 * s, 9 * s, bone)
    arcade.draw_rect_filled(arcade.XYWH(cx + 1.5 * d * s, head_y - 5 * s, 9 * s, 6 * s), bone_shadow)
    arcade.draw_circle_filled(cx - 2 * d * s, head_y + 2 * s, 2.3 * s, (14, 12, 16))
    arcade.draw_circle_filled(cx + 4.5 * d * s, head_y + 2 * s, 2.3 * s, (14, 12, 16))
    # Зубы
    for zx in (-2, 0.5, 3):
        arcade.draw_line(cx + zx * d * s, head_y - 4 * s, cx + zx * d * s, head_y - 7 * s, (25, 22, 26), 1)

    # 7. Костистые руки (передняя опущена с пальцами, задняя держит посох)
    # Свободная рука
    arm_x = cx + 21 * d * s
    elbow_y = cy + 12 * s + b
    hand_y = cy - 8 * s + b
    arcade.draw_line(cx + 16 * d * s, cy + 28 * s + b, arm_x, elbow_y, bone_shadow, 3.5)
    arcade.draw_line(arm_x, elbow_y, arm_x + 4 * d * s, hand_y, bone, 3)
    for finger in (-2, 0, 2):
        arcade.draw_line(arm_x + 4 * d * s, hand_y, arm_x + (5 + finger) * d * s, hand_y - 6 * s, bone, 1.5)

    # 8. Узловатый костяной посох с раздвоенным рогатым навершием (как на арте)
    staff_x = cx - 26 * d * s
    arcade.draw_line(staff_x + 2 * d * s, cy - 52 * s, staff_x - 2 * d * s, cy + 24 * s + b, bone_shadow, 5)
    # Узел посоха в руке
    arcade.draw_circle_filled(staff_x - 2 * d * s, cy + 16 * s + b, 4.5 * s, bone)
    # Левая и правая ветви рогатого навершия
    left_branch = (
        (staff_x - 2 * d * s, cy + 22 * s + b),
        (staff_x - 7 * d * s, cy + 42 * s + b),
        (staff_x - 5 * d * s, cy + 54 * s + b),
        (staff_x - 1 * d * s, cy + 40 * s + b),
    )
    right_branch = (
        (staff_x - 1 * d * s, cy + 24 * s + b),
        (staff_x + 4 * d * s, cy + 46 * s + b),
        (staff_x + 2 * d * s, cy + 58 * s + b),
        (staff_x - 2 * d * s, cy + 42 * s + b),
    )
    arcade.draw_polygon_filled(left_branch, bone)
    arcade.draw_polygon_outline(left_branch, bone_shadow, 1.2)
    arcade.draw_polygon_filled(right_branch, bone)
    arcade.draw_polygon_outline(right_branch, bone_shadow, 1.2)

def _draw_goblin(cx: float, cy: float, s: float, d: float, t: float, b: float):
    """Детализированный спрайт Лесного Гоблина по референсу (красные подтяжки, широкий кинжал, острые уши)."""
    skin = (128, 178, 56)
    skin_light = (158, 206, 78)
    skin_dark = (82, 124, 34)
    brow_col = (68, 108, 26)
    pants = (68, 52, 42)
    pants_dark = (46, 35, 28)
    strap_red = (182, 54, 44)
    bronze = (165, 132, 68)
    blade_light = (212, 218, 224)
    blade_dark = (135, 142, 150)

    # 1. Полусогнутые ноги и остроносые кожаные башмаки
    for side, lx, shoe_col in ((-1, cx - 12 * d * s, (52, 48, 48)), (1, cx + 11 * d * s, (112, 82, 58))):
        knee_x = lx + 3 * d * s
        knee_y = cy - 26 * s
        ankle_x = lx - 1 * d * s
        ankle_y = cy - 42 * s

        # Голень и штанина бриджей
        arcade.draw_line(ankle_x, ankle_y, ankle_x, cy - 49 * s, skin_dark, 5)
        arcade.draw_line(lx, cy - 14 * s, knee_x, knee_y, pants, 11)
        arcade.draw_line(knee_x, knee_y, ankle_x, ankle_y, pants_dark, 10)

        # Остроносый башмак с загнутым вверх носком
        shoe = (
            (ankle_x - 5 * d * s, cy - 52 * s),
            (ankle_x + 12 * d * s, cy - 52 * s),
            (ankle_x + 19 * d * s, cy - 45 * s),
            (ankle_x + 10 * d * s, cy - 46 * s),
            (ankle_x - 4 * d * s, cy - 46 * s),
        )
        arcade.draw_polygon_filled(shoe, shoe_col)
        arcade.draw_polygon_outline(shoe, (28, 24, 24), 1.2)

    # 2. Пузатый торс, бриджи и красные подтяжки
    arcade.draw_ellipse_filled(cx, cy - 12 * s, 34 * s, 20 * s, pants)
    arcade.draw_ellipse_filled(cx + 2 * d * s, cy + 4 * s + b, 30 * s, 32 * s, skin)
    arcade.draw_ellipse_outline(cx + 2 * d * s, cy + 4 * s + b, 30 * s, 32 * s, skin_dark, 1.5)

    # Красные подтяжки и золотые пряжки
    for sx in (-8, 7):
        top_x = cx + (sx - 2) * d * s
        bot_x = cx + sx * d * s
        arcade.draw_line(top_x, cy + 18 * s + b, bot_x, cy - 6 * s, strap_red, 4.5)
        arcade.draw_rect_filled(arcade.XYWH(bot_x, cy - 6 * s, 6 * s, 5 * s), bronze)

    # 3. Задняя рука (держится за лямку подтяжки у плеча)
    arm_bx = cx - 15 * d * s
    arcade.draw_line(cx - 10 * d * s, cy + 15 * s + b, arm_bx - 4 * d * s, cy + 4 * s + b, skin_dark, 6)
    arcade.draw_line(arm_bx - 4 * d * s, cy + 4 * s + b, arm_bx + 3 * d * s, cy + 14 * s + b, skin, 5.5)
    arcade.draw_circle_filled(arm_bx + 4 * d * s, cy + 15 * s + b, 4.5 * s, skin_light)

    # 4. Большая голова с длинными острыми ушами и хитрой ухмылкой
    head_y = cy + 32 * s + b
    ear_wig = math.sin(t * 3.5) * 1.8 * s

    # Левое и правое заострённые уши
    ear_back = (
        (cx - 14 * d * s, head_y + 4 * s),
        (cx - 34 * d * s, head_y + 11 * s + ear_wig),
        (cx - 26 * d * s, head_y - 2 * s),
        (cx - 14 * d * s, head_y - 5 * s),
    )
    ear_front = (
        (cx + 14 * d * s, head_y + 4 * s),
        (cx + 35 * d * s, head_y + 13 * s - ear_wig),
        (cx + 25 * d * s, head_y - 3 * s),
        (cx + 14 * d * s, head_y - 6 * s),
    )
    arcade.draw_polygon_filled(ear_back, skin_dark)
    arcade.draw_polygon_outline(ear_back, brow_col, 1.2)
    arcade.draw_polygon_filled(ear_front, skin_light)
    arcade.draw_polygon_outline(ear_front, skin_dark, 1.2)

    # Череп и подбородок
    arcade.draw_rect_filled(arcade.XYWH(cx, head_y + 2 * s, 28 * s, 26 * s), skin)
    arcade.draw_ellipse_filled(cx, head_y + 12 * s, 26 * s, 12 * s, skin_light)
    arcade.draw_ellipse_filled(cx + 1 * d * s, head_y - 10 * s, 22 * s, 11 * s, skin)
    arcade.draw_rect_outline(arcade.XYWH(cx, head_y + 2 * s, 28 * s, 26 * s), skin_dark, 1.5)

    # Глаза и густые нахмуренные брови
    for ex in (-6, 7):
        eye_x = cx + ex * d * s
        arcade.draw_ellipse_filled(eye_x, head_y + 4 * s, 7 * s, 5 * s, (245, 242, 215))
        arcade.draw_circle_filled(eye_x + 1 * d * s, head_y + 4 * s, 2.0 * s, (35, 42, 24))
        arcade.draw_line(eye_x - 4 * d * s, head_y + 8 * s, eye_x + 4 * d * s, head_y + 7 * s, brow_col, 3)

    # Крупный нос картошкой
    arcade.draw_ellipse_filled(cx + 2 * d * s, head_y - 1 * s, 8 * s, 9 * s, (168, 198, 92))
    arcade.draw_ellipse_outline(cx + 2 * d * s, head_y - 1 * s, 8 * s, 9 * s, skin_dark, 1)

    # Широкая ухмылка с зубами
    arcade.draw_arc_filled(cx + 1 * d * s, head_y - 6 * s, 15 * s, 7 * s, (32, 26, 24), 185, 355)
    arcade.draw_line(cx - 5 * d * s, head_y - 7 * s, cx + 7 * d * s, head_y - 7 * s, (238, 235, 215), 2)

    # 5. Передняя рука с массивным стальным кинжалом наперевес
    sh_x = cx + 14 * d * s
    el_x = cx + 24 * d * s
    el_y = cy + 2 * s + b
    hand_x = cx + 12 * d * s
    hand_y = cy - 8 * s + b

    arcade.draw_line(sh_x, cy + 14 * s + b, el_x, el_y, skin_light, 6.5)
    arcade.draw_line(el_x, el_y, hand_x, hand_y, skin, 6)

    # Рукоять, бронзовая гарда и широкое двуцветное лезвие кинжала
    gx = hand_x - 3 * d * s
    gy = hand_y + 3 * s
    arcade.draw_line(hand_x + 5 * d * s, hand_y - 5 * s, gx, gy, bronze, 5)
    arcade.draw_line(gx - 6 * d * s, gy - 7 * s, gx + 6 * d * s, gy + 7 * s, bronze, 4.5)

    tip_x = gx - 24 * d * s
    tip_y = gy + 22 * s
    blade_top = ((gx - 3 * d * s, gy + 4 * s), (gx + 3 * d * s, gy - 3 * s), (tip_x, tip_y))
    blade_bot = ((gx + 3 * d * s, gy - 3 * s), (gx - 4 * d * s, gy - 6 * s), (tip_x, tip_y))
    arcade.draw_polygon_filled(blade_top, blade_light)
    arcade.draw_polygon_filled(blade_bot, blade_dark)
    blade_outline = (
        (gx - 3 * d * s, gy + 4 * s),
        (tip_x, tip_y),
        (gx - 4 * d * s, gy - 6 * s),
        (gx + 3 * d * s, gy - 3 * s),
    )
    arcade.draw_polygon_outline(blade_outline, (70, 75, 82), 1.2)

    # Кулак поверх рукояти
    arcade.draw_circle_filled(hand_x, hand_y, 5 * s, skin_light)
    arcade.draw_circle_outline(hand_x, hand_y, 5 * s, skin_dark, 1.2)

def _draw_skeleton_swordsman(cx: float, cy: float, s: float, d: float, t: float, b: float):
    """Детализированный спрайт Костяного Воина (Скелета-мечника) по референсу."""
    bone = (198, 186, 162)
    bone_light = (224, 214, 192)
    bone_shadow = (135, 124, 104)
    steel = (145, 152, 160)
    steel_dark = (78, 82, 90)
    steel_light = (205, 212, 220)
    bronze = (158, 128, 72)

    # 1. Тяжёлый длинный меч в задней руке (опущен остриём к земле позади бойца)
    hand_bx = cx - 20 * d * s
    hand_by = cy - 4 * s + b * 0.5
    tip_x = cx - 54 * d * s
    tip_y = cy - 52 * s

    # Клинок (двухцветная грань с зазубринами)
    blade_top = (
        (hand_bx - 2 * d * s, hand_by + 3 * s),
        (hand_bx + 3 * d * s, hand_by - 2 * s),
        (tip_x + 3 * d * s, tip_y - 2 * s),
        (tip_x, tip_y),
    )
    blade_bot = (
        (hand_bx + 3 * d * s, hand_by - 2 * s),
        (hand_bx + 6 * d * s, hand_by - 6 * s),
        (tip_x + 5 * d * s, tip_y - 4 * s),
        (tip_x + 3 * d * s, tip_y - 2 * s),
    )
    arcade.draw_polygon_filled(blade_top, steel)
    arcade.draw_polygon_filled(blade_bot, steel_dark)
    arcade.draw_line(hand_bx, hand_by, tip_x, tip_y, (48, 50, 56), 1.5)

    # Гарда и рукоять меча
    arcade.draw_line(hand_bx - 7 * d * s, hand_by - 6 * s, hand_bx + 7 * d * s, hand_by + 6 * s, bronze, 4)
    arcade.draw_line(hand_bx, hand_by, hand_bx + 9 * d * s, hand_by + 11 * s, (92, 68, 44), 3.5)

    # 2. Задняя рука, держащая меч
    sh_bx = cx - 15 * d * s
    sh_by = cy + 32 * s + b
    el_bx = cx - 19 * d * s
    el_by = cy + 14 * s + b * 0.7
    arcade.draw_line(sh_bx, sh_by, el_bx, el_by, bone_shadow, 3.5)
    arcade.draw_line(el_bx, el_by, hand_bx, hand_by, bone, 3.5)
    arcade.draw_circle_filled(hand_bx, hand_by, 3.5 * s, bone_light)

    # 3. Широко расставленные костистые ноги с коленными суставами
    # Задняя опорная нога
    hip_bx, hip_by = cx - 8 * d * s, cy - 4 * s
    knee_bx, knee_by = cx - 14 * d * s, cy - 26 * s
    foot_bx, foot_by = cx - 22 * d * s, cy - 50 * s
    arcade.draw_line(hip_bx, hip_by, knee_bx, knee_by, bone_shadow, 4.5)
    arcade.draw_line(knee_bx, knee_by, foot_bx, foot_by, bone, 4)
    arcade.draw_circle_filled(knee_bx, knee_by, 4 * s, bone_light)
    arcade.draw_line(foot_bx - 2 * d * s, foot_by, foot_bx + 8 * d * s, foot_by - 2 * s, bone, 3)

    # Передняя выдвинутая нога
    hip_fx, hip_fy = cx + 9 * d * s, cy - 4 * s
    knee_fx, knee_fy = cx + 22 * d * s, cy - 24 * s
    foot_fx, foot_fy = cx + 17 * d * s, cy - 50 * s
    arcade.draw_line(hip_fx, hip_fy, knee_fx, knee_fy, bone, 4.5)
    arcade.draw_line(knee_fx, knee_fy, foot_fx, foot_fy, bone_shadow, 4)
    arcade.draw_circle_filled(knee_fx, knee_fy, 4 * s, bone_light)
    arcade.draw_line(foot_fx - 2 * d * s, foot_fy, foot_fx + 10 * d * s, foot_fy - 2 * s, bone, 3)

    # 4. Тазовая кость и позвоночник
    pelvis = (
        (cx - 13 * d * s, cy + 1 * s),
        (cx + 13 * d * s, cy + 1 * s),
        (cx + 9 * d * s, cy - 8 * s),
        (cx - 9 * d * s, cy - 8 * s),
    )
    arcade.draw_polygon_filled(pelvis, bone_shadow)
    arcade.draw_polygon_outline(pelvis, bone, 1.5)
    arcade.draw_circle_filled(cx - 5 * d * s, cy - 3 * s, 2.5 * s, (24, 22, 26))
    arcade.draw_circle_filled(cx + 5 * d * s, cy - 3 * s, 2.5 * s, (24, 22, 26))

    # Позвоночный столб
    arcade.draw_line(cx, cy, cx + 1 * d * s, cy + 40 * s + b, bone_shadow, 4.5)

    # 5. Объёмная грудная клетка с рёбрами, грудиной и ключицами
    for idx, ry in enumerate((11, 16, 21, 26, 31)):
        rw = (11 + idx * 1.3) * s
        arcade.draw_arc_outline(cx + 2 * d * s, cy + ry * s + b, rw * 2.1, 8 * s, bone_light, 185, 355, 2.4)
    arcade.draw_line(cx + 4 * d * s, cy + 16 * s + b, cx + 3 * d * s, cy + 33 * s + b, bone, 3)
    # Ключицы
    arcade.draw_line(cx - 16 * d * s, cy + 33 * s + b, cx + 17 * d * s, cy + 33 * s + b, bone_light, 3)

    # Лохмотья истлевшей ткани на плече и бедре
    arcade.draw_line(cx - 16 * d * s, cy + 32 * s + b, cx - 18 * d * s, cy + 18 * s, (72, 68, 60, 180), 1.5)
    arcade.draw_line(cx + 11 * d * s, cy - 6 * s, cx + 13 * d * s, cy - 18 * s, (72, 68, 60, 180), 1.5)

    # 6. Анатомичный череп с тёмными глазницами и раскрытой челюстью
    hx = cx + 4 * d * s
    hy = cy + 46 * s + b
    # Нижняя челюсть
    arcade.draw_rect_filled(arcade.XYWH(hx + 2 * d * s, hy - 8 * s, 9 * s, 6 * s), bone_shadow)
    # Черепная коробка и скулы
    arcade.draw_circle_filled(hx, hy + 2 * s, 9.5 * s, bone_light)
    arcade.draw_circle_outline(hx, hy + 2 * s, 9.5 * s, bone_shadow, 1.3)
    # Глазницы и носовая полость
    arcade.draw_circle_filled(hx + 1 * d * s, hy + 2 * s, 2.4 * s, (18, 16, 20))
    arcade.draw_circle_filled(hx + 6.5 * d * s, hy + 2 * s, 2.1 * s, (18, 16, 20))
    arcade.draw_polygon_filled(((hx + 4 * d * s, hy), (hx + 3 * d * s, hy - 3 * s), (hx + 5 * d * s, hy - 3 * s)), (18, 16, 20))
    # Ряд зубов
    for zx in (0, 2.5, 5):
        arcade.draw_line(hx + zx * d * s, hy - 5 * s, hx + zx * d * s, hy - 8 * s, (25, 22, 24), 1)

    # 7. Выпуклый круглый металлический щит в перспективном ракурсе (на передней руке)
    shield_x = cx + 25 * d * s
    shield_y = cy + 8 * s + b * 0.8 + math.sin(t * 2.5) * 1.5 * s
    # Костистые пальцы, выглядывающие из-под нижнего края щита
    for f_off in (-3, 0, 3):
        arcade.draw_line(shield_x - 4 * d * s, shield_y - 20 * s, shield_x + f_off * d * s, shield_y - 26 * s, bone_shadow, 1.8)

    # Основа щита (овал в ракурсе 3/4)
    arcade.draw_ellipse_filled(shield_x, shield_y, 24 * s, 54 * s, steel_dark)
    arcade.draw_ellipse_filled(shield_x + 2 * d * s, shield_y, 19 * s, 46 * s, steel)
    arcade.draw_ellipse_filled(shield_x + 4 * d * s, shield_y, 11 * s, 28 * s, steel_light)
    arcade.draw_ellipse_outline(shield_x, shield_y, 24 * s, 54 * s, bronze, 2.5)

    # Заклёпки по ободу щита
    for deg in range(-75, 85, 25):
        rad = math.radians(deg)
        rx = shield_x + math.cos(rad) * 10 * d * s
        ry = shield_y + math.sin(rad) * 24 * s
        arcade.draw_circle_filled(rx, ry, 1.4 * s, bronze)

def _draw_slime(cx: float, cy: float, s: float, d: float, t: float, b: float):
    """Детализированный спрайт Болотного Слизняка по референсу (один глаз, фиолетовые шипы, зубастая пасть)."""
    # Живое желейное колыхание: при сжатии по вертикали слегка расширяется по горизонтали
    squish = math.sin(t * 3.4) * 0.06
    rx = 46 * s * (1.0 + squish)
    ry = 44 * s * (1.0 - squish)
    base_y = cy - 48 * s

    slime_main = (142, 168, 36)
    slime_dark = (104, 126, 24)
    slime_outline = (78, 96, 18)
    slime_glow = (115, 215, 75, 55)
    spike_violet = (145, 78, 178)
    spike_dark = (96, 48, 122)

    # 1. Мягкое кислотное свечение и растекающаяся лужа слизи у основания
    arcade.draw_ellipse_filled(cx, base_y + ry * 0.85, rx * 2.25, ry * 2.05, slime_glow)
    arcade.draw_ellipse_filled(cx, base_y + 2 * s, rx * 2.25, 14 * s, slime_dark)
    arcade.draw_ellipse_outline(cx, base_y + 2 * s, rx * 2.25, 14 * s, slime_outline, 1.5)

    # 2. Фиолетовые шипы по верхнему контуру купола (рисуем до тела, чтобы основания уходили в слизь)
    spike_angles = (152, 126, 98, 70, 42)
    for deg in spike_angles:
        rad = math.radians(deg)
        # Поворачиваем углы с учётом направления взгляда d (1 или -1)
        nx = -math.cos(rad) * d
        ny = math.sin(rad)

        bx = cx + nx * (rx * 0.92)
        by = base_y + ny * (ry * 1.68)
        tip_x = cx + nx * (rx * 1.24)
        tip_y = base_y + ny * (ry * 2.05)

        # Перпендикуляр к нормали для ширины основания шипа
        px, py = -ny * 7.5 * s, nx * 7.5 * s
        spike_poly = ((bx - px, by - py), (bx + px, by + py), (tip_x, tip_y))
        arcade.draw_polygon_filled(spike_poly, spike_violet)
        arcade.draw_polygon_outline(spike_poly, spike_dark, 1.5)

    # 3. Основной купол тела слизняка
    dome_pts = [(cx - rx, base_y + 2 * s)]
    steps = 24
    for i in range(steps + 1):
        ang = math.pi * (1.0 - i / steps)
        px = cx + math.cos(ang) * rx
        py = base_y + 2 * s + math.sin(ang) * (ry * 1.75)
        dome_pts.append((px, py))
    dome_pts.append((cx + rx, base_y + 2 * s))

    arcade.draw_polygon_filled(dome_pts, slime_main)
    arcade.draw_polygon_outline(dome_pts, slime_outline, 2.5)

    # 4. Внутренние тёмно-оливковые пятна-кратеры и глянцевый блик сбоку
    spots = (
        (-24, 34, 6.5),
        (-16, 56, 4.5),
        (18, 52, 5.5),
        (27, 28, 7.0),
        (-30, 14, 5.0),
        (31, 12, 4.5),
    )
    for sx, sy, sr in spots:
        arcade.draw_circle_filled(cx + sx * d * s, base_y + sy * s * (1.0 - squish), sr * s, slime_dark)

    # Длинный глянцевый блик вдоль правого/переднего края
    arcade.draw_arc_outline(
        cx + 4 * d * s,
        base_y + 16 * s,
        rx * 1.65,
        ry * 2.55,
        (238, 245, 195, 195),
        15 if d > 0 else 110,
        70 if d > 0 else 165,
        4.5,
    )

    # 5. Большой одиночный глаз с малиново-розовым контуром и нависшим веком
    eye_x = cx + 4 * d * s
    eye_y = base_y + 52 * s * (1.0 - squish)

    # Тёмно-бирюзовая тень под глазом и малиновая обводка
    arcade.draw_ellipse_filled(eye_x, eye_y - 2 * s, 28 * s, 22 * s, (48, 118, 102, 180))
    arcade.draw_ellipse_filled(eye_x, eye_y, 26 * s, 19 * s, (238, 62, 168))
    # Лаймовая радужка и чёрный зрачок с бликом
    arcade.draw_circle_filled(eye_x + 1 * d * s, eye_y + 1 * s, 7.5 * s, (132, 245, 42))
    arcade.draw_circle_filled(eye_x + 2 * d * s, eye_y + 1 * s, 3.8 * s, (14, 14, 18))
    arcade.draw_circle_filled(eye_x + 3.2 * d * s, eye_y + 2.5 * s, 1.5 * s, (255, 255, 255))

    # Приспущенное верхнее веко слизняка (придаёт хитрый взгляд)
    lid_rect = arcade.XYWH(eye_x, eye_y + 7.5 * s, 29 * s, 8 * s)
    arcade.draw_rect_filled(lid_rect, slime_main)
    arcade.draw_line(eye_x - 14 * s, eye_y + 3.5 * s, eye_x + 14 * s, eye_y + 3.5 * s, slime_outline, 2)

    # 6. Огромная зубастая пасть с розовым языком
    mx = cx + 3 * d * s
    my = base_y + 22 * s * (1.0 - squish)
    mw = 54 * s
    mh = 30 * s * (1.0 + squish * 0.8)

    # Тёмно-бордовая полость рта с толстым чёрным контуром
    mouth_poly = (
        (mx - mw * 0.52, my - mh * 0.48),
        (mx - mw * 0.44, my + mh * 0.38),
        (mx, my + mh * 0.52),
        (mx + mw * 0.44, my + mh * 0.38),
        (mx + mw * 0.52, my - mh * 0.48),
        (mx, my - mh * 0.34),
    )
    arcade.draw_polygon_filled(mouth_poly, (98, 26, 28))

    # Розовый язык внутри пасти
    tongue = (
        (mx - mw * 0.36, my - mh * 0.32),
        (mx - mw * 0.14, my + mh * 0.05),
        (mx - mw * 0.02, my - mh * 0.05),
        (mx - mw * 0.12, my - mh * 0.36),
    )
    arcade.draw_polygon_filled(tongue, (226, 138, 152))

    # Верхний ряд острых зубов (каждый зуб — отдельный треугольник вдоль верхнего края пасти)
    top_teeth_tris = (
        ((mx - mw * 0.43, my + mh * 0.37), (mx - mw * 0.23, my + mh * 0.43), (mx - mw * 0.33, my + mh * 0.12)),
        ((mx - mw * 0.23, my + mh * 0.43), (mx, my + mh * 0.50), (mx - mw * 0.11, my + mh * 0.14)),
        ((mx, my + mh * 0.50), (mx + mw * 0.23, my + mh * 0.43), (mx + mw * 0.11, my + mh * 0.14)),
        ((mx + mw * 0.23, my + mh * 0.43), (mx + mw * 0.43, my + mh * 0.37), (mx + mw * 0.33, my + mh * 0.12)),
    )
    for tri in top_teeth_tris:
        arcade.draw_polygon_filled(tri, (245, 246, 248))

    # Нижний ряд острых зубов (отдельными треугольниками вдоль нижнего края пасти)
    bot_teeth_tris = (
        ((mx - mw * 0.48, my - mh * 0.45), (mx - mw * 0.24, my - mh * 0.39), (mx - mw * 0.35, my - mh * 0.16)),
        ((mx - mw * 0.24, my - mh * 0.39), (mx, my - mh * 0.33), (mx - mw * 0.12, my - mh * 0.12)),
        ((mx, my - mh * 0.33), (mx + mw * 0.24, my - mh * 0.39), (mx + mw * 0.12, my - mh * 0.12)),
        ((mx + mw * 0.24, my - mh * 0.39), (mx + mw * 0.48, my - mh * 0.45), (mx + mw * 0.35, my - mh * 0.16)),
    )
    for tri in bot_teeth_tris:
        arcade.draw_polygon_filled(tri, (245, 246, 248))

    # Жирный чёрный контур пасти поверх всего
    arcade.draw_polygon_outline(mouth_poly, (16, 16, 18), 3)

def _draw_thief(cx: float, cy: float, s: float, d: float, t: float, b: float):
    """Детализированный спрайт Ночного Вора по референсу (стремительный выпад, маска, 2 клинка, шарф)."""
    bob = math.sin(t * 3.8) * 2.5 * s
    scarf_wave = math.sin(t * 5.2) * 4.5 * s

    cloth_dark = (22, 24, 30)
    cloth_mid = (36, 40, 50)
    chainmail = (58, 64, 76)
    silver = (178, 186, 198)
    silver_dark = (105, 112, 124)
    belt_indigo = (58, 54, 82)
    blade_dark = (32, 36, 44)
    blade_edge = (218, 226, 236)

    # 1. Длинный рваный чёрный шарф, развевающийся за спиной
    scarf_pts = (
        (cx + 8 * d * s, cy + 22 * s + bob),
        (cx - 18 * d * s, cy + 44 * s + scarf_wave * 0.5),
        (cx - 46 * d * s, cy + 46 * s + scarf_wave),
        (cx - 38 * d * s, cy + 39 * s + scarf_wave * 0.8),
        (cx - 50 * d * s, cy + 35 * s + scarf_wave * 1.1),
        (cx - 22 * d * s, cy + 34 * s + scarf_wave * 0.4),
        (cx + 4 * d * s, cy + 16 * s + bob),
    )
    arcade.draw_polygon_filled(scarf_pts, cloth_dark)
    arcade.draw_polygon_outline(scarf_pts, silver_dark, 1.2)

    # 2. Задняя нога, отброшенная назад в прыжке, и передняя согнутая нога
    # Задняя нога
    hip_x, hip_y = cx - 10 * d * s, cy - 6 * s + bob * 0.5
    bk_x, bk_y = cx - 28 * d * s, cy - 22 * s
    bf_x, bf_y = cx - 44 * d * s, cy - 46 * s
    arcade.draw_line(hip_x, hip_y, bk_x, bk_y, cloth_dark, 10)
    arcade.draw_line(bk_x, bk_y, bf_x, bf_y, cloth_mid, 8)
    arcade.draw_line(bk_x, bk_y, bf_x, bf_y, silver_dark, 2)
    arcade.draw_ellipse_filled(bf_x - 2 * d * s, bf_y - 2 * s, 12 * s, 8 * s, (18, 18, 22))

    # Передняя опорная нога (глубокий выпад)
    fk_x, fk_y = cx - 8 * d * s, cy - 26 * s
    ff_x, ff_y = cx - 22 * d * s, cy - 48 * s
    arcade.draw_line(hip_x + 4 * d * s, hip_y, fk_x, fk_y, cloth_mid, 11)
    arcade.draw_line(fk_x, fk_y, ff_x, ff_y, cloth_dark, 8.5)
    # Серебряный наколенник и понож
    arcade.draw_circle_filled(fk_x + 2 * d * s, fk_y, 4.5 * s, silver_dark)
    arcade.draw_line(fk_x + 2 * d * s, fk_y, ff_x + 2 * d * s, ff_y, silver, 2)
    arcade.draw_ellipse_filled(ff_x + 3 * d * s, ff_y - 2 * s, 13 * s, 8 * s, (18, 18, 22))

    # 3. Задняя рука, высоко заносящая первый кинжал за спиной
    sh_bx, sh_by = cx - 6 * d * s, cy + 16 * s + bob
    el_bx, el_by = cx - 26 * d * s, cy + 28 * s + bob
    hd_bx, hd_by = cx - 42 * d * s, cy + 14 * s + bob

    arcade.draw_line(sh_bx, sh_by, el_bx, el_by, chainmail, 7)
    arcade.draw_line(el_bx, el_by, hd_bx, hd_by, cloth_dark, 6.5)
    arcade.draw_circle_filled(el_bx, el_by, 4 * s, silver_dark)

    # Верхний кинжал (клинок смотрит вверх и слегка вперёд)
    tip1_x = hd_bx + 8 * d * s
    tip1_y = hd_by + 36 * s
    dagger1 = (
        (hd_bx - 2 * d * s, hd_by + 4 * s),
        (hd_bx + 3 * d * s, hd_by + 4 * s),
        (tip1_x, tip1_y),
    )
    arcade.draw_polygon_filled(dagger1, blade_dark)
    arcade.draw_line(hd_bx + 3 * d * s, hd_by + 4 * s, tip1_x, tip1_y, blade_edge, 2)
    # Круглая гарда и рукоять с кисточкой
    arcade.draw_ellipse_filled(hd_bx, hd_by + 4 * s, 12 * s, 5 * s, silver_dark)
    arcade.draw_line(hd_bx, hd_by, hd_bx - 3 * d * s, hd_by - 9 * s, cloth_mid, 3.5)
    arcade.draw_circle_filled(hd_bx - 5 * d * s, hd_by - 11 * s, 3 * s, silver)
    arcade.draw_circle_filled(hd_bx, hd_by, 4.5 * s, cloth_dark)

    # 4. Наклонённый вперёд бронированный торс и пояс с набедренными щитками
    torso = (
        (cx - 16 * d * s, cy - 8 * s + bob * 0.5),
        (cx - 10 * d * s, cy + 20 * s + bob),
        (cx + 16 * d * s, cy + 16 * s + bob),
        (cx + 8 * d * s, cy - 10 * s + bob * 0.5),
    )
    arcade.draw_polygon_filled(torso, cloth_dark)
    arcade.draw_polygon_outline(torso, silver_dark, 1.5)

    # Серебристый нагрудник и узорчатый пояс
    arcade.draw_arc_outline(cx + 3 * d * s, cy + 8 * s + bob, 22 * s, 18 * s, silver, 200, 340, 2.2)
    belt_poly = (
        (cx - 16 * d * s, cy - 4 * s + bob * 0.5),
        (cx + 8 * d * s, cy - 7 * s + bob * 0.5),
        (cx + 12 * d * s, cy - 16 * s + bob * 0.4),
        (cx - 20 * d * s, cy - 13 * s + bob * 0.4),
    )
    arcade.draw_polygon_filled(belt_poly, belt_indigo)
    arcade.draw_polygon_outline(belt_poly, silver, 1.5)

    # 5. Голова в шлеме-капюшоне с серебряной чеканкой и маской
    hx = cx + 18 * d * s
    hy = cy + 18 * s + bob
    arcade.draw_circle_filled(hx, hy, 11 * s, cloth_dark)
    arcade.draw_circle_outline(hx, hy, 11 * s, silver_dark, 1.5)

    # Серебряная налобная пластина-корона и защитная маска на нижней половине лица
    brow_plate = (
        (hx - 6 * d * s, hy + 4 * s),
        (hx + 2 * d * s, hy + 11 * s),
        (hx + 11 * d * s, hy + 5 * s),
        (hx + 4 * d * s, hy + 1 * s),
    )
    arcade.draw_polygon_filled(brow_plate, silver)
    arcade.draw_polygon_outline(brow_plate, silver_dark, 1.2)

    mask_poly = (
        (hx - 3 * d * s, hy - 1 * s),
        (hx + 10 * d * s, hy - 1 * s),
        (hx + 8 * d * s, hy - 10 * s),
        (hx - 1 * d * s, hy - 10 * s),
    )
    arcade.draw_polygon_filled(mask_poly, cloth_mid)
    arcade.draw_polygon_outline(mask_poly, silver_dark, 1.2)

    # Узкий прищуренный светящийся глаз в прорези маски
    arcade.draw_line(hx + 2 * d * s, hy + 1.5 * s, hx + 8 * d * s, hy + 0.5 * s, (215, 235, 255), 2.5)

    # 6. Передняя рука, вытянутая вперёд и вниз со вторым кинжалом
    sh_fx, sh_fy = cx + 10 * d * s, cy + 10 * s + bob
    el_fx, el_fy = cx + 22 * d * s, cy - 4 * s + bob * 0.8
    hd_fx, hd_fy = cx + 15 * d * s, cy - 16 * s + bob * 0.6

    # Наплечник с серебряным кантом
    arcade.draw_circle_filled(sh_fx, sh_fy, 6.5 * s, cloth_mid)
    arcade.draw_circle_outline(sh_fx, sh_fy, 6.5 * s, silver, 1.5)

    arcade.draw_line(sh_fx, sh_fy, el_fx, el_fy, chainmail, 7)
    arcade.draw_line(el_fx, el_fy, hd_fx, hd_fy, cloth_dark, 6.5)
    arcade.draw_circle_filled(el_fx, el_fy, 4 * s, silver)

    # Нижний клинок (направлен по диагонали вперёд и вниз)
    tip2_x = hd_fx + 36 * d * s
    tip2_y = hd_fy - 14 * s
    dagger2 = (
        (hd_fx + 4 * d * s, hd_fy + 1 * s),
        (hd_fx + 2 * d * s, hd_fy - 4 * s),
        (tip2_x, tip2_y),
    )
    arcade.draw_polygon_filled(dagger2, blade_dark)
    arcade.draw_line(hd_fx + 2 * d * s, hd_fy - 4 * s, tip2_x, tip2_y, blade_edge, 2)
    # Гарда и обратная рукоять
    arcade.draw_ellipse_filled(hd_fx + 4 * d * s, hd_fy - 1 * s, 5 * s, 12 * s, silver_dark)
    arcade.draw_line(hd_fx, hd_fy, hd_fx - 10 * d * s, hd_fy + 4 * s, cloth_mid, 3.5)
    arcade.draw_circle_filled(hd_fx - 12 * d * s, hd_fy + 5 * s, 3 * s, silver)
    arcade.draw_circle_filled(hd_fx, hd_fy, 4.5 * s, cloth_dark)

def _draw_ogre(cx: float, cy: float, s: float, d: float, t: float, b: float):
    """Детализированный спрайт Пещерного Огра по референсу (каменный молот, портупея, гоблин на спине)."""
    stomp = abs(math.sin(t * 2.4)) * 3.0 * s

    skin = (188, 174, 158)
    skin_light = (212, 198, 182)
    skin_shadow = (138, 124, 110)
    iron = (84, 78, 74)
    iron_dark = (48, 44, 42)
    leather = (78, 56, 42)
    stone = (176, 168, 156)
    stone_dark = (124, 116, 106)

    # 1. Задняя опорная нога и поднятая в шаге передняя нога
    # Задняя мощная нога
    arcade.draw_line(cx - 16 * d * s, cy - 10 * s, cx - 24 * d * s, cy - 30 * s, skin_shadow, 13)
    arcade.draw_line(cx - 24 * d * s, cy - 30 * s, cx - 26 * d * s, cy - 50 * s, skin, 11)
    arcade.draw_ellipse_filled(cx - 23 * d * s, cy - 51 * s, 16 * s, 7 * s, skin_shadow)

    # Передняя нога, занесённая в тяжёлом шаге
    fk_x, fk_y = cx + 14 * d * s, cy - 22 * s + stomp * 0.5
    ff_x, ff_y = cx + 22 * d * s, cy - 38 * s + stomp
    arcade.draw_line(cx + 8 * d * s, cy - 10 * s, fk_x, fk_y, skin_light, 14)
    arcade.draw_line(fk_x, fk_y, ff_x, ff_y, skin, 11)
    arcade.draw_ellipse_filled(ff_x + 5 * d * s, ff_y - 2 * s, 17 * s, 8 * s, skin_light)

    # 2. Массивный сгорбленный торс и рваная набедренная повязка
    torso = (
        (cx - 28 * d * s, cy - 8 * s),
        (cx - 32 * d * s, cy + 24 * s + b),
        (cx - 8 * d * s, cy + 40 * s + b),
        (cx + 22 * d * s, cy + 32 * s + b),
        (cx + 24 * d * s, cy - 6 * s),
    )
    arcade.draw_polygon_filled(torso, skin)
    arcade.draw_polygon_outline(torso, skin_shadow, 2)

    # Спинные шипы и грудные мышцы
    for sx, sy in ((-28, 30), (-22, 36), (-15, 40)):
        spike = (
            (cx + sx * d * s, cy + sy * s + b),
            (cx + (sx - 6) * d * s, cy + (sy + 7) * s + b),
            (cx + (sx + 4) * d * s, cy + (sy + 2) * s + b),
        )
        arcade.draw_polygon_filled(spike, (195, 185, 165))

    arcade.draw_arc_outline(cx + 8 * d * s, cy + 12 * s + b, 24 * s, 16 * s, skin_shadow, 190, 340, 2)

    # Рваная тёмно-коричневая набедренная повязка
    loincloth = (
        (cx - 22 * d * s, cy - 6 * s),
        (cx + 18 * d * s, cy - 6 * s),
        (cx + 14 * d * s, cy - 26 * s),
        (cx + 3 * d * s, cy - 20 * s),
        (cx - 6 * d * s, cy - 28 * s),
        (cx - 18 * d * s, cy - 22 * s),
    )
    arcade.draw_polygon_filled(loincloth, (65, 45, 34))
    arcade.draw_polygon_outline(loincloth, iron_dark, 1.5)

    # 3. Кожаная портупея с железным кольцом на груди и кованый наплечник
    ring_x, ring_y = cx + 8 * d * s, cy + 14 * s + b
    arcade.draw_line(cx - 18 * d * s, cy + 34 * s + b, ring_x, ring_y, leather, 5)
    arcade.draw_line(cx + 18 * d * s, cy + 30 * s + b, ring_x, ring_y, leather, 5)
    arcade.draw_line(ring_x, ring_y, cx + 6 * d * s, cy - 6 * s, leather, 4.5)
    arcade.draw_circle_outline(ring_x, ring_y, 4.5 * s, iron, 2.5)

    # Тяжёлый металлический наплечник на переднем плече
    pauldron = (
        (cx + 10 * d * s, cy + 35 * s + b),
        (cx + 28 * d * s, cy + 32 * s + b),
        (cx + 31 * d * s, cy + 18 * s + b),
        (cx + 12 * d * s, cy + 20 * s + b),
    )
    arcade.draw_polygon_filled(pauldron, iron)
    arcade.draw_polygon_outline(pauldron, iron_dark, 2)

    # 4. Маленький зелёный гоблин-наездник на плечах огра
    gx = cx - 8 * d * s
    gy = cy + 44 * s + b + math.sin(t * 4.5) * 1.5 * s
    arcade.draw_ellipse_filled(gx, gy, 11 * s, 14 * s, (135, 175, 58))
    arcade.draw_circle_filled(gx + 2 * d * s, gy + 10 * s, 6 * s, (152, 194, 72))
    # Острые уши и кинжал гоблина
    arcade.draw_line(gx + 2 * d * s, gy + 11 * s, gx - 7 * d * s, gy + 15 * s, (125, 165, 50), 2.5)
    arcade.draw_line(gx + 4 * d * s, gy + 11 * s, gx + 12 * d * s, gy + 14 * s, (152, 194, 72), 2.5)
    arcade.draw_line(gx + 4 * d * s, gy + 3 * s, gx + 15 * d * s, gy + 6 * s, (135, 175, 58), 3)
    arcade.draw_line(gx + 15 * d * s, gy + 6 * s, gx + 25 * d * s, gy + 11 * s, (215, 222, 228), 2)

    # 5. Голова огра в рогатом шлеме-маске с клыками
    hx = cx + 8 * d * s
    hy = cy + 28 * s + b
    # Нижняя челюсть с клыками
    arcade.draw_ellipse_filled(hx + 2 * d * s, hy - 5 * s, 21 * s, 14 * s, skin_light)
    arcade.draw_line(hx - 4 * d * s, hy - 7 * s, hx + 8 * d * s, hy - 7 * s, (42, 32, 28), 2)
    for tx in (-2, 5):
        arcade.draw_polygon_filled(
            ((hx + (tx - 1.5) * d * s, hy - 7 * s), (hx + (tx + 1.5) * d * s, hy - 7 * s), (hx + tx * d * s, hy - 2 * s)),
            (238, 232, 212),
        )

    # Железный шлем, закрывающий глаза
    arcade.draw_arc_filled(hx, hy + 2 * s, 24 * s, 22 * s, iron, 0, 180)
    arcade.draw_rect_filled(arcade.XYWH(hx + 1 * d * s, hy + 1 * s, 22 * s, 6 * s), iron_dark)
    arcade.draw_line(hx - 10 * d * s, hy + 1 * s, hx + 11 * d * s, hy + 1 * s, (145, 132, 118), 1.5)
    # Изогнутый рог шлема
    horn = ((hx - 6 * d * s, hy + 8 * s), (hx - 18 * d * s, hy + 17 * s), (hx - 10 * d * s, hy + 3 * s))
    arcade.draw_polygon_filled(horn, (182, 168, 142))
    arcade.draw_polygon_outline(horn, iron_dark, 1.5)

    # 6. Могучие руки и огромный двуручный каменный молот
    # Задняя рука
    el_bx, el_by = cx - 32 * d * s, cy + 4 * s + b * 0.7
    hd_bx, hd_by = cx - 18 * d * s, cy - 8 * s + b * 0.5
    arcade.draw_line(cx - 24 * d * s, cy + 22 * s + b, el_bx, el_by, skin_shadow, 11)
    arcade.draw_line(el_bx, el_by, hd_bx, hd_by, skin, 10)

    # Передняя рука
    el_fx, el_fy = cx + 26 * d * s, cy + 4 * s + b * 0.7
    hd_fx, hd_fy = cx + 16 * d * s, cy - 2 * s + b * 0.5
    arcade.draw_line(cx + 20 * d * s, cy + 20 * s + b, el_fx, el_fy, skin_light, 11)
    arcade.draw_line(el_fx, el_fy, hd_fx, hd_fy, skin, 10)

    # Длинное древко молота через обе руки
    shaft_back = (cx - 48 * d * s, cy - 16 * s + b * 0.4)
    shaft_front = (cx + 42 * d * s, cy + 8 * s + b * 0.6)
    arcade.draw_line(*shaft_back, *shaft_front, (58, 46, 38), 6.5)

    # Шипастое навершие сзади
    arcade.draw_circle_filled(*shaft_back, 6 * s, iron)
    arcade.draw_line(shaft_back[0], shaft_back[1] - 8 * s, shaft_back[0], shaft_back[1] + 8 * s, iron_dark, 3)

    # Огромный валун-боёк спереди, стянутый железными полосами
    mx, my = shaft_front
    boulder = (
        (mx - 10 * d * s, my + 16 * s),
        (mx + 8 * d * s, my + 24 * s),
        (mx + 24 * d * s, my + 12 * s),
        (mx + 22 * d * s, my - 12 * s),
        (mx + 4 * d * s, my - 22 * s),
        (mx - 12 * d * s, my - 10 * s),
    )
    arcade.draw_polygon_filled(boulder, stone)
    arcade.draw_polygon_outline(boulder, iron_dark, 2.2)
    # Внутренние грани валуна и железные обручи
    arcade.draw_polygon_filled(
        ((mx + 4 * d * s, my - 22 * s), (mx + 22 * d * s, my - 12 * s), (mx + 12 * d * s, my - 2 * s)),
        stone_dark,
    )
    arcade.draw_line(mx - 4 * d * s, my + 19 * s, mx + 12 * d * s, my - 18 * s, iron, 4.5)
    arcade.draw_line(mx - 11 * d * s, my + 4 * s, mx + 23 * d * s, my - 2 * s, iron_dark, 4)

    # Кулаки поверх древка
    arcade.draw_circle_filled(hd_bx, hd_by, 6.5 * s, skin_light)
    arcade.draw_circle_outline(hd_bx, hd_by, 6.5 * s, skin_shadow, 1.5)
    arcade.draw_circle_filled(hd_fx, hd_fy, 6.5 * s, skin_light)
    arcade.draw_circle_outline(hd_fx, hd_fy, 6.5 * s, skin_shadow, 1.5)


def _draw_skeleton_archer(cx: float, cy: float, s: float, d: float, t: float, b: float):
    """Детализированный спрайт Скелета-Лучника по референсу (синеватый наплечник, колчан со стрелами, длинный лук)."""
    aim_sway = math.sin(t * 2.4) * 1.5 * s

    bone = (206, 196, 174)
    bone_light = (228, 220, 200)
    bone_shadow = (142, 132, 114)
    steel_blue = (118, 138, 158)
    steel_dark = (66, 76, 90)
    leather = (76, 54, 38)
    leather_dark = (48, 34, 24)
    rag_red = (142, 68, 66)
    wood_bow = (154, 128, 84)

    # 1. Колчан за спиной/поясом и торчащие стрелы с красноватым оперением
    q_bot = (cx + 12 * d * s, cy - 16 * s)
    q_top = (cx - 26 * d * s, cy + 4 * s + b * 0.5)

    # Стрелы в колчане (рисуем до колчана, чтобы древка уходили внутрь)
    for idx, (ang_off, len_off) in enumerate(((-4, 18), (0, 22), (4, 16), (8, 20))):
        ax1 = q_top[0] - 2 * d * s
        ay1 = q_top[1] + (idx - 1.5) * 2 * s
        ax2 = ax1 - (16 + len_off * 0.3) * d * s
        ay2 = ay1 + (14 + ang_off) * s
        arcade.draw_line(ax1, ay1, ax2, ay2, (192, 176, 136), 2)
        # Красновато-розовое оперение
        feather = (
            (ax2 + 3 * d * s, ay2 - 2 * s),
            (ax2 - 5 * d * s, ay2 + 4 * s),
            (ax2 - 2 * d * s, ay2 - 4 * s),
        )
        arcade.draw_polygon_filled(feather, rag_red)

    # Кожаный корпус колчана
    arcade.draw_line(q_bot[0], q_bot[1], q_top[0], q_top[1], leather, 11)
    arcade.draw_ellipse_filled(q_top[0], q_top[1], 7 * s, 12 * s, leather_dark)
    arcade.draw_ellipse_outline(q_top[0], q_top[1], 7 * s, 12 * s, (115, 86, 62), 1.5)

    # 2. Костистые ноги и сегментированный стальной набедренник спереди
    # Задняя нога
    arcade.draw_line(cx - 8 * d * s, cy - 6 * s, cx - 14 * d * s, cy - 28 * s, bone_shadow, 4)
    arcade.draw_line(cx - 14 * d * s, cy - 28 * s, cx - 16 * d * s, cy - 50 * s, bone, 3.5)
    arcade.draw_line(cx - 17 * d * s, cy - 50 * s, cx - 8 * d * s, cy - 52 * s, bone, 3)

    # Передняя нога
    fk_x, fk_y = cx + 11 * d * s, cy - 26 * s
    ff_x, ff_y = cx + 10 * d * s, cy - 50 * s
    arcade.draw_line(cx + 8 * d * s, cy - 6 * s, fk_x, fk_y, bone, 4)
    arcade.draw_line(fk_x, fk_y, ff_x, ff_y, bone_shadow, 3.5)
    arcade.draw_line(ff_x - 2 * d * s, ff_y, ff_x + 8 * d * s, ff_y - 2 * s, bone, 3)

    # Сегментированный стальной щиток на переднем бедре (как на референсе)
    for seg in range(4):
        sy = cy - (8 + seg * 4.5) * s
        sx = cx + (8 + seg * 0.6) * d * s
        arcade.draw_rect_filled(arcade.XYWH(sx, sy, 11 * s, 4.5 * s), steel_blue)
        arcade.draw_rect_outline(arcade.XYWH(sx, sy, 11 * s, 4.5 * s), steel_dark, 1.2)

    # 3. Таз, пояс, бордовая набедренная повязка и рукоять кинжала
    arcade.draw_ellipse_filled(cx, cy - 4 * s, 22 * s, 9 * s, bone_shadow)
    loincloth = (
        (cx + 2 * d * s, cy - 5 * s),
        (cx + 14 * d * s, cy - 5 * s),
        (cx + 15 * d * s, cy - 24 * s),
        (cx + 4 * d * s, cy - 21 * s),
    )
    arcade.draw_polygon_filled(loincloth, rag_red)
    arcade.draw_polygon_outline(loincloth, (82, 36, 36), 1.2)
    arcade.draw_line(cx - 12 * d * s, cy - 3 * s, cx + 13 * d * s, cy - 5 * s, leather_dark, 4)

    # Рукоять запасного кинжала у пояса
    arcade.draw_line(cx + 14 * d * s, cy - 6 * s, cx + 20 * d * s, cy - 1 * s, steel_blue, 3.5)
    arcade.draw_circle_filled(cx + 21 * d * s, cy, 2.5 * s, steel_dark)

    # 4. Позвоночник и грудная клетка с рёбрами
    arcade.draw_line(cx - 1 * d * s, cy - 2 * s, cx - 2 * d * s, cy + 40 * s + b, bone_shadow, 4)
    for idx, ry in enumerate((10, 15, 20, 25, 30)):
        rw = (10 + idx * 1.2) * s
        arcade.draw_arc_outline(cx + 2 * d * s, cy + ry * s + b, rw * 2, 7.5 * s, bone_light, 185, 355, 2.2)

    # Диагональная кожаная перевязь и две круглые стальные бляхи на груди
    arcade.draw_line(cx - 12 * d * s, cy + 32 * s + b, cx + 10 * d * s, cy - 4 * s, leather, 4)
    for bx, by, br in ((2, 27, 4.5), (-3, 18, 4.2)):
        arcade.draw_circle_filled(cx + bx * d * s, cy + by * s + b, br * s, steel_blue)
        arcade.draw_circle_outline(cx + bx * d * s, cy + by * s + b, br * s, steel_dark, 1.3)

    # 5. Задняя опущенная рука, рваная бордовая накидка и сегментированный стальной наплечник
    sh_bx, sh_by = cx - 15 * d * s, cy + 30 * s + b
    arcade.draw_line(sh_bx, sh_by, sh_bx - 3 * d * s, cy + 8 * s + b * 0.6, bone_shadow, 3.2)
    arcade.draw_line(sh_bx - 3 * d * s, cy + 8 * s + b * 0.6, sh_bx - 1 * d * s, cy - 12 * s, bone, 3)

    # Рваная бордовая ткань на плече
    rag_shoulder = (
        (cx - 18 * d * s, cy + 34 * s + b),
        (cx + 2 * d * s, cy + 35 * s + b),
        (cx - 4 * d * s, cy + 22 * s + b),
        (cx - 21 * d * s, cy + 16 * s + b),
    )
    arcade.draw_polygon_filled(rag_shoulder, rag_red)

    # Сегментированный синевато-стальной наплечник
    for p_idx in range(3):
        py = cy + (31 - p_idx * 4.5) * s + b
        px = cx - (14 + p_idx * 1.2) * d * s
        arcade.draw_ellipse_filled(px, py, 16 * s, 8 * s, steel_blue)
        arcade.draw_ellipse_outline(px, py, 16 * s, 8 * s, steel_dark, 1.5)

    # 6. Горделиво приподнятый череп с тёмными глазницами
    hx = cx - 2 * d * s
    hy = cy + 47 * s + b
    arcade.draw_rect_filled(arcade.XYWH(hx + 3 * d * s, hy - 6 * s, 9 * s, 6 * s), bone_shadow)
    arcade.draw_circle_filled(hx, hy + 2 * s, 9.5 * s, bone_light)
    arcade.draw_circle_outline(hx, hy + 2 * s, 9.5 * s, bone_shadow, 1.3)
    # Глазницы и нос (направлены чуть вверх, как на референсе)
    arcade.draw_circle_filled(hx + 2 * d * s, hy + 3.5 * s, 2.5 * s, (18, 16, 20))
    arcade.draw_circle_filled(hx + 7 * d * s, hy + 4.5 * s, 2.1 * s, (18, 16, 20))
    arcade.draw_line(hx + 1 * d * s, hy - 3 * s, hx + 7 * d * s, hy - 2 * s, (30, 26, 28), 1.5)

    # 7. Передняя рука с кожаным наручем, вытянутая влево (в сторону игрока)
    sh_fx, sh_fy = cx - 12 * s, cy + 28 * s + b
    el_fx, el_fy = cx - 22 * s, cy + 14 * s + b * 0.8
    hd_fx, hd_fy = cx - 32 * s + aim_sway, cy + 6 * s + b * 0.6

    arcade.draw_line(sh_fx, sh_fy, el_fx, el_fy, bone, 3.5)
    arcade.draw_line(el_fx, el_fy, hd_fx, hd_fy, bone_light, 3.5)
    # Кожаный наруч на запястье и костистая кисть
    arcade.draw_line(el_fx - 4 * s, el_fy - 3 * s, hd_fx + 2 * s, hd_fy + 2 * s, leather, 6)
    arcade.draw_circle_filled(hd_fx, hd_fy, 3.8 * s, bone_light)

    # Правильный лук: рукоять слева (у игрока), плечи загибаются вправо (к скелету), тетива со стороны скелета
    bow_top = (hd_fx + 15 * s, hd_fy + 42 * s)
    bow_bot = (hd_fx + 15 * s, hd_fy - 42 * s)
    bow_mid_top = (hd_fx + 4 * s, hd_fy + 18 * s)
    bow_mid_bot = (hd_fx + 4 * s, hd_fy - 18 * s)

    # Тетива (натянута вертикально со стороны скелета)
    arcade.draw_line(*bow_top, *bow_bot, (220, 215, 200, 200), 1.4)

    # Деревянное древко лука (выгнуто дугой влево — в сторону игрока)
    arcade.draw_line(*bow_top, *bow_mid_top, wood_bow, 4)
    arcade.draw_line(*bow_mid_top, hd_fx, hd_fy, (122, 98, 62), 5)
    arcade.draw_line(hd_fx, hd_fy, *bow_mid_bot, (122, 98, 62), 5)
    arcade.draw_line(*bow_mid_bot, *bow_bot, wood_bow, 4)

    # Деревянные плечи лука (дуга выгнута в сторону игрока)
    arcade.draw_line(*bow_top, *bow_mid_top, wood_bow, 4)
    arcade.draw_line(*bow_mid_top, hd_fx, hd_fy, (122, 98, 62), 5)
    arcade.draw_line(hd_fx, hd_fy, *bow_mid_bot, (122, 98, 62), 5)
    arcade.draw_line(*bow_mid_bot, *bow_bot, wood_bow, 4)

    # Тетива
    arcade.draw_line(*bow_top, *bow_bot, (215, 210, 195, 190), 1.3)

    # Деревянные плечи лука
    arcade.draw_line(*bow_top, *bow_mid_top, wood_bow, 4)
    arcade.draw_line(*bow_mid_top, hd_fx, hd_fy, (122, 98, 62), 5)
    arcade.draw_line(hd_fx, hd_fy, *bow_mid_bot, (122, 98, 62), 5)
    arcade.draw_line(*bow_mid_bot, *bow_bot, wood_bow, 4)

def _draw_goblin_king(cx: float, cy: float, s: float, d: float, t: float, b: float):
    """Детализированный спрайт Босса: Короля Гоблинов по референсу."""
    belly_bob = math.sin(t * 2.6) * 2.2 * s

    skin = (146, 178, 56)
    skin_light = (176, 206, 78)
    skin_dark = (96, 124, 34)
    steel = (148, 162, 176)
    steel_dark = (82, 92, 104)
    wood_club = (156, 102, 48)
    wood_dark = (104, 64, 28)
    bone = (224, 218, 204)
    leather = (96, 56, 36)

    # 1. Короткие мощные ноги с когтистыми ступнями и набедренная повязка
    for side, lx in ((-1, cx - 18 * d * s), (1, cx + 16 * d * s)):
        arcade.draw_line(lx, cy - 16 * s, lx + side * 4 * d * s, cy - 34 * s, skin_dark, 13)
        arcade.draw_line(lx + side * 4 * d * s, cy - 34 * s, lx, cy - 48 * s, skin, 11)
        # Когтистая ступня
        foot_x = lx + 3 * d * s
        arcade.draw_ellipse_filled(foot_x, cy - 50 * s, 18 * s, 7 * s, skin)
        arcade.draw_ellipse_outline(foot_x, cy - 50 * s, 18 * s, 7 * s, skin_dark, 1.5)
        for claw in (-4, 0, 4):
            arcade.draw_circle_filled(foot_x + (7 + claw * 0.4) * d * s, cy - 51 * s, 2.2 * s, (135, 115, 58))

    # 2. Поднятая рука с деревянной дубиной на костяной рукояти (спереди по взгляду)
    sh_fx, sh_fy = cx + 22 * d * s, cy + 20 * s + b
    el_fx, el_fy = cx + 36 * d * s, cy + 28 * s + b
    hd_fx, hd_fy = cx + 44 * d * s, cy + 40 * s + b

    arcade.draw_line(sh_fx, sh_fy, el_fx, el_fy, skin, 11)
    arcade.draw_line(el_fx, el_fy, hd_fx, hd_fy, skin_light, 10)
    # Шипастый стальной браслет на запястье
    arcade.draw_circle_filled(hd_fx - 3 * d * s, hd_fy - 4 * s, 6 * s, steel)
    arcade.draw_circle_outline(hd_fx - 3 * d * s, hd_fy - 4 * s, 6 * s, steel_dark, 1.5)

    # Костяная рукоять и массивная деревянная дубина вверх
    arcade.draw_line(hd_fx - 7 * d * s, hd_fy - 9 * s, hd_fx + 5 * d * s, hd_fy + 7 * s, bone, 5)
    club_poly = (
        (hd_fx + 2 * d * s, hd_fy + 6 * s),
        (hd_fx + 8 * d * s, hd_fy + 2 * s),
        (hd_fx + 26 * d * s, hd_fy + 34 * s),
        (hd_fx + 18 * d * s, hd_fy + 46 * s),
        (hd_fx + 4 * d * s, hd_fy + 38 * s),
    )
    arcade.draw_polygon_filled(club_poly, wood_club)
    arcade.draw_polygon_outline(club_poly, wood_dark, 2)
    arcade.draw_circle_filled(hd_fx, hd_fy, 6 * s, skin_light)

    # 3. Огромное пузо и коренастый торс
    # Верхняя грудная клетка
    arcade.draw_ellipse_filled(cx + 2 * d * s, cy + 12 * s + b, 52 * s, 38 * s, skin)
    # Огромный отвислый живот
    belly_x = cx + 5 * d * s
    belly_y = cy - 16 * s + belly_bob
    arcade.draw_ellipse_filled(belly_x, belly_y, 64 * s, 54 * s, skin)
    arcade.draw_ellipse_filled(belly_x + 4 * d * s, belly_y - 2 * s, 46 * s, 40 * s, skin_light)
    arcade.draw_ellipse_outline(belly_x, belly_y, 64 * s, 54 * s, skin_dark, 2)
    # Пупок и складки груди
    arcade.draw_circle_filled(belly_x + 8 * d * s, belly_y - 4 * s, 2.5 * s, skin_dark)
    arcade.draw_arc_outline(cx + 12 * d * s, cy + 10 * s + b, 24 * s, 14 * s, skin_dark, 190, 345, 2)

    # Кожаный ремень на груди, цепь и белый череп-пряжка
    arcade.draw_line(cx - 22 * d * s, cy + 20 * s + b, cx + 26 * d * s, cy + 16 * s + b, leather, 5.5)
    for i in range(6):
        ch_x = cx + (14 - i * 5.5) * d * s
        ch_y = cy + (22 + math.sin(i * 0.7) * 3) * s + b
        arcade.draw_circle_outline(ch_x, ch_y, 3 * s, steel, 1.8)

    skull_x = cx + 14 * d * s
    skull_y = cy + 14 * s + b
    arcade.draw_circle_filled(skull_x, skull_y, 6.5 * s, bone)
    arcade.draw_rect_filled(arcade.XYWH(skull_x, skull_y - 4.5 * s, 7 * s, 5 * s), bone)
    arcade.draw_circle_filled(skull_x - 2.2 * s, skull_y + 1 * s, 1.6 * s, (24, 22, 24))
    arcade.draw_circle_filled(skull_x + 2.2 * s, skull_y + 1 * s, 1.6 * s, (24, 22, 24))

    # 4. Массивный шипастый наплечник и задняя рука с шипастым кольцом-кастетом
    sh_bx, sh_by = cx - 22 * d * s, cy + 22 * s + b
    el_bx, el_by = cx - 34 * d * s, cy + 4 * s + b * 0.7
    hd_bx, hd_by = cx - 38 * d * s, cy - 14 * s + b * 0.5

    arcade.draw_line(sh_bx, sh_by, el_bx, el_by, skin_dark, 11)
    arcade.draw_line(el_bx, el_by, hd_bx, hd_by, skin, 10)
    arcade.draw_circle_filled(hd_bx + 1 * d * s, hd_by + 4 * s, 6 * s, steel)

    # Шипастый стальной наплечник на плече
    pauldron = (
        (sh_bx + 8 * d * s, sh_by + 8 * s),
        (sh_bx - 14 * d * s, sh_by + 6 * s),
        (sh_bx - 16 * d * s, sh_by - 6 * s),
        (sh_bx + 6 * d * s, sh_by - 4 * s),
    )
    arcade.draw_polygon_filled(pauldron, steel)
    arcade.draw_polygon_outline(pauldron, steel_dark, 2)
    for sp_x, sp_y, dx_sp, dy_sp in (
        (-2, 8, -4, 14),
        (-8, 7, -14, 12),
        (-13, 3, -22, 5),
        (-6, 1, -13, 2),
    ):
        spike = (
            (sh_bx + sp_x * d * s, sh_by + sp_y * s),
            (sh_bx + (sp_x + 3) * d * s, sh_by + (sp_y - 3) * s),
            (sh_bx + dx_sp * d * s, sh_by + dy_sp * s),
        )
        arcade.draw_polygon_filled(spike, steel)
        arcade.draw_polygon_outline(spike, steel_dark, 1.2)

    # Стальной шипастый кастет-кольцо в задней руке
    ring_x, ring_y = hd_bx, hd_by - 10 * s
    arcade.draw_circle_outline(ring_x, ring_y, 11 * s, steel, 4.5)
    for deg in range(110, 340, 36):
        rad = math.radians(deg)
        sx1 = ring_x + math.cos(rad) * 11 * s
        sy1 = ring_y + math.sin(rad) * 11 * s
        sx2 = ring_x + math.cos(rad) * 21 * s
        sy2 = ring_y + math.sin(rad) * 21 * s
        arcade.draw_line(sx1, sy1, sx2, sy2, steel, 3)
    arcade.draw_circle_filled(hd_bx, hd_by, 6 * s, skin_light)

    # 5. Голова Короля Гоблинов: длинные уши с серьгой, широкий оскал и зубчатая корона с рубином
    hx = cx + 8 * d * s
    hy = cy + 38 * s + b

    # Длинные заострённые уши
    ear_back = ((hx - 12 * d * s, hy + 4 * s), (hx - 32 * d * s, hy + 8 * s), (hx - 20 * d * s, hy - 4 * s))
    ear_front = ((hx + 12 * d * s, hy + 4 * s), (hx + 30 * d * s, hy + 2 * s), (hx + 16 * d * s, hy - 5 * s))
    arcade.draw_polygon_filled(ear_back, skin)
    arcade.draw_polygon_outline(ear_back, skin_dark, 1.5)
    arcade.draw_polygon_filled(ear_front, skin_light)
    arcade.draw_polygon_outline(ear_front, skin_dark, 1.5)
    # Серьга-кольцо в ухе
    arcade.draw_circle_outline(hx - 17 * d * s, hy - 3 * s, 3.5 * s, steel, 1.8)

    # Голова и массивная челюсть
    arcade.draw_ellipse_filled(hx, hy, 30 * s, 26 * s, skin)
    arcade.draw_ellipse_filled(hx + 2 * d * s, hy - 8 * s, 26 * s, 14 * s, skin_light)
    arcade.draw_ellipse_outline(hx, hy, 30 * s, 26 * s, skin_dark, 1.8)

    # Глаза, хмурые складки и большой мясистый нос
    for ex in (-4, 8):
        arcade.draw_ellipse_filled(hx + ex * d * s, hy + 4 * s, 6.5 * s, 4.5 * s, (245, 240, 210))
        arcade.draw_circle_filled(hx + (ex + 1) * d * s, hy + 4 * s, 1.8 * s, (55, 22, 18))
        arcade.draw_line(hx + (ex - 4) * d * s, hy + 8 * s, hx + (ex + 4) * d * s, hy + 7 * s, skin_dark, 2.5)

    arcade.draw_ellipse_filled(hx + 4 * d * s, hy - 1 * s, 12 * s, 8 * s, skin_light)
    arcade.draw_ellipse_outline(hx + 4 * d * s, hy - 1 * s, 12 * s, 8 * s, skin_dark, 1.5)

    # Широкая зубастая ухмылка
    arcade.draw_arc_filled(hx + 3 * d * s, hy - 7 * s, 18 * s, 8 * s, (35, 22, 22), 185, 355)
    arcade.draw_line(hx - 5 * d * s, hy - 8 * s, hx + 11 * d * s, hy - 8 * s, (242, 240, 228), 2.5)

    # Высокая зубчатая стальная корона с рубином
    crown_y = hy + 11 * s
    arcade.draw_rect_filled(arcade.XYWH(hx, crown_y, 26 * s, 5 * s), steel)
    for dx_t, h_t in ((-10, 12), (-5, 17), (0, 24), (5, 17), (10, 12)):
        tooth = (
            (hx + (dx_t - 2.2) * s, crown_y + 2 * s),
            (hx + (dx_t + 2.2) * s, crown_y + 2 * s),
            (hx + dx_t * s, crown_y + h_t * s),
        )
        arcade.draw_polygon_filled(tooth, steel)
        arcade.draw_polygon_outline(tooth, steel_dark, 1.2)

    # Рубин в центре короны
    ruby = (
        (hx + 2 * d * s, crown_y + 6 * s),
        (hx + 5 * d * s, crown_y + 1 * s),
        (hx + 2 * d * s, crown_y - 4 * s),
        (hx - 1 * d * s, crown_y + 1 * s),
    )
    arcade.draw_polygon_filled(ruby, (215, 38, 42))
    arcade.draw_polygon_outline(ruby, (255, 195, 95), 1.2)

def _draw_dark_knight(cx: float, cy: float, s: float, d: float, t: float, b: float):
    """Детализированный спрайт Секретного Босса: Тёмного Магического Рыцаря по референсу."""
    flame_pulse = math.sin(t * 7.5) * 2.5 * s
    cape_sway = math.sin(t * 2.0) * 3.0 * s

    armor_dark = (26, 28, 34)
    armor_mid = (56, 62, 72)
    armor_light = (138, 148, 162)
    armor_rim = (195, 206, 220)
    fire_glow = (235, 115, 38)
    fire_core = (255, 225, 115)

    # 1. Тёмный тяжёлый плащ за спиной
    cape = (
        (cx - 22 * d * s, cy + 32 * s + b),
        (cx + 22 * d * s, cy + 32 * s + b),
        (cx + 36 * d * s + cape_sway, cy - 52 * s),
        (cx - 34 * d * s + cape_sway, cy - 52 * s),
    )
    arcade.draw_polygon_filled(cape, (14, 15, 20))
    arcade.draw_polygon_outline(cape, armor_mid, 1.5)

    # 2. Готические латные ноги, набедренные щитки и острые сабатоны
    for side, lx in ((-1, cx - 10 * d * s), (1, cx + 10 * d * s)):
        leg_col = armor_mid if side < 0 else (74, 58, 48)
        rim_col = armor_light if side < 0 else fire_glow

        # Бедро и голень
        arcade.draw_line(lx, cy - 4 * s, lx + side * 2 * d * s, cy - 26 * s, armor_dark, 11)
        arcade.draw_line(lx + side * 2 * d * s, cy - 26 * s, lx + side * 3 * d * s, cy - 49 * s, leg_col, 9)
        arcade.draw_line(lx + side * 2 * d * s, cy - 26 * s, lx + side * 3 * d * s, cy - 49 * s, rim_col, 2)

        # Острый наколенник и готические шипы на голени
        ky = cy - 25 * s
        arcade.draw_polygon_filled(
            ((lx - 4 * s, ky), (lx + 4 * s, ky), (lx, ky + 9 * s)),
            armor_rim if side < 0 else fire_glow,
        )
        # Сабатон (острый латный ботинок)
        foot_x = lx + side * 4 * d * s
        sabaton = (
            (foot_x - 5 * s, cy - 52 * s),
            (foot_x + 9 * d * s, cy - 52 * s),
            (foot_x + 4 * d * s, cy - 45 * s),
            (foot_x - 4 * s, cy - 46 * s),
        )
        arcade.draw_polygon_filled(sabaton, leg_col)
        arcade.draw_polygon_outline(sabaton, rim_col, 1.2)

    # Острые набедренные латные щитки (тассеты) и центральный клин
    for side in (-1, 1):
        tasset = (
            (cx + side * 6 * d * s, cy + 2 * s + b * 0.5),
            (cx + side * 20 * d * s, cy - 4 * s + b * 0.5),
            (cx + side * 24 * d * s, cy - 26 * s),
            (cx + side * 12 * d * s, cy - 20 * s),
        )
        arcade.draw_polygon_filled(tasset, armor_mid)
        arcade.draw_polygon_outline(tasset, armor_light if side < 0 else fire_glow, 1.5)

    center_tasset = ((cx - 5 * s, cy - 2 * s), (cx + 5 * s, cy - 2 * s), (cx, cy - 29 * s))
    arcade.draw_polygon_filled(center_tasset, armor_dark)
    arcade.draw_polygon_outline(center_tasset, armor_rim, 1.3)

    # 3. Ребристая готическая кираса с V-образными пластинами
    torso = (
        (cx - 14 * d * s, cy - 2 * s),
        (cx - 21 * d * s, cy + 30 * s + b),
        (cx + 21 * d * s, cy + 30 * s + b),
        (cx + 14 * d * s, cy - 2 * s),
    )
    arcade.draw_polygon_filled(torso, armor_dark)
    arcade.draw_polygon_outline(torso, armor_light, 1.8)

    # V-образные рельефные рёбра доспеха
    for ry in (6, 13, 20, 27):
        y_mid = cy + ry * s + b
        arcade.draw_line(cx - 14 * d * s, y_mid + 5 * s, cx, y_mid - 2 * s, armor_rim, 2.2)
        arcade.draw_line(cx, y_mid - 2 * s, cx + 14 * d * s, y_mid + 5 * s, fire_glow, 2.2)

    # 4. Многоярусные шипастые готические наплечники
    for side in (-1, 1):
        px = cx + side * 22 * d * s
        py = cy + 29 * s + b
        rim = armor_rim if side < 0 else (235, 175, 115)

        # 3 яруса веерных пластин-лезвий
        for tier in range(3):
            ty = py - tier * 5.5 * s
            tx_out = px + side * (16 - tier * 1.5) * d * s
            blade_p = (
                (px - side * 4 * d * s, ty + 4 * s),
                (tx_out, ty + 7 * s),
                (px + side * 6 * d * s, ty - 3 * s),
            )
            arcade.draw_polygon_filled(blade_p, armor_mid)
            arcade.draw_polygon_outline(blade_p, rim, 1.4)

        # Вертикальный рог-шип на плече
        top_horn = (
            (px - side * 2 * d * s, py + 4 * s),
            (px + side * 5 * d * s, py + 22 * s),
            (px + side * 7 * d * s, py + 3 * s),
        )
        arcade.draw_polygon_filled(top_horn, armor_light)
        arcade.draw_polygon_outline(top_horn, rim, 1.3)

    # 5. Высокий готический шлем-корона с рогами и тёмной лицевой маской
    hx = cx
    hy = cy + 43 * s + b
    helm = (
        (hx - 10 * s, hy - 6 * s),
        (hx - 11 * s, hy + 10 * s),
        (hx, hy + 15 * s),
        (hx + 11 * s, hy + 10 * s),
        (hx + 10 * s, hy - 6 * s),
        (hx, hy - 12 * s),
    )
    arcade.draw_polygon_filled(helm, armor_dark)
    arcade.draw_polygon_outline(helm, armor_rim, 1.8)

    # Четыре острых готических зубца короны шлема
    for dx_h, h_h in ((-7, 22), (-3, 29), (3, 29), (7, 22)):
        horn_pts = (
            (hx + (dx_h - 2) * s, hy + 9 * s),
            (hx + (dx_h + 2) * s, hy + 9 * s),
            (hx + dx_h * 1.15 * s, hy + h_h * s),
        )
        arcade.draw_polygon_filled(horn_pts, armor_light)
        arcade.draw_polygon_outline(horn_pts, armor_rim, 1.2)

    # Узкие прорези глазниц и решётка забрала
    arcade.draw_line(hx - 6 * s, hy + 3 * s, hx - 1.5 * s, hy + 1 * s, (255, 95, 45), 2.2)
    arcade.draw_line(hx + 6 * s, hy + 3 * s, hx + 1.5 * s, hy + 1 * s, (255, 95, 45), 2.2)
    for vx in (-3, 0, 3):
        arcade.draw_line(hx + vx * s, hy - 2 * s, hx + vx * s, hy - 9 * s, armor_mid, 1.2)

    # 6. Правая рука с зазубренным наручем и длинным прямым стальным мечом
    sh_rx, sh_ry = cx + 21 * d * s, cy + 22 * s + b
    el_rx, el_ry = cx + 28 * d * s, cy + 6 * s + b * 0.7
    hd_rx, hd_ry = cx + 24 * d * s, cy - 8 * s + b * 0.5

    arcade.draw_line(sh_rx, sh_ry, el_rx, el_ry, armor_dark, 8)
    arcade.draw_line(el_rx, el_ry, hd_rx, hd_ry, armor_mid, 8)
    # Шипастый наруч
    arcade.draw_line(el_rx + 3 * d * s, el_ry, hd_rx + 3 * d * s, hd_ry + 2 * s, armor_rim, 2)

    # Длинный прямой меч (направлен вперёд и вниз)
    tip_x = hd_rx + 32 * d * s
    tip_y = hd_ry - 42 * s
    sword_blade = (
        (hd_rx + 2 * d * s, hd_ry + 2 * s),
        (hd_rx + 6 * d * s, hd_ry - 2 * s),
        (tip_x, tip_y),
    )
    arcade.draw_polygon_filled(sword_blade, armor_rim)
    arcade.draw_polygon_outline(sword_blade, armor_dark, 1.5)
    arcade.draw_line(hd_rx + 4 * d * s, hd_ry, tip_x, tip_y, (240, 246, 255), 1.5)
    # Гарда и рукоять
    arcade.draw_line(hd_rx - 4 * d * s, hd_ry - 5 * s, hd_rx + 9 * d * s, hd_ry + 4 * s, armor_light, 4)
    arcade.draw_line(hd_rx, hd_ry, hd_rx - 7 * d * s, hd_ry + 8 * s, armor_dark, 4)
    arcade.draw_circle_filled(hd_rx, hd_ry, 4.5 * s, armor_mid)

    # 7. Левая рука с пылающей огненной булавой
    sh_lx, sh_ly = cx - 21 * d * s, cy + 22 * s + b
    el_lx, el_ly = cx - 28 * d * s, cy + 5 * s + b * 0.7
    hd_lx, hd_ly = cx - 25 * d * s, cy - 8 * s + b * 0.5

    arcade.draw_line(sh_lx, sh_ly, el_lx, el_ly, armor_dark, 8)
    arcade.draw_line(el_lx, el_ly, hd_lx, hd_ly, (88, 62, 46), 8)

    # Рукоять булавы и огненный шар с языками пламени
    mace_x = hd_lx - 18 * d * s
    mace_y = hd_ly - 12 * s
    arcade.draw_line(hd_lx + 4 * d * s, hd_ly + 3 * s, mace_x, mace_y, (92, 56, 36), 4.5)
    arcade.draw_circle_filled(hd_lx, hd_ly, 4.5 * s, armor_mid)

    # Многослойное живое пламя вокруг навершия булавы
    arcade.draw_circle_filled(mace_x, mace_y, 22 * s + flame_pulse, (235, 75, 25, 70))
    arcade.draw_circle_filled(mace_x, mace_y, 14 * s + flame_pulse * 0.6, (245, 115, 32, 210))
    arcade.draw_circle_filled(mace_x, mace_y, 8 * s, fire_core)

    # Огненные шипы-языки пламени
    for deg in (25, 85, 145, 205, 255, 315):
        rad = math.radians(deg + math.sin(t * 6.0) * 10)
        fx1 = mace_x + math.cos(rad) * 10 * s
        fy1 = mace_y + math.sin(rad) * 10 * s
        fx2 = mace_x + math.cos(rad) * (21 * s + flame_pulse)
        fy2 = mace_y + math.sin(rad) * (21 * s + flame_pulse)
        arcade.draw_line(fx1, fy1, fx2, fy2, fire_glow, 4)
        arcade.draw_line(fx1, fy1, fx2, fy2, fire_core, 1.5)


def _draw_bone_axe_guard(cx: float, cy: float, s: float, d: float, t: float, b: float):
    """Детализированный спрайт Элиты: Костяной Страж с Топором по референсу."""
    flesh = (176, 168, 156)
    flesh_light = (204, 196, 184)
    flesh_dark = (118, 110, 102)
    armor_dark = (46, 44, 46)
    armor_mid = (68, 65, 68)
    armor_edge = (104, 100, 104)
    necro_glow = (95, 225, 195)
    cloth_rag = (54, 52, 54)

    # 1. Широко расставленные мощные ноги в латных сапогах и открытые колени/бёдра
    for side, lx in ((-1, cx - 14 * d * s), (1, cx + 14 * d * s)):
        kx = lx + side * 3 * d * s
        ky = cy - 22 * s
        fx = lx + side * 4 * d * s
        fy = cy - 49 * s

        # Открытое бледное бедро со шрамами
        arcade.draw_line(lx, cy - 4 * s, kx, ky, flesh if side > 0 else flesh_dark, 11)
        arcade.draw_line(lx - 1 * d * s, cy - 10 * s, kx - 1 * d * s, ky - 2 * s, (98, 62, 62), 1.5)

        # Тяжёлые латные поножи, наколенники и сапоги
        arcade.draw_line(kx, ky, fx, fy, armor_mid if side > 0 else armor_dark, 12)
        arcade.draw_line(kx + 2 * d * s, ky, fx + 2 * d * s, fy, armor_edge, 2)
        arcade.draw_ellipse_filled(kx + 1 * d * s, ky + 1 * s, 13 * s, 11 * s, armor_mid)
        arcade.draw_ellipse_outline(kx + 1 * d * s, ky + 1 * s, 13 * s, 11 * s, armor_edge, 1.5)

        # Латный сапог
        boot = (
            (fx - 6 * s, cy - 52 * s),
            (fx + 10 * d * s, cy - 52 * s),
            (fx + 7 * d * s, cy - 44 * s),
            (fx - 5 * s, cy - 45 * s),
        )
        arcade.draw_polygon_filled(boot, armor_dark)
        arcade.draw_polygon_outline(boot, armor_edge, 1.3)

    # 2. Рваная тёмная юбка-туника и пояс с набедренными щитками
    rag_skirt = (
        (cx - 18 * d * s, cy - 2 * s),
        (cx + 18 * d * s, cy - 2 * s),
        (cx + 21 * d * s, cy - 26 * s),
        (cx + 9 * d * s, cy - 19 * s),
        (cx, cy - 28 * s),
        (cx - 9 * d * s, cy - 20 * s),
        (cx - 20 * d * s, cy - 25 * s),
    )
    arcade.draw_polygon_filled(rag_skirt, cloth_rag)
    arcade.draw_polygon_outline(rag_skirt, armor_dark, 1.5)

    # Пояс и боковые латные набедренники
    arcade.draw_rect_filled(arcade.XYWH(cx, cy + 1 * s + b * 0.4, 34 * s, 6 * s), armor_dark)
    arcade.draw_rect_outline(arcade.XYWH(cx, cy + 1 * s + b * 0.4, 34 * s, 6 * s), armor_edge, 1.2)
    for side in (-1, 1):
        tasset = (
            (cx + side * 8 * d * s, cy + 2 * s + b * 0.4),
            (cx + side * 21 * d * s, cy - 2 * s + b * 0.4),
            (cx + side * 23 * d * s, cy - 18 * s),
            (cx + side * 11 * d * s, cy - 15 * s),
        )
        arcade.draw_polygon_filled(tasset, armor_mid)
        arcade.draw_polygon_outline(tasset, armor_edge, 1.4)

    # 3. Мускулистый торс нежити с бирюзовыми трещинами и массивной тёмной кирасой
    abdomen = (
        (cx - 15 * d * s, cy + 2 * s),
        (cx - 18 * d * s, cy + 16 * s + b * 0.6),
        (cx + 18 * d * s, cy + 16 * s + b * 0.6),
        (cx + 15 * d * s, cy + 2 * s),
    )
    arcade.draw_polygon_filled(abdomen, flesh_dark)
    # Светящиеся некротические прожилки на животе и груди
    arcade.draw_line(cx + 5 * d * s, cy + 11 * s + b * 0.5, cx + 11 * d * s, cy + 7 * s + b * 0.4, necro_glow, 1.8)
    arcade.draw_line(cx - 2 * d * s, cy + 18 * s + b * 0.8, cx - 2 * d * s, cy + 25 * s + b, necro_glow, 1.8)

    # Массивная нагрудная кираса с вырезом и высоким воротником-горжетом
    chest_plate = (
        (cx - 18 * d * s, cy + 13 * s + b * 0.7),
        (cx - 23 * d * s, cy + 32 * s + b),
        (cx - 9 * d * s, cy + 37 * s + b),
        (cx + 9 * d * s, cy + 37 * s + b),
        (cx + 23 * d * s, cy + 32 * s + b),
        (cx + 18 * d * s, cy + 13 * s + b * 0.7),
        (cx, cy + 10 * s + b * 0.6),
    )
    arcade.draw_polygon_filled(chest_plate, armor_mid)
    arcade.draw_polygon_outline(chest_plate, armor_edge, 1.8)
    arcade.draw_line(cx, cy + 11 * s + b * 0.6, cx, cy + 29 * s + b, armor_dark, 2)

    # 4. Массивные шипастые наплечники
    for side in (-1, 1):
        px = cx + side * 23 * d * s
        py = cy + 30 * s + b
        pauldron = (
            (px - side * 6 * d * s, py + 7 * s),
            (px + side * 12 * d * s, py + 5 * s),
            (px + side * 15 * d * s, py - 8 * s),
            (px - side * 4 * d * s, py - 6 * s),
        )
        arcade.draw_polygon_filled(pauldron, armor_mid)
        arcade.draw_polygon_outline(pauldron, armor_edge, 1.6)
        # Короткие стальные шипы на наплечниках
        for sp_off, sp_y in ((6, 6), (11, 1)):
            tip = (px + side * (sp_off + 5) * d * s, py + (sp_y + 4) * s)
            arcade.draw_line(px + side * sp_off * d * s, py + sp_y * s, *tip, armor_edge, 2.5)

    # 5. Голова нежити: бледный череп, зубастый оскал и светящиеся бирюзовые глаза
    hx = cx + 1 * d * s
    hy = cy + 45 * s + b
    arcade.draw_rect_filled(arcade.XYWH(hx, hy - 7 * s, 11 * s, 7 * s), flesh_dark)
    arcade.draw_ellipse_filled(hx, hy + 2 * s, 19 * s, 21 * s, flesh_light)
    arcade.draw_ellipse_outline(hx, hy + 2 * s, 19 * s, 21 * s, flesh_dark, 1.5)

    # Тёмные глазницы и яркие бирюзово-зелёные глаза
    for ex in (-3.5, 4.5):
        arcade.draw_circle_filled(hx + ex * d * s, hy + 1 * s, 3.2 * s, (18, 22, 24))
        arcade.draw_circle_filled(hx + ex * d * s, hy + 1 * s, 2.0 * s, necro_glow)

    # Носовая впадина и оскал зубов
    arcade.draw_polygon_filled(((hx + 0.5 * d * s, hy - 1 * s), (hx - 1 * d * s, hy - 4 * s), (hx + 2 * d * s, hy - 4 * s)), (28, 24, 24))
    arcade.draw_line(hx - 4 * d * s, hy - 7 * s, hx + 5 * d * s, hy - 7 * s, (28, 22, 22), 2.5)
    for zx in (-3, -0.5, 2, 4):
        arcade.draw_line(hx + zx * d * s, hy - 6 * s, hx + zx * d * s, hy - 8.5 * s, flesh_light, 1.2)

    # 6. Могучие руки в длинных латных наручах
    # Задняя рука с боевым топором
    sh_bx, sh_by = cx - 22 * d * s, cy + 24 * s + b
    el_bx, el_by = cx - 30 * d * s, cy + 8 * s + b * 0.7
    hd_bx, hd_by = cx - 28 * d * s, cy - 6 * s + b * 0.5

    arcade.draw_line(sh_bx, sh_by, el_bx, el_by, flesh_dark, 8.5)
    arcade.draw_line(el_bx, el_by, hd_bx, hd_by, armor_mid, 9)
    arcade.draw_line(el_bx - 2 * d * s, el_by, hd_bx - 2 * d * s, hd_by, armor_edge, 2)
    arcade.draw_circle_filled(hd_bx, hd_by, 5 * s, flesh)

    # Массивный боевой топор (опущен вниз в задней руке, как на референсе)
    axe_top = (hd_bx + 8 * d * s, hd_by + 12 * s)
    axe_head_x = hd_bx - 16 * d * s
    axe_head_y = hd_by - 28 * s
    # Древко топора с кожаной обмоткой
    arcade.draw_line(*axe_top, axe_head_x - 6 * d * s, axe_head_y - 10 * s, (86, 62, 46), 5)
    for wrap in range(4):
        wy = hd_by - (4 + wrap * 5) * s
        wx = hd_bx - (2 + wrap * 3.5) * d * s
        arcade.draw_line(wx - 2 * s, wy + 1 * s, wx + 2 * s, wy - 1 * s, (42, 34, 30), 2)

    # Костяной обух и широкое изогнутое лезвие топора
    arcade.draw_ellipse_filled(axe_head_x, axe_head_y, 13 * s, 9 * s, flesh_light)
    arcade.draw_ellipse_outline(axe_head_x, axe_head_y, 13 * s, 9 * s, flesh_dark, 1.5)

    blade_poly = (
        (axe_head_x + 2 * d * s, axe_head_y + 4 * s),
        (axe_head_x + 15 * d * s, axe_head_y + 10 * s),
        (axe_head_x + 18 * d * s, axe_head_y - 6 * s),
        (axe_head_x + 10 * d * s, axe_head_y - 22 * s),
        (axe_head_x - 2 * d * s, axe_head_y - 4 * s),
    )
    arcade.draw_polygon_filled(blade_poly, armor_mid)
    arcade.draw_polygon_outline(blade_poly, armor_edge, 1.8)
    # Острая светлая кромка лезвия
    arcade.draw_line(axe_head_x + 15 * d * s, axe_head_y + 10 * s, axe_head_x + 18 * d * s, axe_head_y - 6 * s, (185, 190, 196), 2.2)
    arcade.draw_line(axe_head_x + 18 * d * s, axe_head_y - 6 * s, axe_head_x + 10 * d * s, axe_head_y - 22 * s, (185, 190, 196), 2.2)

    # Передняя рука в латном наруче с когтистой кистью
    sh_fx, sh_fy = cx + 22 * d * s, cy + 24 * s + b
    el_fx, el_fy = cx + 29 * d * s, cy + 8 * s + b * 0.7
    hd_fx, hd_fy = cx + 26 * d * s, cy - 7 * s + b * 0.5

    arcade.draw_line(sh_fx, sh_fy, el_fx, el_fy, flesh, 8.5)
    arcade.draw_line(el_fx, el_fy, hd_fx, hd_fy, armor_mid, 9.5)
    arcade.draw_line(el_fx + 2 * d * s, el_fy, hd_fx + 2 * d * s, hd_fy, armor_edge, 2)
    arcade.draw_circle_filled(hd_fx, hd_fy, 5 * s, flesh_light)
    for finger in (-2, 0, 2):
        arcade.draw_line(hd_fx + finger * s, hd_fy - 3 * s, hd_fx + (finger * 1.3) * s, hd_fy - 9 * s, flesh_dark, 1.8)

def _draw_mummy(cx: float, cy: float, s: float, d: float, t: float, b: float):
    """Детализированный спрайт Древней Мумии по референсу (бинты, лохмотья, царская пектораль)."""
    sway = math.sin(t * 2.2) * 3.0 * s
    shamble = math.sin(t * 2.6) * 2.0 * s

    wrap_light = (196, 186, 152)
    wrap_mid = (154, 144, 114)
    wrap_dark = (88, 82, 66)
    skin_dead = (56, 52, 48)
    gold = (198, 166, 84)
    gold_dark = (122, 98, 44)
    scarab_teal = (62, 168, 162)

    # 1. Задняя нога в тёмных теневых бинтах и передняя мощная забинтованная нога
    # Задняя нога
    bh_x, bh_y = cx - 10 * d * s, cy - 8 * s
    bk_x, bk_y = cx - 22 * d * s, cy - 26 * s
    bf_x, bf_y = cx - 24 * d * s, cy - 49 * s
    arcade.draw_line(bh_x, bh_y, bk_x, bk_y, wrap_dark, 11)
    arcade.draw_line(bk_x, bk_y, bf_x, bf_y, skin_dead, 9)
    for wy in (-14, -22, -32, -41):
        arcade.draw_line(bk_x - 5 * s, cy + wy * s, bk_x + 5 * s, cy + (wy - 3) * s, wrap_mid, 2.2)
    arcade.draw_ellipse_filled(bf_x - 3 * d * s, bf_y - 2 * s, 14 * s, 7 * s, wrap_dark)

    # Передняя опорная нога (широко забинтованная, с массивной стопой как на арте)
    fh_x, fh_y = cx + 6 * d * s, cy - 8 * s
    fk_x, fk_y = cx + 8 * d * s, cy - 27 * s
    ff_x, ff_y = cx + 15 * d * s, cy - 49 * s
    arcade.draw_line(fh_x, fh_y, fk_x, fk_y, wrap_mid, 13)
    arcade.draw_line(fk_x, fk_y, ff_x, ff_y, wrap_light, 12)
    arcade.draw_line(fh_x, fh_y, fk_x, fk_y, wrap_dark, 1.5)

    # Перекрещивающиеся полосы бинтов на передней ноге
    for idx, wy in enumerate((-12, -18, -24, -30, -36, -42)):
        lx = fk_x + (idx * 1.1) * d * s
        ly = cy + wy * s
        dir_flip = 1 if idx % 2 == 0 else -1
        arcade.draw_line(lx - 7 * s, ly + 2 * dir_flip * s, lx + 7 * s, ly - 2 * dir_flip * s, wrap_dark, 2)
        arcade.draw_line(lx - 6 * s, ly + 1 * dir_flip * s, lx + 6 * s, ly - 1 * dir_flip * s, wrap_light, 1.5)

    # Массивная забинтованная ступня
    foot_poly = (
        (ff_x - 7 * s, cy - 52 * s),
        (ff_x + 14 * d * s, cy - 52 * s),
        (ff_x + 11 * d * s, cy - 42 * s),
        (ff_x - 6 * s, cy - 43 * s),
    )
    arcade.draw_polygon_filled(foot_poly, wrap_light)
    arcade.draw_polygon_outline(foot_poly, wrap_dark, 1.8)
    arcade.draw_line(ff_x - 3 * s, cy - 46 * s, ff_x + 9 * d * s, cy - 50 * s, wrap_dark, 2)

    # 2. Сгорбленный торс мумии и многослойные бинты
    torso = (
        (cx - 18 * d * s, cy - 10 * s),
        (cx - 22 * d * s, cy + 22 * s + b),
        (cx + 18 * d * s, cy + 28 * s + b),
        (cx + 16 * d * s, cy - 8 * s),
    )
    arcade.draw_polygon_filled(torso, wrap_mid)
    arcade.draw_polygon_outline(torso, wrap_dark, 1.8)

    # Горизонтальные и диагональные витки бинтов на торсе
    for idx, ty in enumerate((-2, 5, 12, 19)):
        y_pos = cy + ty * s + b * 0.7
        arcade.draw_line(cx - 18 * d * s, y_pos - 2 * s, cx + 17 * d * s, y_pos + 2 * s, wrap_light, 3.5)
        arcade.draw_line(cx - 18 * d * s, y_pos - 3.5 * s, cx + 17 * d * s, y_pos + 0.5 * s, wrap_dark, 1.5)

    # 3. Царская египетская пектораль (нагрудное украшение с синим амулетом)
    pec_x = cx + 9 * d * s
    pec_y = cy + 16 * s + b * 0.85
    # Ожерелье-воротник
    arcade.draw_arc_outline(pec_x, pec_y + 11 * s, 26 * s, 14 * s, gold, 185, 355, 4)
    arcade.draw_arc_outline(pec_x, pec_y + 11 * s, 26 * s, 14 * s, scarab_teal, 200, 340, 1.8)
    # Амулет-скарабей в центре
    arcade.draw_circle_filled(pec_x, pec_y + 5 * s, 4 * s, scarab_teal)
    arcade.draw_circle_outline(pec_x, pec_y + 5 * s, 4 * s, gold, 1.5)
    # Прямоугольная золотая пластина пекторали
    arcade.draw_rect_filled(arcade.XYWH(pec_x, pec_y - 3 * s, 19 * s, 11 * s), gold_dark)
    arcade.draw_rect_outline(arcade.XYWH(pec_x, pec_y - 3 * s, 19 * s, 11 * s), gold, 1.8)
    arcade.draw_circle_filled(pec_x, pec_y - 3 * s, 2.5 * s, gold)

    # 4. Свисающие длинные лохмотья истлевших бинтов
    rag1 = (
        (cx + 16 * d * s, cy + 20 * s + b),
        (cx + 25 * d * s + sway, cy - 12 * s),
        (cx + 21 * d * s + sway, cy - 28 * s),
        (cx + 15 * d * s, cy - 6 * s),
    )
    rag2 = (
        (cx - 2 * d * s, cy - 6 * s),
        (cx - 8 * d * s - sway * 0.7, cy - 30 * s),
        (cx - 2 * d * s - sway * 0.7, cy - 24 * s),
        (cx + 3 * d * s, cy - 8 * s),
    )
    arcade.draw_polygon_filled(rag1, wrap_light)
    arcade.draw_polygon_outline(rag1, wrap_dark, 1.2)
    arcade.draw_polygon_filled(rag2, wrap_mid)
    arcade.draw_polygon_outline(rag2, wrap_dark, 1.2)

    # 5. Сгорбленная голова в плотных бинтах со щелью для глаза и оскалом
    hx = cx + 14 * d * s
    hy = cy + 34 * s + b + shamble * 0.4
    arcade.draw_ellipse_filled(hx, hy, 21 * s, 24 * s, skin_dead)
    arcade.draw_ellipse_outline(hx, hy, 21 * s, 24 * s, wrap_dark, 1.5)

    # Витки бинтов на голове (оставляют узкую тёмную прорезь для левого глаза и рот)
    arcade.draw_line(hx - 9 * d * s, hy + 8 * s, hx + 9 * d * s, hy + 6 * s, wrap_light, 4.5)
    arcade.draw_line(hx - 9 * d * s, hy + 3 * s, hx + 8 * d * s, hy + 9 * s, wrap_mid, 3.5)
    arcade.draw_line(hx - 8 * d * s, hy - 2 * s, hx + 9 * d * s, hy + 1 * s, wrap_light, 4)
    arcade.draw_line(hx - 7 * d * s, hy - 8 * s, hx + 7 * d * s, hy - 9 * s, wrap_mid, 3.5)

    # Прищуренный глаз сквозь бинты и оскал зубов
    arcade.draw_circle_filled(hx + 4 * d * s, hy + 3 * s, 2.2 * s, (235, 225, 195))
    arcade.draw_circle_filled(hx + 4.5 * d * s, hy + 3 * s, 1.0 * s, (20, 18, 18))
    arcade.draw_line(hx, hy - 5 * s, hx + 8 * d * s, hy - 5 * s, (212, 204, 178), 2)

    # 6. Забинтованные когтистые руки (передняя вытянута вперёд, задняя опущена)
    # Задняя рука
    sh_bx, sh_by = cx - 18 * d * s, cy + 20 * s + b
    el_bx, el_by = cx - 26 * d * s, cy + 3 * s + b * 0.7
    hd_bx, hd_by = cx - 22 * d * s, cy - 14 * s + b * 0.5
    arcade.draw_line(sh_bx, sh_by, el_bx, el_by, wrap_mid, 8)
    arcade.draw_line(el_bx, el_by, hd_bx, hd_by, wrap_light, 7.5)
    for wy in (14, 6, -2, -9):
        arcade.draw_line(el_bx - 4 * s, cy + wy * s, el_bx + 4 * s, cy + (wy - 2) * s, wrap_dark, 1.6)
    arcade.draw_circle_filled(hd_bx, hd_by, 4.5 * s, skin_dead)
    for claw in (-2, 0, 2):
        arcade.draw_line(hd_bx + claw * s, hd_by - 3 * s, hd_bx + (claw + 2) * d * s, hd_by - 8 * s, wrap_dark, 1.6)

    # Передняя вытянутая когтистая рука
    sh_fx, sh_fy = cx + 15 * d * s, cy + 22 * s + b
    el_fx, el_fy = cx + 22 * d * s, cy + 6 * s + b * 0.7
    hd_fx, hd_fy = cx + 11 * d * s, cy - 2 * s + b * 0.5
    arcade.draw_line(sh_fx, sh_fy, el_fx, el_fy, wrap_light, 8.5)
    arcade.draw_line(el_fx, el_fy, hd_fx, hd_fy, wrap_mid, 8)
    for wx in (13, 17, 21):
        arcade.draw_line(cx + wx * d * s, cy + 2 * s, cx + (wx - 2) * d * s, cy - 4 * s, wrap_dark, 1.6)
    arcade.draw_circle_filled(hd_fx, hd_fy, 4.8 * s, skin_dead)
    for claw_y in (-2, 1, 4):
        arcade.draw_line(hd_fx, hd_fy + claw_y * s, hd_fx + 7 * d * s, hd_fy + (claw_y - 2) * s, wrap_dark, 1.8)

def _draw_skeleton_giant(cx: float, cy: float, s: float, d: float, t: float, b: float):
    """Детализированный спрайт Колоссального Скелета-Гиганта по референсу."""
    sway = math.sin(t * 1.8) * 2.5 * s
    mist_shift = math.sin(t * 2.2) * 4.0 * s

    bone_dark = (88, 76, 74)
    bone_mid = (132, 116, 110)
    bone_light = (176, 158, 148)
    bone_highlight = (212, 196, 182)
    socket_dark = (26, 20, 22)

    # 1. Массивные кости ног и тазовый пояс (уходящие в дымку у основания)
    for side, lx in ((-1, cx - 16 * d * s), (1, cx + 16 * d * s)):
        col = bone_mid if side > 0 else bone_dark
        arcade.draw_line(lx, cy - 8 * s, lx + side * 4 * d * s, cy - 48 * s, col, 11)
        arcade.draw_line(lx + side * 4 * d * s, cy - 8 * s, lx + side * 8 * d * s, cy - 48 * s, bone_dark, 5)

    # Массивная тазовая кость с анатомическими отверстиями
    pelvis = (
        (cx - 24 * d * s, cy - 2 * s),
        (cx + 24 * d * s, cy - 2 * s),
        (cx + 18 * d * s, cy - 18 * s),
        (cx - 18 * d * s, cy - 18 * s),
    )
    arcade.draw_polygon_filled(pelvis, bone_mid)
    arcade.draw_polygon_outline(pelvis, bone_dark, 2)
    arcade.draw_ellipse_filled(cx - 9 * d * s, cy - 9 * s, 9 * s, 7 * s, socket_dark)
    arcade.draw_ellipse_filled(cx + 9 * d * s, cy - 9 * s, 9 * s, 7 * s, socket_dark)

    # Клубы тумана/пыли у ног гиганта (как на концепт-арте)
    for mx, my, mw, mh in (
        (-22 + mist_shift * 0.3, -44, 48, 16),
        (18 - mist_shift * 0.3, -46, 52, 18),
        (0, -49, 76, 14),
    ):
        arcade.draw_ellipse_filled(cx + mx * s, cy + my * s, mw * s, mh * s, (215, 208, 198, 120))

    # 2. Толстый сегментированный позвоночник
    arcade.draw_line(cx, cy - 4 * s, cx, cy + 44 * s + b, bone_dark, 9)
    for vy in range(-2, 42, 6):
        arcade.draw_rect_filled(arcade.XYWH(cx, cy + vy * s + b * 0.6, 11 * s, 3.5 * s), bone_light)

    # 3. Огромная бочкообразная грудная клетка с мощными рёбрами и грудиной
    # Тёмная полость внутри грудной клетки
    arcade.draw_ellipse_filled(cx, cy + 20 * s + b, 46 * s, 36 * s, (46, 38, 40, 210))

    for idx, ry in enumerate((7, 13, 19, 25, 31)):
        rw = (18 + idx * 1.6) * s
        arcade.draw_arc_outline(cx, cy + ry * s + b, rw * 2.2, 11 * s, bone_light, 185, 355, 3.5)
        arcade.draw_arc_outline(cx, cy + (ry - 1) * s + b, rw * 2.2, 11 * s, bone_dark, 190, 350, 1.5)

    # Центральная грудина и поры на костях
    arcade.draw_rect_filled(arcade.XYWH(cx + 2 * d * s, cy + 23 * s + b, 7 * s, 22 * s), bone_highlight)
    arcade.draw_rect_outline(arcade.XYWH(cx + 2 * d * s, cy + 23 * s + b, 7 * s, 22 * s), bone_dark, 1.5)

    # 4. Широкие шипастые костяные плечи (наплечные гребни)
    for side in (-1, 1):
        px = cx + side * 27 * d * s
        py = cy + 33 * s + b
        crest = (
            (cx + side * 10 * d * s, py + 5 * s),
            (px + side * 12 * d * s, py + 4 * s),
            (px + side * 15 * d * s, py - 8 * s),
            (cx + side * 14 * d * s, py - 7 * s),
        )
        arcade.draw_polygon_filled(crest, bone_mid if side > 0 else bone_dark)
        arcade.draw_polygon_outline(crest, bone_highlight if side > 0 else bone_mid, 1.5)

        # Костяные шипы вдоль верхнего гребня плеч
        for sp_x, sp_y, tip_dx, tip_dy in (
            (14, 4, 12, 12),
            (22, 4, 24, 15),
            (30, 3, 36, 13),
            (36, 0, 44, 6),
        ):
            spike = (
                (cx + side * (sp_x - 2) * d * s, py + sp_y * s),
                (cx + side * (sp_x + 2) * d * s, py + sp_y * s),
                (cx + side * tip_dx * d * s, py + tip_dy * s),
            )
            arcade.draw_polygon_filled(spike, bone_light)

    # 5. Массивный череп титана на мощной шее
    hx = cx - 2 * d * s
    hy = cy + 51 * s + b
    # Толстая шейная опора
    arcade.draw_rect_filled(arcade.XYWH(hx + 1 * d * s, hy - 8 * s, 12 * s, 9 * s), bone_dark)
    # Нижняя челюсть
    arcade.draw_rect_filled(arcade.XYWH(hx + 2 * d * s, hy - 8 * s, 11 * s, 7 * s), bone_mid)
    # Черепная коробка
    arcade.draw_circle_filled(hx, hy + 2 * s, 11 * s, bone_highlight)
    arcade.draw_circle_outline(hx, hy + 2 * s, 11 * s, bone_dark, 1.8)

    # Глубокие тёмные глазницы и носовая впадина
    arcade.draw_circle_filled(hx - 1 * d * s, hy + 2 * s, 2.8 * s, socket_dark)
    arcade.draw_circle_filled(hx + 5.5 * d * s, hy + 2 * s, 2.5 * s, socket_dark)
    arcade.draw_polygon_filled(((hx + 2.5 * d * s, hy), (hx + 1.5 * d * s, hy - 3 * s), (hx + 3.5 * d * s, hy - 3 * s)), socket_dark)
    for zx in (-2, 0.5, 3, 5):
        arcade.draw_line(hx + zx * d * s, hy - 5 * s, hx + zx * d * s, hy - 8.5 * s, socket_dark, 1.2)

    # 6. Огромные длинные костистые руки с двойными костями предплечья и свисающими нитями
    for side, col_arm in ((-1, bone_dark), (1, bone_light)):
        sh_x = cx + side * 32 * d * s
        sh_y = cy + 28 * s + b
        el_x = cx + side * 38 * d * s
        el_y = cy + 1 * s + b * 0.6
        hd_x = cx + side * 36 * d * s
        hd_y = cy - 32 * s + b * 0.3

        # Плечевая кость
        arcade.draw_line(sh_x, sh_y, el_x, el_y, col_arm, 8)
        arcade.draw_circle_filled(el_x, el_y, 5.5 * s, bone_mid)

        # Двойные кости предплечья (лучевая и локтевая, с зазором между ними как на арте)
        arcade.draw_line(el_x - 2 * s, el_y, hd_x - 2 * s, hd_y, col_arm, 4)
        arcade.draw_line(el_x + 2.5 * s, el_y, hd_x + 2.5 * s, hd_y, bone_mid, 3.5)

        # Свисающие нити истлевших сухожилий с рук
        for thread_off in (-3, 4):
            tx = el_x + thread_off * s
            arcade.draw_line(tx, el_y - 2 * s, tx + sway * 0.6, el_y - 22 * s, (72, 62, 60, 185), 1.2)

        # Огромная когтистая кисть гиганта
        arcade.draw_ellipse_filled(hd_x, hd_y - 3 * s, 9 * s, 11 * s, bone_mid)
        for finger in (-3, 0, 3):
            arcade.draw_line(
                hd_x + finger * s,
                hd_y - 7 * s,
                hd_x + (finger * 1.4) * s,
                hd_y - 16 * s,
                col_arm,
                2.5,
            )

def _draw_plague_zombie(cx: float, cy: float, s: float, d: float, t: float, b: float):
    """Детализированный спрайт Чумного Зомби по референсу (мозг, вывалившийся глаз, рваная футболка)."""
    shamble = math.sin(t * 3.0) * 2.5 * s
    eye_swing = math.sin(t * 4.5) * 2.2 * s

    skin = (126, 168, 162)
    skin_light = (154, 194, 188)
    skin_dark = (84, 118, 114)
    shirt = (224, 214, 192)
    shirt_shadow = (182, 172, 152)
    pants = (82, 52, 42)
    pants_dark = (54, 34, 28)
    blood = (168, 32, 34)
    brain_pink = (218, 118, 134)
    brain_dark = (156, 72, 88)
    outline = (24, 26, 28)

    # 1. Косолапые ноги в коричневых штанах с заплатками и босые ступни
    # Задняя нога (отставлена назад)
    bh_x, bh_y = cx - 10 * d * s, cy - 6 * s
    bk_x, bk_y = cx - 4 * d * s, cy - 26 * s
    bf_x, bf_y = cx - 18 * d * s, cy - 48 * s
    arcade.draw_line(bh_x, bh_y, bk_x, bk_y, pants_dark, 9.5)
    arcade.draw_line(bk_x, bk_y, bf_x, bf_y, pants, 9.5)
    arcade.draw_line(bh_x, bh_y, bk_x, bk_y, outline, 1.5)
    # Босая ступня задней ноги с пальцами
    arcade.draw_ellipse_filled(bf_x + 4 * d * s, cy - 50 * s, 16 * s, 6.5 * s, skin)
    arcade.draw_ellipse_outline(bf_x + 4 * d * s, cy - 50 * s, 16 * s, 6.5 * s, outline, 1.4)

    # Передняя нога (колено сведено внутрь, как на референсе)
    fh_x, fh_y = cx + 4 * d * s, cy - 6 * s
    fk_x, fk_y = cx + 1 * d * s, cy - 25 * s
    ff_x, ff_y = cx + 15 * d * s, cy - 48 * s
    arcade.draw_line(fh_x, fh_y, fk_x, fk_y, pants, 10)
    arcade.draw_line(fk_x, fk_y, ff_x, ff_y, pants_dark, 10)
    # Синяя заплатка на штанине
    arcade.draw_rect_filled(arcade.XYWH(fk_x + 5 * d * s, cy - 34 * s, 5.5 * s, 6.5 * s), (72, 96, 114))
    arcade.draw_rect_outline(arcade.XYWH(fk_x + 5 * d * s, cy - 34 * s, 5.5 * s, 6.5 * s), outline, 1)

    # Босая ступня передней ноги с раной и пальцами
    arcade.draw_ellipse_filled(ff_x + 5 * d * s, cy - 50 * s, 18 * s, 7 * s, skin_light)
    arcade.draw_ellipse_outline(ff_x + 5 * d * s, cy - 50 * s, 18 * s, 7 * s, outline, 1.5)
    arcade.draw_circle_filled(ff_x + 2 * d * s, cy - 48 * s, 2.5 * s, blood)

    # 2. Дальняя рука (вытянута далеко вперёд в сторону игрока)
    sh_fx, sh_fy = cx + 12 * d * s, cy + 16 * s + b
    el_fx, el_fy = cx + 26 * d * s, cy + 2 * s + b * 0.7
    hd_fx, hd_fy = cx + 38 * d * s, cy - 8 * s + b * 0.5

    arcade.draw_line(sh_fx, sh_fy, el_fx, el_fy, skin_dark, 6.5)
    arcade.draw_line(el_fx, el_fy, hd_fx, hd_fy, skin, 6)
    # Рваный рукав футболки на дальнем плече
    arcade.draw_line(sh_fx, sh_fy, sh_fx + 9 * d * s, sh_fy - 8 * s, shirt_shadow, 11)
    # Когтистая растопыренная кисть
    arcade.draw_circle_filled(hd_fx, hd_fy, 4.5 * s, skin)
    for fx_off, fy_off in ((7, 2), (8, -2), (6, -6), (2, -7)):
        arcade.draw_line(hd_fx, hd_fy, hd_fx + fx_off * d * s, hd_fy + fy_off * s, skin_light, 2)

    # 3. Сгорбленный торс в грязно-бежевой рваной футболке с кровавым пятном
    torso = (
        (cx - 13 * d * s, cy - 7 * s),
        (cx - 16 * d * s, cy + 22 * s + b),
        (cx + 15 * d * s, cy + 24 * s + b),
        (cx + 12 * d * s, cy - 5 * s),
    )
    arcade.draw_polygon_filled(torso, shirt)
    arcade.draw_polygon_outline(torso, outline, 1.8)
    # Складки и заплатка на футболке
    arcade.draw_line(cx - 11 * d * s, cy + 1 * s, cx + 10 * d * s, cy + 3 * s, shirt_shadow, 2)
    arcade.draw_rect_filled(arcade.XYWH(cx + 7 * d * s, cy + 8 * s + b * 0.5, 5 * s, 5 * s), (135, 165, 168))

    # Алое кровавое пятно у ворота на груди
    blood_stain = (
        (cx + 3 * d * s, cy + 23 * s + b),
        (cx + 13 * d * s, cy + 22 * s + b),
        (cx + 14 * d * s, cy + 12 * s + b),
        (cx + 7 * d * s, cy + 9 * s + b),
        (cx + 2 * d * s, cy + 15 * s + b),
    )
    arcade.draw_polygon_filled(blood_stain, blood)

    # 4. Ближняя рука с рваным рукавом и кровавой раной на предплечье
    sh_bx, sh_by = cx - 10 * d * s, cy + 16 * s + b
    el_bx, el_by = cx - 22 * d * s, cy + 2 * s + b * 0.7
    hd_bx, hd_by = cx - 6 * d * s, cy - 11 * s + b * 0.5

    arcade.draw_line(sh_bx, sh_by, el_bx, el_by, skin, 7)
    arcade.draw_line(el_bx, el_by, hd_bx, hd_by, skin_light, 6.5)
    arcade.draw_line(sh_bx, sh_by, sh_bx - 9 * d * s, sh_by - 10 * s, shirt, 12)
    arcade.draw_line(sh_bx, sh_by, sh_bx - 9 * d * s, sh_by - 10 * s, outline, 1.5)

    # Кровавая рана на предплечье и растопыренные пальцы
    arcade.draw_ellipse_filled(el_bx + 7 * d * s, el_by - 5 * s, 8 * s, 4 * s, blood)
    arcade.draw_circle_filled(hd_bx, hd_by, 4.8 * s, skin_light)
    for fx_off, fy_off in ((-4, -5), (0, -7), (4, -6), (7, -3)):
        arcade.draw_line(hd_bx, hd_by, hd_bx + fx_off * d * s, hd_by + fy_off * s, skin, 2.2)

    # 5. Большая голова с открытым розовым мозгом, зубастым оскалом и вывалившимся глазом
    hx = cx + 11 * d * s
    hy = cy + 34 * s + b + shamble * 0.4

    # Нижняя челюсть и скулы
    arcade.draw_ellipse_filled(hx + 3 * d * s, hy - 8 * s, 19 * s, 14 * s, skin)
    arcade.draw_ellipse_outline(hx + 3 * d * s, hy - 8 * s, 19 * s, 14 * s, outline, 1.6)
    # Черепная коробка
    arcade.draw_ellipse_filled(hx, hy + 4 * s, 25 * s, 24 * s, skin_light)
    arcade.draw_ellipse_outline(hx, hy + 4 * s, 25 * s, 24 * s, outline, 1.8)

    # Открытый розовый мозг в верхней части черепа (как на референсе)
    brain_x = hx - 2 * d * s
    brain_y = hy + 13 * s
    arcade.draw_ellipse_filled(brain_x, brain_y, 17 * s, 10 * s, brain_pink)
    arcade.draw_ellipse_outline(brain_x, brain_y, 17 * s, 10 * s, outline, 1.5)
    arcade.draw_arc_outline(brain_x - 3 * d * s, brain_y, 7 * s, 5 * s, brain_dark, 20, 200, 1.8)
    arcade.draw_arc_outline(brain_x + 3 * d * s, brain_y + 1 * s, 7 * s, 5 * s, brain_dark, 180, 350, 1.8)

    # Широкий зубастый оскал с деснами
    arcade.draw_ellipse_filled(hx + 4 * d * s, hy - 8 * s, 14 * s, 7 * s, brain_dark)
    arcade.draw_line(hx - 2 * d * s, hy - 7 * s, hx + 10 * d * s, hy - 7 * s, (242, 238, 215), 2.5)
    arcade.draw_line(hx - 1 * d * s, hy - 10 * s, hx + 9 * d * s, hy - 10 * s, (242, 238, 215), 2.2)

    # Большой белый глаз (ближний)
    arcade.draw_circle_filled(hx + 1 * d * s, hy + 2 * s, 4.8 * s, (245, 242, 224))
    arcade.draw_circle_outline(hx + 1 * d * s, hy + 2 * s, 4.8 * s, outline, 1.5)

    # Пустая тёмная вторая глазница и свисающий на розовом нерве глаз (фирменная деталь!)
    socket_x = hx + 9 * d * s
    socket_y = hy + 2 * s
    arcade.draw_ellipse_filled(socket_x, socket_y, 6 * s, 8 * s, (16, 18, 20))

    dangling_x = socket_x + 2 * d * s + eye_swing
    dangling_y = socket_y - 12 * s
    # Розовый зрительный нерв
    arcade.draw_line(socket_x, socket_y - 1 * s, dangling_x, dangling_y + 2 * s, brain_pink, 2.5)
    arcade.draw_line(socket_x + 1 * d * s, socket_y - 2 * s, dangling_x + 1 * d * s, dangling_y + 2 * s, blood, 1.2)
    # Свисающее глазное яблоко
    arcade.draw_circle_filled(dangling_x, dangling_y, 4.2 * s, (245, 242, 224))
    arcade.draw_circle_outline(dangling_x, dangling_y, 4.2 * s, outline, 1.5)

def _draw_necromancer(cx: float, cy: float, s: float, d: float, t: float, b: float):
    """Детализированный спрайт Некроманта по референсу (коса с алыми рунами, парящий гримуар, капюшон)."""
    sway = math.sin(t * 2.1) * 3.0 * s
    book_float = math.sin(t * 3.2) * 3.5 * s
    rune_pulse = 0.75 + 0.25 * math.sin(t * 4.5)

    robe_black = (18, 17, 22)
    robe_dark = (34, 32, 40)
    shawl_grey = (82, 80, 88)
    shawl_light = (122, 118, 128)
    skin_corpse = (118, 134, 146)
    crimson = (225, 48, 52)
    scythe_steel = (64, 68, 76)
    scythe_edge = (182, 192, 204)
    magic_blue = (145, 205, 255)

    # 1. Мрачная пурпурная аура за спиной и клубы тумана у подола
    arcade.draw_ellipse_filled(cx, cy + 12 * s + b, 72 * s, 96 * s, (92, 38, 86, 45))
    for mx, my, mw, mh in ((-18, -48, 46, 14), (16, -50, 44, 13), (0, -52, 68, 12)):
        arcade.draw_ellipse_filled(cx + mx * s, cy + my * s, mw * s, mh * s, (16, 15, 20, 210))

    # 2. Длинная рваная мантия с развевающимся подолом
    robe_pts = (
        (cx - 17 * d * s, cy + 28 * s + b),
        (cx + 17 * d * s, cy + 28 * s + b),
        (cx + 32 * d * s + sway, cy - 50 * s),
        (cx + 15 * d * s, cy - 44 * s),
        (cx + 2 * d * s - sway * 0.5, cy - 53 * s),
        (cx - 14 * d * s, cy - 45 * s),
        (cx - 29 * d * s + sway * 0.8, cy - 51 * s),
    )
    arcade.draw_polygon_filled(robe_pts, robe_black)
    arcade.draw_polygon_outline(robe_pts, robe_dark, 1.5)

    # Складки мантии и кожаный пояс с пряжкой
    arcade.draw_line(cx - 4 * d * s, cy + 4 * s, cx - 12 * d * s + sway * 0.5, cy - 46 * s, robe_dark, 2.5)
    arcade.draw_line(cx + 6 * d * s, cy + 4 * s, cx + 14 * d * s + sway * 0.5, cy - 46 * s, robe_dark, 2.5)
    arcade.draw_line(cx - 14 * d * s, cy + 5 * s + b * 0.5, cx + 14 * d * s, cy + 4 * s + b * 0.5, (48, 36, 32), 4.5)
    arcade.draw_circle_outline(cx + 3 * d * s, cy + 4.5 * s + b * 0.5, 3.5 * s, (135, 118, 92), 1.5)

    # Пепельно-серая рваная накидка на плечах и груди
    shawl = (
        (cx - 20 * d * s, cy + 32 * s + b),
        (cx + 20 * d * s, cy + 32 * s + b),
        (cx + 24 * d * s + sway * 0.4, cy + 6 * s + b),
        (cx + 12 * d * s, cy + 14 * s + b),
        (cx + 3 * d * s, cy + 2 * s + b),
        (cx - 8 * d * s, cy + 16 * s + b),
        (cx - 22 * d * s + sway * 0.4, cy + 8 * s + b),
    )
    arcade.draw_polygon_filled(shawl, shawl_grey)
    arcade.draw_polygon_outline(shawl, shawl_light, 1.2)

    # 3. Глубокий капюшон и иссушенное лицо с горящими багровыми глазами
    hx = cx + 1 * d * s
    hy = cy + 40 * s + b
    hood = (
        (hx - 14 * d * s, hy - 8 * s),
        (hx - 12 * d * s, hy + 11 * s),
        (hx, hy + 17 * s),
        (hx + 12 * d * s, hy + 11 * s),
        (hx + 14 * d * s, hy - 8 * s),
    )
    arcade.draw_polygon_filled(hood, robe_black)
    arcade.draw_polygon_outline(hood, shawl_grey, 1.5)

    # Бледно-синюшное лицо в тени капюшона
    arcade.draw_ellipse_filled(hx + 1 * d * s, hy, 13 * s, 16 * s, skin_corpse)
    arcade.draw_line(hx - 2 * d * s, hy - 4 * s, hx + 4 * d * s, hy - 4 * s, (38, 42, 48), 1.5)
    # Светящиеся красные глаза
    arcade.draw_circle_filled(hx - 1.5 * d * s, hy + 2 * s, 1.8 * s, crimson)
    arcade.draw_circle_filled(hx + 4 * d * s, hy + 2 * s, 1.8 * s, crimson)

    # 4. Передняя рука с когтистыми пальцами и парящий призрачный гримуар с молниями
    sh_fx, sh_fy = cx + 16 * d * s, cy + 24 * s + b
    el_fx, el_fy = cx + 23 * d * s, cy + 10 * s + b * 0.7
    hd_fx, hd_fy = cx + 21 * d * s, cy - 3 * s + b * 0.5
    arcade.draw_line(sh_fx, sh_fy, el_fx, el_fy, robe_dark, 6.5)
    arcade.draw_line(el_fx, el_fy, hd_fx, hd_fy, skin_corpse, 4.5)
    for finger in (-2, 0, 2):
        arcade.draw_line(hd_fx, hd_fy, hd_fx + (3 + finger) * d * s, hd_fy - 6 * s, skin_corpse, 1.5)

    # Парящий раскрытый гримуар перед некромантом
    bx = cx + 38 * d * s
    by = cy + 16 * s + book_float
    arcade.draw_circle_filled(bx, by, 18 * s, (110, 175, 255, 55))

    # Обложка и веер светящихся страниц
    cover = (
        (bx - 8 * d * s, by - 9 * s),
        (bx + 7 * d * s, by - 11 * s),
        (bx + 9 * d * s, by + 5 * s),
        (bx - 6 * d * s, by + 7 * s),
    )
    arcade.draw_polygon_filled(cover, (68, 96, 138, 210))
    arcade.draw_polygon_outline(cover, (215, 238, 255), 1.5)
    for pg in range(4):
        off = pg * 2.2 * s
        arcade.draw_line(
            bx - 5 * d * s + off * 0.3,
            by + 6 * s + off * 0.4,
            bx + 8 * d * s + off * 0.4,
            by + 5 * s + off * 0.7,
            (235, 246, 255),
            1.6,
        )

    # Разряды сине-белой молнии от книги вниз
    bolt1 = (
        (bx + 6 * d * s, by - 8 * s),
        (bx + 14 * d * s, by - 22 * s),
        (bx + 8 * d * s, by - 36 * s),
        (bx + 17 * d * s, by - 54 * s),
    )
    arcade.draw_line_strip(bolt1, magic_blue, 1.5)

    # 5. Задняя рука и огромная коса Смерти, упирающаяся в череп на земле
    staff_x = cx - 26 * d * s
    sh_bx, sh_by = cx - 16 * d * s, cy + 25 * s + b
    el_bx, el_by = cx - 22 * d * s, cy + 14 * s + b * 0.8
    hd_bx, hd_by = staff_x, cy + 22 * s + b * 0.8

    arcade.draw_line(sh_bx, sh_by, el_bx, el_by, robe_dark, 6.5)
    arcade.draw_line(el_bx, el_by, hd_bx, hd_by, skin_corpse, 4.5)

    # Череп на земле у основания древка косы
    skull_y = cy - 47 * s
    arcade.draw_circle_filled(staff_x, skull_y, 6.5 * s, (165, 155, 148))
    arcade.draw_circle_filled(staff_x - 2 * s, skull_y, 1.8 * s, crimson)
    arcade.draw_circle_filled(staff_x + 2 * s, skull_y, 1.8 * s, crimson)

    # Длинное узловатое древко косы
    top_y = cy + 56 * s + b
    arcade.draw_line(staff_x, skull_y + 4 * s, staff_x, top_y, (112, 108, 114), 4.5)
    arcade.draw_circle_filled(hd_bx, hd_by, 4 * s, skin_corpse)

    # Обух и широкое зазубренное лезвие косы, нависающее над головой
    tip_x = cx + 26 * d * s
    tip_y = top_y - 10 * s
    blade_pts = (
        (staff_x - 10 * d * s, top_y + 5 * s),
        (staff_x + 2 * d * s, top_y + 12 * s),
        (cx + 4 * d * s, top_y + 13 * s),
        (tip_x, tip_y),
        (cx + 2 * d * s, top_y + 5 * s),
        (staff_x - 2 * d * s, top_y - 3 * s),
    )
    arcade.draw_polygon_filled(blade_pts, scythe_steel)
    arcade.draw_polygon_outline(blade_pts, scythe_edge, 1.6)

    # Светящиеся алые руны вдоль полотна косы (как на референсе)
    rune_alpha = int(255 * rune_pulse)
    for rx_off, ry_off in ((-14, 7), (-7, 8), (0, 8), (7, 6)):
        rx = cx + rx_off * d * s
        ry = top_y + ry_off * s
        arcade.draw_line(rx, ry - 2 * s, rx, ry + 2 * s, (255, 65, 65, rune_alpha), 1.8)
        arcade.draw_line(rx - 2 * s, ry, rx + 2 * s, ry + 1 * s, (255, 65, 65, rune_alpha), 1.4)

def _draw_skeleton_executioner(cx: float, cy: float, s: float, d: float, t: float, b: float):
    """Детализированный спрайт Скелета-Палача по референсу (корона, кираса с шипами, двуручный топор)."""
    axe_heft = math.sin(t * 2.2) * 1.5 * s

    bone_light = (214, 204, 184)
    bone_mid = (168, 158, 140)
    bone_dark = (104, 96, 84)
    armor_light = (158, 154, 148)
    armor_mid = (112, 108, 104)
    armor_dark = (62, 60, 58)
    robe_grey = (138, 132, 124)
    robe_shadow = (86, 82, 76)
    blade_steel = (192, 196, 200)

    # 1. Тяжёлый плащ за спиной и длинная потрёпанная ряса в пол
    cape = (
        (cx - 21 * d * s, cy + 32 * s + b),
        (cx + 21 * d * s, cy + 32 * s + b),
        (cx + 27 * d * s, cy - 50 * s),
        (cx - 27 * d * s, cy - 50 * s),
    )
    arcade.draw_polygon_filled(cape, robe_shadow)
    arcade.draw_polygon_outline(cape, armor_dark, 1.5)

    robe = (
        (cx - 17 * d * s, cy + 2 * s),
        (cx + 17 * d * s, cy + 2 * s),
        (cx + 21 * d * s, cy - 50 * s),
        (cx - 21 * d * s, cy - 50 * s),
    )
    arcade.draw_polygon_filled(robe, robe_grey)
    arcade.draw_polygon_outline(robe, robe_shadow, 1.6)

    # Вертикальные складки рясы и меховая оторочка у колен
    for fx in (-9, 0, 9):
        arcade.draw_line(cx + fx * d * s, cy - 4 * s, cx + (fx * 1.2) * d * s, cy - 49 * s, robe_shadow, 2)
    for kx in (-12, 12):
        arcade.draw_ellipse_filled(cx + kx * d * s, cy - 22 * s, 11 * s, 8 * s, bone_mid)
        arcade.draw_ellipse_outline(cx + kx * d * s, cy - 22 * s, 11 * s, 8 * s, robe_shadow, 1.4)

    # 2. Круглый медальон со звездой на цепях у пояса (как на миниатюре)
    med_x = cx + 1 * d * s
    med_y = cy - 10 * s + b * 0.4
    arcade.draw_line(cx - 14 * d * s, cy + 1 * s + b * 0.5, med_x - 6 * s, med_y + 5 * s, armor_dark, 2)
    arcade.draw_line(cx + 14 * d * s, cy + 1 * s + b * 0.5, med_x + 6 * s, med_y + 5 * s, armor_dark, 2)

    arcade.draw_circle_filled(med_x, med_y, 8.5 * s, armor_mid)
    arcade.draw_circle_outline(med_x, med_y, 8.5 * s, armor_light, 1.6)
    # Лучи звезды внутри медальона
    for deg in range(0, 180, 45):
        rad = math.radians(deg)
        dx_r = math.cos(rad) * 7.5 * s
        dy_r = math.sin(rad) * 7.5 * s
        arcade.draw_line(med_x - dx_r, med_y - dy_r, med_x + dx_r, med_y + dy_r, armor_light, 1.2)

    # 3. Угловатая латная кираса с острым нижним клином и высоким воротником
    cuirass = (
        (cx - 16 * d * s, cy + 8 * s + b * 0.6),
        (cx - 19 * d * s, cy + 31 * s + b),
        (cx + 19 * d * s, cy + 31 * s + b),
        (cx + 16 * d * s, cy + 8 * s + b * 0.6),
        (cx, cy - 1 * s + b * 0.5),
    )
    arcade.draw_polygon_filled(cuirass, armor_mid)
    arcade.draw_polygon_outline(cuirass, armor_light, 1.8)
    arcade.draw_line(cx, cy, cx, cy + 30 * s + b, armor_dark, 2)
    # Зубчатый верхний край горжета
    arcade.draw_line(cx - 14 * d * s, cy + 32 * s + b, cx + 14 * d * s, cy + 32 * s + b, armor_light, 3)

    # 4. Массивные наплечники с вертикальными шипами
    for side in (-1, 1):
        px = cx + side * 21 * d * s
        py = cy + 28 * s + b
        pauldron = (
            (px - side * 5 * d * s, py + 7 * s),
            (px + side * 10 * d * s, py + 4 * s),
            (px + side * 12 * d * s, py - 9 * s),
            (px - side * 4 * d * s, py - 7 * s),
        )
        arcade.draw_polygon_filled(pauldron, armor_light if side > 0 else armor_mid)
        arcade.draw_polygon_outline(pauldron, armor_dark, 1.6)
        # Вертикальный шип на плече
        spike = (
            (px + side * 2 * d * s, py + 5 * s),
            (px + side * 5 * d * s, py + 18 * s),
            (px + side * 8 * d * s, py + 4 * s),
        )
        arcade.draw_polygon_filled(spike, armor_light)
        arcade.draw_polygon_outline(spike, armor_dark, 1.2)

    # 5. Череп в ниспадающем покрывале и высокой зубчатой короне
    hx = cx + 1 * d * s
    hy = cy + 42 * s + b
    # Покрывало за черепом до плеч
    veil = (
        (hx - 12 * d * s, hy + 8 * s),
        (hx + 12 * d * s, hy + 8 * s),
        (hx + 15 * d * s, cy + 29 * s + b),
        (hx - 15 * d * s, cy + 29 * s + b),
    )
    arcade.draw_polygon_filled(veil, robe_grey)
    arcade.draw_polygon_outline(veil, robe_shadow, 1.3)

    # Череп и нижняя челюсть
    arcade.draw_rect_filled(arcade.XYWH(hx + 1 * d * s, hy - 6 * s, 8 * s, 6 * s), bone_mid)
    arcade.draw_circle_filled(hx + 1 * d * s, hy + 1 * s, 8.5 * s, bone_light)
    arcade.draw_circle_outline(hx + 1 * d * s, hy + 1 * s, 8.5 * s, bone_dark, 1.3)
    arcade.draw_circle_filled(hx - 1 * d * s, hy + 1.5 * s, 2.1 * s, (22, 20, 22))
    arcade.draw_circle_filled(hx + 4.5 * d * s, hy + 1.5 * s, 2.0 * s, (22, 20, 22))

    # Зубчатая корона палача
    crown_y = hy + 7 * s
    arcade.draw_rect_filled(arcade.XYWH(hx, crown_y, 19 * s, 6 * s), armor_light)
    arcade.draw_rect_outline(arcade.XYWH(hx, crown_y, 19 * s, 6 * s), armor_dark, 1.3)
    for dx_c, h_c in ((-7, 11), (0, 14), (7, 11)):
        tooth = (
            (hx + (dx_c - 2) * s, crown_y + 3 * s),
            (hx + (dx_c + 2) * s, crown_y + 3 * s),
            (hx + dx_c * s, crown_y + h_c * s),
        )
        arcade.draw_polygon_filled(tooth, armor_light)
        arcade.draw_polygon_outline(tooth, armor_dark, 1.2)

    # 6. Обе руки и тяжёлый двуручный топор палача по диагонали перед собой
    # Координаты рук, сжимающих древко
    hd_bx, hd_by = cx - 20 * d * s, cy - 2 * s + b * 0.5 + axe_heft * 0.5
    hd_fx, hd_fy = cx + 14 * d * s, cy + 12 * s + b * 0.7 + axe_heft

    # Задняя рука
    arcade.draw_line(cx - 21 * d * s, cy + 20 * s + b, cx - 25 * d * s, cy + 8 * s + b * 0.7, bone_dark, 6.5)
    arcade.draw_line(cx - 25 * d * s, cy + 8 * s + b * 0.7, hd_bx, hd_by, armor_mid, 7)
    # Передняя рука
    arcade.draw_line(cx + 21 * d * s, cy + 20 * s + b, cx + 23 * d * s, cy + 9 * s + b * 0.7, bone_mid, 6.5)
    arcade.draw_line(cx + 23 * d * s, cy + 9 * s + b * 0.7, hd_fx, hd_fy, armor_light, 7)

    # Длинное изогнутое древко топора
    haft_end = (cx - 38 * d * s, cy - 14 * s + axe_heft * 0.3)
    haft_top = (cx + 34 * d * s, cy + 20 * s + b * 0.7 + axe_heft * 1.2)
    arcade.draw_line_strip((haft_end, (hd_bx, hd_by), (hd_fx, hd_fy), haft_top), (118, 106, 92), 4.5)
    arcade.draw_line_strip((haft_end, (hd_bx, hd_by), (hd_fx, hd_fy), haft_top), armor_dark, 1.3)

    # Широкое трапециевидное лезвие топора палача (справа от передней руки)
    ax_x = cx + 29 * d * s
    ax_y = cy + 18 * s + b * 0.7 + axe_heft * 1.15
    axe_blade = (
        (ax_x - 4 * d * s, ax_y - 2 * s),
        (ax_x + 5 * d * s, ax_y + 2 * s),
        (ax_x + 16 * d * s, ax_y - 16 * s),
        (ax_x - 3 * d * s, ax_y - 22 * s),
    )
    arcade.draw_polygon_filled(axe_blade, blade_steel)
    arcade.draw_polygon_outline(axe_blade, armor_dark, 1.8)
    # Острая светлая кромка лезвия снизу
    arcade.draw_line(ax_x + 16 * d * s, ax_y - 16 * s, ax_x - 3 * d * s, ax_y - 22 * s, (238, 240, 242), 2.5)

    # Костистые кисти поверх древка
    arcade.draw_circle_filled(hd_bx, hd_by, 4.5 * s, bone_light)
    arcade.draw_circle_outline(hd_bx, hd_by, 4.5 * s, bone_dark, 1.2)
    arcade.draw_circle_filled(hd_fx, hd_fy, 4.8 * s, bone_light)
    arcade.draw_circle_outline(hd_fx, hd_fy, 4.8 * s, bone_dark, 1.2)

def _draw_skeleton_mage(cx: float, cy: float, s: float, d: float, t: float, b: float):
    """Детализированный спрайт Скелета-Мага по референсу (изумрудный плащ, зелёно-золотые молнии)."""
    cloak_sway = math.sin(t * 2.4) * 3.0 * s
    magic_pulse = math.sin(t * 6.0) * 2.0 * s

    bone_light = (224, 228, 206)
    bone_mid = (168, 184, 156)
    bone_shadow = (104, 124, 102)
    cloak_dark = (22, 36, 28)
    cloak_mid = (38, 64, 48)
    cloak_edge = (82, 138, 96)
    fel_green = (55, 245, 95)
    spark_gold = (255, 205, 65)

    # 1. Изумрудная аура магии за спиной и рваный плащ с острыми плечами
    arcade.draw_ellipse_filled(cx, cy + 8 * s + b, 74 * s, 92 * s, (35, 185, 75, 45))

    cloak_pts = (
        (cx - 28 * d * s, cy + 36 * s + b),
        (cx - 12 * d * s, cy + 30 * s + b),
        (cx + 12 * d * s, cy + 30 * s + b),
        (cx + 28 * d * s, cy + 36 * s + b),
        (cx + 31 * d * s + cloak_sway, cy - 28 * s),
        (cx + 21 * d * s, cy - 14 * s),
        (cx + 14 * d * s - cloak_sway * 0.5, cy - 32 * s),
        (cx + 6 * d * s, cy - 8 * s),
        (cx - 6 * d * s, cy - 8 * s),
        (cx - 14 * d * s + cloak_sway * 0.5, cy - 32 * s),
        (cx - 21 * d * s, cy - 14 * s),
        (cx - 31 * d * s + cloak_sway, cy - 28 * s),
    )
    arcade.draw_polygon_filled(cloak_pts, cloak_dark)
    arcade.draw_polygon_outline(cloak_pts, cloak_edge, 1.5)

    # 2. Костистые ноги, таз и зелёная набедренная драпировка
    for side, lx in ((-1, cx - 10 * d * s), (1, cx + 10 * d * s)):
        arcade.draw_line(lx, cy - 6 * s, lx + side * 3 * d * s, cy - 28 * s, bone_mid, 4.5)
        arcade.draw_line(lx + side * 3 * d * s, cy - 28 * s, lx + side * 4 * d * s, cy - 50 * s, bone_shadow, 4)
        arcade.draw_circle_filled(lx + side * 3 * d * s, cy - 28 * s, 3.5 * s, bone_light)

    # Тазовая кость и набедренная ткань
    pelvis = (
        (cx - 15 * d * s, cy),
        (cx + 15 * d * s, cy),
        (cx + 11 * d * s, cy - 11 * s),
        (cx - 11 * d * s, cy - 11 * s),
    )
    arcade.draw_polygon_filled(pelvis, bone_mid)
    drape = (
        (cx - 9 * d * s, cy - 2 * s),
        (cx + 9 * d * s, cy - 2 * s),
        (cx + 12 * d * s, cy - 26 * s),
        (cx, cy - 20 * s),
        (cx - 11 * d * s, cy - 28 * s),
    )
    arcade.draw_polygon_filled(drape, cloak_mid)
    arcade.draw_polygon_outline(drape, cloak_edge, 1.3)

    # 3. Позвоночник и грудная клетка с рёбрами
    arcade.draw_line(cx, cy - 2 * s, cx, cy + 40 * s + b, bone_shadow, 4.5)
    for idx, ry in enumerate((9, 14, 19, 24, 29)):
        rw = (10 + idx * 1.3) * s
        arcade.draw_arc_outline(cx, cy + ry * s + b, rw * 2.1, 7.5 * s, bone_light, 185, 355, 2.4)
    arcade.draw_line(cx, cy + 15 * s + b, cx, cy + 31 * s + b, bone_mid, 2.8)
    # Ключицы и складки воротника плаща
    arcade.draw_line(cx - 19 * d * s, cy + 31 * s + b, cx + 19 * d * s, cy + 31 * s + b, cloak_mid, 5)
    arcade.draw_line(cx - 19 * d * s, cy + 31 * s + b, cx + 19 * d * s, cy + 31 * s + b, cloak_edge, 1.5)

    # 4. Череп с тёмными глазницами и зубами
    hx = cx
    hy = cy + 46 * s + b
    arcade.draw_rect_filled(arcade.XYWH(hx, hy - 8 * s, 9 * s, 6 * s), bone_mid)
    arcade.draw_circle_filled(hx, hy + 2 * s, 10 * s, bone_light)
    arcade.draw_circle_outline(hx, hy + 2 * s, 10 * s, bone_shadow, 1.4)

    # Глазницы и нос
    arcade.draw_circle_filled(hx - 3.8 * d * s, hy + 1.5 * s, 2.5 * s, (18, 22, 18))
    arcade.draw_circle_filled(hx + 3.8 * d * s, hy + 1.5 * s, 2.5 * s, (18, 22, 18))
    arcade.draw_polygon_filled(((hx, hy), (hx - 1.5 * s, hy - 3 * s), (hx + 1.5 * s, hy - 3 * s)), (18, 22, 18))
    for zx in (-3, -1, 1, 3):
        arcade.draw_line(hx + zx * s, hy - 5.5 * s, hx + zx * s, hy - 8.5 * s, (25, 28, 24), 1.1)

    # 5. Раскинутые костистые руки с зелёно-золотой магией и кристаллом
    # Левая рука (на арте — вытянута вниз и в сторону в вихре зелёных и золотых разрядов)
    sh_lx, sh_ly = cx - 18 * d * s, cy + 29 * s + b
    el_lx, el_ly = cx - 30 * d * s, cy + 12 * s + b * 0.7
    hd_lx, hd_ly = cx - 42 * d * s, cy - 3 * s + b * 0.5
    arcade.draw_line(sh_lx, sh_ly, el_lx, el_ly, bone_mid, 3.8)
    arcade.draw_line(el_lx, el_ly, hd_lx, hd_ly, bone_light, 3.5)
    arcade.draw_circle_filled(el_lx, el_ly, 3.5 * s, bone_light)
    arcade.draw_circle_filled(hd_lx, hd_ly, 3.8 * s, bone_light)

    # Зелёное пламя над кистью и золотые искры вниз
    arcade.draw_circle_filled(hd_lx, hd_ly + 4 * s, 11 * s + magic_pulse, (55, 245, 95, 70))
    bolt_l_up = (
        (hd_lx - 3 * d * s, hd_ly + 2 * s),
        (hd_lx - 6 * d * s, hd_ly + 11 * s),
        (hd_lx + 2 * d * s, hd_ly + 16 * s),
        (hd_lx + 5 * d * s, hd_ly + 4 * s),
    )
    arcade.draw_line_strip(bolt_l_up, fel_green, 1.8)
    bolt_l_down = (
        (hd_lx, hd_ly - 2 * s),
        (hd_lx - 4 * d * s, hd_ly - 12 * s),
        (hd_lx + 3 * d * s, hd_ly - 20 * s),
        (hd_lx - 2 * d * s, hd_ly - 28 * s),
    )
    arcade.draw_line_strip(bolt_l_down, spark_gold, 2.0)

    # Правая рука (поднята, держит светящийся изумрудный кристалл-жезл)
    sh_rx, sh_ry = cx + 18 * d * s, cy + 29 * s + b
    el_rx, el_ry = cx + 31 * d * s, cy + 11 * s + b * 0.7
    hd_rx, hd_ry = cx + 41 * d * s, cy + 18 * s + b * 0.8
    arcade.draw_line(sh_rx, sh_ry, el_rx, el_ry, bone_mid, 3.8)
    arcade.draw_line(el_rx, el_ry, hd_rx, hd_ry, bone_light, 3.5)
    arcade.draw_circle_filled(el_rx, el_ry, 3.5 * s, bone_light)

    # Изумрудный кристалл в ладони и аура зелёных молний
    arcade.draw_circle_filled(hd_rx, hd_ry + 8 * s, 14 * s + magic_pulse, (55, 245, 95, 75))
    crystal = (
        (hd_rx - 2.5 * s, hd_ry + 1 * s),
        (hd_rx + 2.5 * s, hd_ry + 1 * s),
        (hd_rx + 2 * s, hd_ry + 19 * s),
        (hd_rx, hd_ry + 23 * s),
        (hd_rx - 2 * s, hd_ry + 19 * s),
    )
    arcade.draw_polygon_filled(crystal, (125, 255, 165))
    arcade.draw_polygon_outline(crystal, fel_green, 1.4)
    arcade.draw_circle_filled(hd_rx, hd_ry, 3.8 * s, bone_light)

    # Зелёные молнии вокруг кристалла и золотой разряд вниз
    bolt_r_up = (
        (hd_rx - 6 * s, hd_ry + 6 * s),
        (hd_rx - 9 * s, hd_ry + 18 * s),
        (hd_rx + 4 * s, hd_ry + 28 * s),
        (hd_rx + 9 * s, hd_ry + 14 * s),
    )
    arcade.draw_line_strip(bolt_r_up, fel_green, 1.8)
    bolt_r_down = (
        (hd_rx, hd_ry - 3 * s),
        (hd_rx + 5 * d * s, hd_ry - 14 * s),
        (hd_rx - 3 * d * s, hd_ry - 24 * s),
        (hd_rx + 2 * d * s, hd_ry - 34 * s),
    )
    arcade.draw_line_strip(bolt_r_down, spark_gold, 2.0)

def _draw_hell_cerberus(cx: float, cy: float, s: float, d: float, t: float, b: float):
    """Детализированный спрайт Адского Цербера (обсидиановый мех, стальные наручи, пламя)."""
    flame_wave = math.sin(t * 7.5) * 3.0 * s
    tail_sway = math.sin(t * 2.6) * 4.0 * s

    fur_black = (20, 22, 28)
    fur_dark = (32, 36, 46)
    fur_highlight = (58, 68, 86)
    steel_dark = (52, 56, 64)
    steel_mid = (96, 102, 112)
    steel_light = (158, 166, 178)
    fire_red = (218, 46, 18)
    fire_orange = (252, 118, 24)
    fire_yellow = (255, 222, 88)
    claw_red = (156, 28, 28)
    tooth_white = (238, 232, 218)

    # 1. Пылающий хвост за спиной
    t_base = (cx - 32 * d * s, cy - 4 * s + b * 0.4)
    t_mid = (cx - 56 * d * s, cy + 12 * s + tail_sway * 0.5)
    t_tip = (cx - 68 * d * s + tail_sway, cy + 34 * s)
    tx, ty = t_tip

    arcade.draw_line_strip((t_base, t_mid, t_tip), fur_black, 6)
    arcade.draw_line_strip((t_base, t_mid, t_tip), fur_highlight, 2)
    arcade.draw_circle_filled(tx, ty + 4 * s, 9 * s, (252, 118, 24, 150))
    arcade.draw_polygon_filled(
        ((tx - 4 * s, ty), (tx + 4 * s, ty), (tx + flame_wave * 0.5, ty + 18 * s)),
        fire_orange,
    )
    arcade.draw_polygon_filled(
        ((tx - 2 * s, ty + 2 * s), (tx + 2 * s, ty + 2 * s), (tx + flame_wave * 0.3, ty + 11 * s)),
        fire_yellow,
    )

    # 2. Дальние лапы и звенья разорванной цепи на земле
    arcade.draw_line(cx - 28 * d * s, cy - 8 * s, cx - 36 * d * s, cy - 46 * s, fur_black, 9)
    arcade.draw_ellipse_filled(cx - 33 * d * s, cy - 49 * s, 14 * s, 6 * s, fur_black)

    fl_x, fl_y = cx + 32 * d * s, cy - 46 * s
    arcade.draw_line(cx + 18 * d * s, cy - 4 * s, cx + 28 * d * s, cy - 26 * s, fur_dark, 10)
    arcade.draw_line(cx + 28 * d * s, cy - 26 * s, fl_x, fl_y, fur_black, 9)
    arcade.draw_rect_filled(arcade.XYWH(cx + 30 * d * s, cy - 34 * s, 12 * s, 9 * s), steel_dark)
    arcade.draw_rect_outline(arcade.XYWH(cx + 30 * d * s, cy - 34 * s, 12 * s, 9 * s), steel_light, 1.4)
    arcade.draw_ellipse_filled(fl_x + 4 * d * s, cy - 49 * s, 15 * s, 6.5 * s, fur_black)

    for idx in range(6):
        ch_x = cx + (38 - idx * 14) * d * s
        ch_y = cy - (48 + (idx % 2) * 2) * s
        arcade.draw_ellipse_outline(ch_x, ch_y, 12 * s, 6 * s, (48, 50, 56), 2.5)
        arcade.draw_ellipse_outline(ch_x, ch_y, 12 * s, 6 * s, steel_mid, 1.0)

    # 3. Пылающая огненная грива вдоль спины и загривка
    mane_pts = ((-28, 12, 13), (-18, 20, 16), (-6, 27, 19), (4, 34, 18), (12, 42, 16))
    for mx, my, mr in mane_pts:
        px = cx + mx * d * s
        py = cy + my * s + b * 0.8
        arcade.draw_circle_filled(px, py, mr * s, (218, 46, 18, 130))
        arcade.draw_polygon_filled(
            ((px - mr * 0.6 * s, py - 2 * s), (px + mr * 0.6 * s, py - 2 * s), (px - 5 * d * s + flame_wave * 0.5, py + mr * 1.35 * s)),
            fire_orange,
        )
        arcade.draw_polygon_filled(
            ((px - mr * 0.3 * s, py), (px + mr * 0.3 * s, py), (px - 2 * d * s + flame_wave * 0.3, py + mr * 0.85 * s)),
            fire_yellow,
        )

    # 4. Мускулистое обсидианово-чёрное тело с магматическими трещинами
    torso = (
        (cx - 34 * d * s, cy - 4 * s),
        (cx - 16 * d * s, cy + 20 * s + b),
        (cx + 22 * d * s, cy + 22 * s + b),
        (cx + 28 * d * s, cy - 12 * s),
        (cx - 22 * d * s, cy - 16 * s),
    )
    arcade.draw_polygon_filled(torso, fur_dark)
    arcade.draw_polygon_outline(torso, fur_black, 2)
    arcade.draw_ellipse_filled(cx + 6 * d * s, cy + 6 * s + b * 0.7, 26 * s, 22 * s, fur_highlight)
    arcade.draw_ellipse_filled(cx + 5 * d * s, cy + 5 * s + b * 0.7, 21 * s, 17 * s, fur_dark)
    arcade.draw_line(cx + 2 * d * s, cy + 10 * s + b * 0.7, cx + 9 * d * s, cy + 2 * s + b * 0.6, fire_orange, 1.8)
    arcade.draw_line(cx + 9 * d * s, cy + 2 * s + b * 0.6, cx + 6 * d * s, cy - 5 * s + b * 0.5, fire_red, 1.5)

    # 5. Ближние мощные лапы со стальными доспехами и багровыми когтями
    rh_x, rh_y = cx - 22 * d * s, cy - 2 * s
    rk_x, rk_y = cx - 16 * d * s, cy - 25 * s
    rf_x, rf_y = cx - 24 * d * s, cy - 48 * s
    arcade.draw_line(rh_x, rh_y, rk_x, rk_y, fur_highlight, 13)
    arcade.draw_line(rk_x, rk_y, rf_x, rf_y, fur_dark, 9.5)
    thigh_plate = ((rh_x - 7 * d * s, rh_y - 4 * s), (rh_x + 8 * d * s, rh_y - 2 * s), (rk_x + 7 * d * s, rk_y + 4 * s), (rk_x - 6 * d * s, rk_y + 2 * s))
    arcade.draw_polygon_filled(thigh_plate, steel_mid)
    arcade.draw_polygon_outline(thigh_plate, steel_light, 1.5)
    arcade.draw_ellipse_filled(rf_x + 5 * d * s, cy - 49 * s, 16 * s, 7 * s, fur_black)
    for cl in (-3, 1, 5):
        arcade.draw_circle_filled(rf_x + (11 + cl * 0.3) * d * s, cy - 50 * s, 2.0 * s, claw_red)

    fh_x, fh_y = cx + 12 * d * s, cy - 2 * s + b * 0.4
    fk_x, fk_y = cx + 10 * d * s, cy - 24 * s
    ff_x, ff_y = cx + 8 * d * s, cy - 48 * s
    arcade.draw_line(fh_x, fh_y, fk_x, fk_y, fur_highlight, 14)
    arcade.draw_line(fk_x, fk_y, ff_x, ff_y, fur_dark, 11)
    bracer = ((fk_x - 7 * s, fk_y - 2 * s), (fk_x + 7 * s, fk_y - 2 * s), (ff_x + 6.5 * s, ff_y + 7 * s), (ff_x - 6.5 * s, ff_y + 7 * s))
    arcade.draw_polygon_filled(bracer, steel_mid)
    arcade.draw_polygon_outline(bracer, steel_light, 1.8)
    for ry_off in (-6, -13):
        arcade.draw_circle_filled(fk_x - 3 * s, fk_y + ry_off * s, 1.2 * s, steel_light)
        arcade.draw_circle_filled(fk_x + 3 * s, fk_y + ry_off * s, 1.2 * s, steel_light)

    arcade.draw_ellipse_filled(ff_x + 4 * d * s, cy - 49 * s, 18 * s, 8 * s, fur_black)
    for cl in (-4, 0, 4):
        cx_claw = ff_x + (11 + cl * 0.4) * d * s
        arcade.draw_polygon_filled(((cx_claw - 2 * s, cy - 48 * s), (cx_claw + 3 * d * s, cy - 52 * s), (cx_claw, cy - 46 * s)), claw_red)

    # 6. ДАЛЬНЯЯ (ВЫДВИНУТАЯ ВПЕРЁД) ГОЛОВА
    h2x, h2y = cx + 38 * d * s, cy + 16 * s + b * 0.8
    arcade.draw_line(cx + 16 * d * s, cy + 16 * s + b, h2x - 6 * d * s, h2y, fur_dark, 13)
    arcade.draw_polygon_filled(((h2x - 6 * s, h2y + 6 * s), (h2x + 4 * s, h2y + 6 * s), (h2x - 2 * d * s + flame_wave * 0.4, h2y + 20 * s)), fire_orange)
    arcade.draw_ellipse_filled(h2x, h2y + 3 * s, 21 * s, 12 * s, fur_black)
    arcade.draw_polygon_filled(((h2x - 7 * d * s, h2y + 7 * s), (h2x - 11 * d * s, h2y + 16 * s), (h2x - 2 * d * s, h2y + 9 * s)), fur_dark)
    arcade.draw_circle_filled(h2x + 5 * d * s, h2y - 2 * s, 5.5 * s, fire_orange)
    arcade.draw_circle_filled(h2x + 5 * d * s, h2y - 2 * s, 3.0 * s, fire_yellow)
    arcade.draw_polygon_filled(((h2x - 6 * d * s, h2y - 3 * s), (h2x + 12 * d * s, h2y - 5 * s), (h2x + 8 * d * s, h2y - 10 * s), (h2x - 8 * d * s, h2y - 9 * s)), fur_dark)
    arcade.draw_circle_filled(h2x + 2 * d * s, h2y + 4 * s, 2.2 * s, fire_yellow)
    for tx in (3, 7, 10):
        arcade.draw_line(h2x + tx * d * s, h2y, h2x + tx * d * s, h2y - 3 * s, tooth_white, 1.4)

    # 7. ВЕРХНЯЯ (ГЛАВНАЯ) ГОЛОВА В СТАЛЬНОМ ОШЕЙНИКЕ
    h1x, h1y = cx + 18 * d * s, cy + 44 * s + b
    arcade.draw_line(cx + 6 * d * s, cy + 18 * s + b, h1x - 2 * d * s, h1y - 4 * s, fur_dark, 17)
    collar = ((cx + 1 * d * s, cy + 28 * s + b), (cx + 21 * d * s, cy + 24 * s + b), (cx + 24 * d * s, cy + 13 * s + b), (cx + 12 * d * s, cy + 8 * s + b), (cx - 1 * d * s, cy + 18 * s + b))
    arcade.draw_polygon_filled(collar, steel_mid)
    arcade.draw_polygon_outline(collar, steel_light, 1.8)
    for rx_c, ry_c in ((4, 24), (11, 22), (18, 21)):
        arcade.draw_circle_filled(cx + rx_c * d * s, cy + ry_c * s + b, 1.4 * s, steel_light)

    arcade.draw_polygon_filled(((h1x - 9 * s, h1y + 7 * s), (h1x + 5 * s, h1y + 7 * s), (h1x - 2 * d * s + flame_wave * 0.5, h1y + 25 * s)), fire_orange)
    arcade.draw_polygon_filled(((h1x - 5 * s, h1y + 8 * s), (h1x + 3 * s, h1y + 8 * s), (h1x - 1 * d * s + flame_wave * 0.3, h1y + 18 * s)), fire_yellow)
    arcade.draw_ellipse_filled(h1x, h1y + 4 * s, 23 * s, 14 * s, fur_black)
    arcade.draw_ellipse_outline(h1x, h1y + 4 * s, 23 * s, 14 * s, fur_highlight, 1.3)
    arcade.draw_polygon_filled(((h1x - 8 * d * s, h1y + 8 * s), (h1x - 12 * d * s, h1y + 19 * s), (h1x - 3 * d * s, h1y + 10 * s)), fur_dark)
    arcade.draw_polygon_filled(((h1x - 1 * d * s, h1y + 8 * s), (h1x - 3 * d * s, h1y + 18 * s), (h1x + 4 * d * s, h1y + 9 * s)), fur_dark)

    arcade.draw_circle_filled(h1x + 6 * d * s, h1y - 2 * s, 6.5 * s, fire_orange)
    arcade.draw_circle_filled(h1x + 6 * d * s, h1y - 2 * s, 3.8 * s, fire_yellow)
    jaw1 = ((h1x - 5 * d * s, h1y - 3 * s), (h1x + 13 * d * s, h1y - 6 * s), (h1x + 9 * d * s, h1y - 12 * s), (h1x - 7 * d * s, h1y - 10 * s))
    arcade.draw_polygon_filled(jaw1, fur_dark)
    arcade.draw_circle_filled(h1x + 3 * d * s, h1y + 5 * s, 2.5 * s, fire_yellow)
    for tx in (3, 7, 11):
        arcade.draw_line(h1x + tx * d * s, h1y + 1 * s, h1x + tx * d * s, h1y - 2.5 * s, tooth_white, 1.6)
        arcade.draw_line(h1x + tx * d * s, h1y - 6 * s, h1x + tx * d * s, h1y - 3 * s, tooth_white, 1.5)

    # 8. ПЕРЕДНЯЯ (НИЖНЯЯ) ГОЛОВА В ХИЩНОМ ВЫПАДЕ
    h3x, h3y = cx + 22 * d * s, cy - 8 * s + b * 0.5
    arcade.draw_polygon_filled(((h3x - 9 * s, h3y + 8 * s), (h3x + 7 * s, h3y + 8 * s), (h3x - 3 * d * s + flame_wave * 0.6, h3y + 28 * s)), fire_orange)
    arcade.draw_polygon_filled(((h3x - 5 * s, h3y + 9 * s), (h3x + 4 * s, h3y + 9 * s), (h3x - 1 * d * s + flame_wave * 0.4, h3y + 20 * s)), fire_yellow)
    arcade.draw_ellipse_filled(h3x, h3y + 2 * s, 22 * s, 20 * s, fur_black)
    arcade.draw_ellipse_outline(h3x, h3y + 2 * s, 22 * s, 20 * s, fur_highlight, 1.4)
    arcade.draw_polygon_filled(((h3x - 8 * s, h3y + 8 * s), (h3x - 12 * s, h3y + 19 * s), (h3x - 3 * s, h3y + 11 * s)), fur_dark)
    arcade.draw_polygon_filled(((h3x + 8 * s, h3y + 8 * s), (h3x + 12 * s, h3y + 19 * s), (h3x + 3 * s, h3y + 11 * s)), fur_dark)

    arcade.draw_circle_filled(h3x - 4.5 * s, h3y + 3 * s, 2.8 * s, fire_orange)
    arcade.draw_circle_filled(h3x + 4.5 * s, h3y + 3 * s, 2.8 * s, fire_orange)
    arcade.draw_circle_filled(h3x - 4.5 * s, h3y + 3 * s, 1.4 * s, fire_yellow)
    arcade.draw_circle_filled(h3x + 4.5 * s, h3y + 3 * s, 1.4 * s, fire_yellow)

    arcade.draw_ellipse_filled(h3x + 1 * d * s, h3y - 3 * s, 13 * s, 10 * s, fur_dark)
    arcade.draw_rect_filled(arcade.XYWH(h3x + 1 * d * s, h3y - 8 * s, 11 * s, 6 * s), (88, 22, 24))
    for zx in (-4, -1.5, 1.5, 4):
        arcade.draw_line(h3x + zx * s, h3y - 5.5 * s, h3x + zx * s, h3y - 9.5 * s, tooth_white, 1.6)



def _draw_evil_wizard(cx: float, cy: float, s: float, d: float, t: float, b: float):
    """Детализированный спрайт Злого Волшебника по референсу (чёрная мантия, седая борода, змеиный посох)."""
    sleeve_sway = math.sin(t * 2.2) * 2.5 * s
    beard_sway = math.sin(t * 2.0) * 1.5 * s

    robe_black = (18, 19, 24)
    robe_charcoal = (34, 37, 44)
    silver_trim = (118, 128, 142)
    silver_bright = (176, 186, 198)
    skin_pale = (212, 188, 174)
    skin_shadow = (158, 134, 124)
    beard_white = (228, 228, 224)
    beard_grey = (176, 178, 176)
    wood_staff = (108, 86, 62)
    wood_dark = (66, 52, 36)

    # 1. Чёрные башмаки под подолом и длинная мантия
    arcade.draw_ellipse_filled(cx - 10 * d * s, cy - 50 * s, 12 * s, 6 * s, (14, 14, 18))
    arcade.draw_ellipse_filled(cx + 10 * d * s, cy - 50 * s, 12 * s, 6 * s, (14, 14, 18))

    robe_body = (
        (cx - 18 * d * s, cy + 28 * s + b),
        (cx + 18 * d * s, cy + 28 * s + b),
        (cx + 25 * d * s, cy - 49 * s),
        (cx - 25 * d * s, cy - 49 * s),
    )
    arcade.draw_polygon_filled(robe_body, robe_black)
    arcade.draw_polygon_outline(robe_body, robe_charcoal, 1.5)

    # Передние серебристо-пепельные фалды мантии с вертикальными складками
    front_panel = (
        (cx - 11 * d * s, cy + 4 * s + b * 0.5),
        (cx + 11 * d * s, cy + 4 * s + b * 0.5),
        (cx + 16 * d * s, cy - 49 * s),
        (cx - 16 * d * s, cy - 49 * s),
    )
    arcade.draw_polygon_filled(front_panel, robe_charcoal)
    arcade.draw_line(cx - 11 * d * s, cy + 4 * s, cx - 16 * d * s, cy - 49 * s, silver_trim, 2)
    arcade.draw_line(cx + 11 * d * s, cy + 4 * s, cx + 16 * d * s, cy - 49 * s, silver_trim, 2)
    arcade.draw_line(cx, cy + 4 * s, cx, cy - 49 * s, robe_black, 2)

    # 2. Широкие треугольные отвороты (воротник-наплечники) и усеянный пояс
    for side in (-1, 1):
        lapel = (
            (cx, cy + 12 * s + b),
            (cx + side * 24 * d * s, cy + 31 * s + b),
            (cx + side * 14 * d * s, cy + 34 * s + b),
            (cx + side * 5 * d * s, cy + 14 * s + b),
        )
        arcade.draw_polygon_filled(lapel, robe_charcoal)
        arcade.draw_polygon_outline(lapel, silver_trim, 1.5)

    # Широкий чёрный пояс с серебряными заклёпками и ромбовидной пряжкой
    belt_y = cy + 6 * s + b * 0.6
    arcade.draw_rect_filled(arcade.XYWH(cx, belt_y, 26 * s, 9 * s), robe_black)
    arcade.draw_rect_outline(arcade.XYWH(cx, belt_y, 26 * s, 9 * s), silver_trim, 1.4)
    for bx_off in (-9, -5, 5, 9):
        arcade.draw_circle_filled(cx + bx_off * d * s, belt_y + 1.5 * s, 1.0 * s, silver_bright)
        arcade.draw_circle_filled(cx + bx_off * d * s, belt_y - 1.5 * s, 1.0 * s, silver_bright)

    buckle = (
        (cx, belt_y + 5.5 * s),
        (cx + 4.5 * s, belt_y),
        (cx, belt_y - 5.5 * s),
        (cx - 4.5 * s, belt_y),
    )
    arcade.draw_polygon_filled(buckle, robe_charcoal)
    arcade.draw_polygon_outline(buckle, silver_bright, 1.5)

    # 3. Остроконечный капюшон, бледное лицо и длинная седая борода до пояса
    hx = cx
    hy = cy + 38 * s + b
    hood = (
        (hx - 14 * d * s, hy - 12 * s),
        (hx - 11 * d * s, hy + 10 * s),
        (hx, hy + 22 * s),
        (hx + 11 * d * s, hy + 10 * s),
        (hx + 14 * d * s, hy - 12 * s),
    )
    arcade.draw_polygon_filled(hood, robe_black)
    arcade.draw_polygon_outline(hood, silver_trim, 1.5)

    # Бледное суровое лицо внутри капюшона
    arcade.draw_ellipse_filled(hx, hy + 1 * s, 13 * s, 15 * s, skin_pale)
    arcade.draw_circle_filled(hx - 3 * d * s, hy + 2 * s, 2.2 * s, skin_shadow)
    arcade.draw_circle_filled(hx + 3 * d * s, hy + 2 * s, 2.2 * s, skin_shadow)
    arcade.draw_circle_filled(hx - 3 * d * s, hy + 2 * s, 1.0 * s, (25, 25, 30))
    arcade.draw_circle_filled(hx + 3 * d * s, hy + 2 * s, 1.0 * s, (25, 25, 30))
    arcade.draw_line(hx - 5 * d * s, hy + 5 * s, hx - 1 * d * s, hy + 3.5 * s, beard_white, 2)
    arcade.draw_line(hx + 5 * d * s, hy + 5 * s, hx + 1 * d * s, hy + 3.5 * s, beard_white, 2)

    # Густая длинная седая борода с усами до самого пояса
    beard_pts = (
        (hx - 7 * d * s, hy - 2 * s),
        (hx + 7 * d * s, hy - 2 * s),
        (hx + 10 * d * s, hy - 18 * s),
        (hx + 5 * d * s + beard_sway, cy + 9 * s + b * 0.6),
        (hx - 5 * d * s + beard_sway, cy + 9 * s + b * 0.6),
        (hx - 10 * d * s, hy - 18 * s),
    )
    arcade.draw_polygon_filled(beard_pts, beard_white)
    arcade.draw_polygon_outline(beard_pts, beard_grey, 1.3)
    arcade.draw_line(hx - 2 * d * s, hy - 6 * s, hx - 3 * d * s + beard_sway, cy + 11 * s + b * 0.6, beard_grey, 1.3)
    arcade.draw_line(hx + 2 * d * s, hy - 6 * s, hx + 3 * d * s + beard_sway, cy + 11 * s + b * 0.6, beard_grey, 1.3)

    # 4. Передняя рука с широким рукавом, отведена в сторону с раскрытой ладонью
    sh_fx, sh_fy = cx + 17 * d * s, cy + 25 * s + b
    hd_fx, hd_fy = cx + 38 * d * s, cy + 10 * s + b * 0.7
    sleeve_front = (
        (sh_fx, sh_fy + 3 * s),
        (hd_fx - 3 * d * s, hd_fy + 4 * s),
        (hd_fx - 6 * d * s, hd_fy - 18 * s + sleeve_sway),
        (cx + 17 * d * s, cy + 2 * s + b * 0.5),
    )
    arcade.draw_polygon_filled(sleeve_front, robe_black)
    arcade.draw_polygon_outline(sleeve_front, robe_charcoal, 1.4)
    arcade.draw_circle_filled(hd_fx, hd_fy, 4 * s, skin_pale)
    for fx_off, fy_off in ((4, 4), (7, 1), (7, -2), (5, -4)):
        arcade.draw_line(hd_fx, hd_fy, hd_fx + fx_off * d * s, hd_fy + fy_off * s, skin_pale, 1.6)

    # 5. Задняя рука с широким рукавом и изогнутый змеиный посох
    staff_x = cx - 34 * d * s
    sh_bx, sh_by = cx - 17 * d * s, cy + 25 * s + b
    hd_bx, hd_by = staff_x, cy + 14 * s + b * 0.7
    sleeve_back = (
        (sh_bx, sh_by + 3 * s),
        (hd_bx + 3 * d * s, hd_by + 4 * s),
        (hd_bx + 6 * d * s, hd_by - 18 * s - sleeve_sway),
        (cx - 17 * d * s, cy + 2 * s + b * 0.5),
    )
    arcade.draw_polygon_filled(sleeve_back, robe_black)
    arcade.draw_polygon_outline(sleeve_back, robe_charcoal, 1.4)

    # Узловатый змеиный посох от земли до высоты головы
    staff_pts = (
        (staff_x + 2 * d * s, cy - 52 * s),
        (staff_x, cy - 18 * s),
        (staff_x + 1 * d * s, cy + 14 * s + b * 0.7),
        (staff_x - 3 * d * s, cy + 30 * s + b),
        (staff_x + 3 * d * s, cy + 38 * s + b),
    )
    arcade.draw_line_strip(staff_pts, wood_staff, 5)
    arcade.draw_line_strip(staff_pts, wood_dark, 1.5)

    # Голова змеи на вершине посоха с раскрытой пастью и клыками
    snake_x = staff_x + 3 * d * s
    snake_y = cy + 39 * s + b
    arcade.draw_ellipse_filled(snake_x + 3 * d * s, snake_y + 1 * s, 9 * s, 5 * s, wood_staff)
    arcade.draw_line(snake_x + 2 * d * s, snake_y - 1 * s, snake_x + 7 * d * s, snake_y - 3 * s, wood_dark, 2.5)
    arcade.draw_circle_filled(snake_x + 3 * d * s, snake_y + 2 * s, 1.2 * s, (215, 65, 45))
    arcade.draw_line(snake_x + 6 * d * s, snake_y, snake_x + 6 * d * s, snake_y - 2.5 * s, (235, 230, 215), 1.2)

    # Кисть руки, сжимающая посох
    arcade.draw_circle_filled(hd_bx, hd_by, 4.5 * s, skin_pale)
    arcade.draw_circle_outline(hd_bx, hd_by, 4.5 * s, skin_shadow, 1.2)



def draw_enemy_sprite(role: str, cx: float, cy: float, s: float, d: int, b: float, t: float):
    """Рисует детализированную дарк-фэнтези фигурку врага с уникальной анимацией."""

    if role == "Чёрный Скелет-Маг":
        _draw_black_skeleton_mage(cx, cy, s, d, t, b)
        return
    elif role == "Дракон":
        _draw_crystal_dragon(cx, cy, s, d, t, b)
        return
    elif role == "Гоблин":
        _draw_goblin(cx, cy, s, d, t, b)
        return

    elif role == "Огр":
        _draw_ogre(cx, cy, s, d, t, b)
        return

    elif role == "Скелет":
        _draw_skeleton_swordsman(cx, cy, s, d, t, b)
        return

    elif role == "Скелет-стрелок":
        _draw_skeleton_archer(cx, cy, s, d, t, b)
        return

    elif role == "Король Гоблинов":
        _draw_goblin_king(cx, cy, s, d, t, b)
        return

    elif role == "Слизняк":
        _draw_slime(cx, cy, s, d, t, b)
        return

    elif role == "Тёмный Рыцарь":
        _draw_dark_knight(cx, cy, s, d, t, b)
        return

    elif role == "Костяной Страж":
        _draw_bone_axe_guard(cx, cy, s, d, t, b)
        return

    elif role == "Скелет-гигант":
        _draw_skeleton_giant(cx, cy, s, d, t, b)
        return

    elif role == "Зомби":
        _draw_plague_zombie(cx, cy, s, d, t, b)
        return

    elif role == "Вор":
        _draw_thief(cx, cy, s, d, t, b)
        return

    elif role == "Мумия":
        _draw_mummy(cx, cy, s, d, t, b)
        return

    elif role == "Некромант":
        _draw_necromancer(cx, cy, s, d, t, b)
        return

    elif role == "Верховный Лич":
        _draw_supreme_lich(cx, cy, s, d, t, b)
        return

    elif role == "Злой Волшебник":
        _draw_evil_wizard(cx, cy, s, d, t, b)
        return

    elif role == "Скелет-палач":
        _draw_skeleton_executioner(cx, cy, s, d, t, b)
        return

    elif role == "Скелет-маг":
        _draw_skeleton_mage(cx, cy, s, d, t, b)
        return

    elif role in ("Адский цербер", "Цербер"):
        _draw_hell_cerberus(cx, cy, s, d, t, b)
        return

