import json
import os
import random
import math
import arcade
from config import BORDER_GOLD
from core.entity import Entity
from core.card import EnemyAction
from core.effects import build_effects


class Enemy(Entity):
    def __init__(self, name: str, role: str, base_hp: int, is_boss: bool, actions: list[EnemyAction],
                 ng_level: int = 0):
        hp_scale = 1.0 + ng_level * 0.35
        super().__init__(name, int(base_hp * hp_scale))
        self.role = role
        self.is_boss = is_boss
        self.ng_level = ng_level
        self.actions = actions

        self.planned_action: EnemyAction | None = None
        self.last_action_text: str = "Первый ход (действий еще не было)"

    def _s(self, val: int) -> int:
        return int(val * (1.0 + self.ng_level * 0.25))

    def choose_action(self) -> EnemyAction:
        self.planned_action = random.choice(self.actions)
        return self.planned_action


def create_enemy_for_stage(stage: int, round_idx: int, ng_level: int = 0) -> Enemy:
    """
    stage: 1, 2, 3 (Миры)
    round_idx: 1, 2 (Обычные/Элитные), 3 (Босс)
    """
    action_scale = 1.0 + ng_level * 0.25
    is_boss = (round_idx >= 3)

    # Уникальные элитные враги 3-го мира перед финальным боссом
    if stage == 3 and not is_boss:
        elite_pool = [
            {
                "name": "ЭЛИТА: Костяной Страж с Топором",
                "role": "Огр",  # Переиспользуем замах Огра для тяжелого топора
                "hp": 130,
                "actions": [
                    {"type": "Атака", "name": "Казнящий замах", "effects": [{"type": "damage", "value": 18}]},
                    {"type": "Защита", "name": "Тяжелый доспех стражи", "effects": [{"type": "block", "value": 15}]}
                ]
            },
            {
                "name": "ЭЛИТА: Чёрный Скелет-Маг",
                "role": "Злой Волшебник",  # Переиспользуем анимацию каста мага
                "hp": 110,
                "actions": [
                    {"type": "Заклинание", "name": "Стрела Бездны", "effects": [{"type": "damage", "value": 14}]},
                    {"type": "Заклинание", "name": "Проклятие увядания",
                     "effects": [{"type": "damage", "value": 8}, {"type": "steal_stamina", "value": 1}]}
                ]
            }
        ]
        chosen = random.choice(elite_pool)
        actions = [EnemyAction(a["type"], a["name"], build_effects(a.get("effects", [])), scale=action_scale) for a in
                   chosen["actions"]]
        return Enemy(chosen["name"], chosen["role"], chosen["hp"], is_boss=False, actions=actions, ng_level=ng_level)

    # Чтение стандартных пулов из JSON
    path = os.path.join("data", "enemies.json")
    with open(path, "r", encoding="utf-8") as f:
        pool_data = json.load(f)

    if not is_boss:
        # Мир 1: слабые враги, Мир 2: сильные враги
        sub_pool = pool_data["regular"]
        if stage == 1:
            candidates = [e for e in sub_pool if e["role"] in ("Гоблин", "Скелет", "Слизняк", "Вор")]
        else:
            candidates = [e for e in sub_pool if e["role"] in ("Огр", "Скелет-стрелок", "Зомби", "Мумия")]

        # Защита от пустого пула
        if not candidates:
            candidates = sub_pool
        chosen = random.choice(candidates)
    else:
        # 3 Мир — гарантированный Секретный Тёмный Рыцарь, 1 и 2 миры — обычные боссы
        if stage == 3:
            chosen = pool_data.get("rare_bosses", pool_data["bosses"])[0]
        else:
            chosen = random.choice(pool_data["bosses"])

    # Дополнительное усиление босса 2-го мира
    hp_multiplier = 1.25 if (is_boss and stage == 2) else 1.0
    final_hp = int(chosen["hp"] * hp_multiplier)

    actions = []
    for act in chosen.get("actions", []):
        act_scale = action_scale * (1.15 if (is_boss and stage == 2) else 1.0)
        actions.append(EnemyAction(act["type"], act["name"], build_effects(act.get("effects", [])), scale=act_scale))

    return Enemy(chosen["name"], chosen["role"], final_hp, is_boss=is_boss, actions=actions, ng_level=ng_level)


def draw_enemy_sprite(role: str, cx: float, cy: float, s: float, d: int, b: float, t: float, state: str = "idle", prog: float = 0.0):
    """Рисует детализированную дарк-фэнтези фигурку врага с уникальной анимацией."""
    atk = prog if state == "casting" else 0.0

    if role == "Гоблин":
        arcade.draw_polygon_filled(((cx - 18 * s, cy - 34 * s), (cx + 18 * s, cy - 34 * s), (cx + 8 * d * s, cy + 12 * s)), (58, 42, 30))
        arcade.draw_circle_filled(cx + 4 * d * s, cy + 16 * s, 14 * s, (72, 92, 46))
        arcade.draw_polygon_filled(((cx - 10 * s, cy + 18 * s), (cx - 28 * s, cy + 26 * s), (cx - 10 * s, cy + 10 * s)), (72, 92, 46))
        arcade.draw_polygon_filled(((cx + 12 * s, cy + 18 * s), (cx + 28 * s, cy + 26 * s), (cx + 12 * s, cy + 10 * s)), (72, 92, 46))
        arcade.draw_circle_filled(cx + 8 * d * s, cy + 18 * s, 3 * s, (220, 180, 40))
        thrust = atk * 32 * d * s
        arcade.draw_line(cx + 14 * d * s + thrust, cy - 8 * s, cx + 38 * d * s + thrust, cy - 2 * s, (180, 185, 190), 4)

    elif role == "Огр":
        arcade.draw_rect_filled(arcade.XYWH(cx, cy - 4 * s, 56 * s, 58 * s), (68, 74, 52))
        arcade.draw_rect_filled(arcade.XYWH(cx, cy - 22 * s, 56 * s, 20 * s), (65, 38, 24))
        arcade.draw_circle_filled(cx, cy + 32 * s, 18 * s, (82, 90, 62))
        arcade.draw_polygon_filled(((cx + 8 * d * s, cy + 24 * s), (cx + 11 * d * s, cy + 31 * s), (cx + 14 * d * s, cy + 24 * s)), (215, 205, 180))
        arcade.draw_circle_filled(cx + 7 * d * s, cy + 35 * s, 3.5 * s, (200, 40, 40))
        club_tip_y = (34 - atk * 55) * s
        club_tip_x = (36 + atk * 26) * d * s
        arcade.draw_line(cx + 24 * d * s, cy - 8 * s, cx + club_tip_x, cy + club_tip_y, (74, 48, 28), 10)

    elif role == "Скелет":
        arcade.draw_rect_filled(arcade.XYWH(cx, cy - 8 * s, 22 * s, 38 * s), (195, 188, 170))
        for ry in (-16, -8, 0):
            arcade.draw_line(cx - 12 * s, cy + ry * s, cx + 12 * s, cy + ry * s, (120, 115, 105), 3)
        arcade.draw_circle_filled(cx, cy + 24 * s, 14 * s, (205, 198, 180))
        arcade.draw_arc_filled(cx, cy + 26 * s, 30 * s, 26 * s, (65, 70, 78), 0, 180)
        arcade.draw_circle_filled(cx + 5 * d * s, cy + 23 * s, 3 * s, (90, 200, 210))
        sword_y = (26 - atk * 42) * s
        arcade.draw_line(cx + 16 * d * s, cy - 8 * s, cx + (34 + atk * 18) * d * s, cy + sword_y, (175, 180, 185), 4)

    elif role == "Скелет-стрелок":
        arcade.draw_rect_filled(arcade.XYWH(cx, cy - 8 * s, 22 * s, 38 * s), (190, 182, 165))
        arcade.draw_circle_filled(cx, cy + 24 * s, 14 * s, (200, 192, 175))
        arcade.draw_polygon_filled(((cx - 16 * s, cy + 22 * s), (cx + 16 * s, cy + 22 * s), (cx - 4 * d * s, cy + 44 * s)), (32, 48, 36))
        arcade.draw_circle_filled(cx + 6 * d * s, cy + 23 * s, 3 * s, (110, 220, 130))
        bow_x = cx + 18 * d * s
        arcade.draw_arc_outline(bow_x, cy, 24 * s, 54 * s, (92, 58, 32), -90 if d > 0 else 90, 90 if d > 0 else 270, 4)
        pull = -atk * 14 * d * s
        arcade.draw_line(bow_x, cy + 26 * s, bow_x + pull, cy, (180, 175, 160), 2)
        arcade.draw_line(bow_x, cy - 26 * s, bow_x + pull, cy, (180, 175, 160), 2)

    elif role == "Слизняк":
        stretch_x = atk * 26 * s
        stretch_y = -atk * 12 * s
        wobble = math.sin(t * 6.0) * 5 * s + stretch_x
        arcade.draw_ellipse_filled(cx + atk * 15 * d * s, cy - 14 * s, 68 * s + wobble, 48 * s + stretch_y, (42, 138, 66, 220))
        arcade.draw_ellipse_outline(cx + atk * 15 * d * s, cy - 14 * s, 68 * s + wobble, 48 * s + stretch_y, (110, 190, 95), 3)
        arcade.draw_circle_filled(cx - 6 * d * s, cy - 16 * s, 9 * s, (185, 180, 160))
        arcade.draw_circle_filled(cx + 12 * d * s, cy - 4 * s, 4 * s, (210, 220, 70))

    elif role == "Зомби":
        arcade.draw_rect_filled(arcade.XYWH(cx, cy - 8 * s, 30 * s, 42 * s), (48, 52, 58))
        arcade.draw_circle_filled(cx + 4 * d * s, cy + 22 * s, 14 * s, (76, 108, 82))
        arcade.draw_circle_filled(cx + 8 * d * s, cy + 24 * s, 3 * s, (210, 190, 70))
        reach = atk * 28 * d * s
        arcade.draw_line(cx, cy + 4 * s, cx + 30 * d * s + reach, cy + 10 * s + b, (76, 108, 82), 6)
        arcade.draw_line(cx, cy - 4 * s, cx + 28 * d * s + reach, cy + 2 * s - b, (64, 92, 70), 6)

    elif role == "Вор":
        alpha = int(255 * (1.0 - atk * 0.6))
        arcade.draw_polygon_filled(((cx - 20 * s, cy - 36 * s), (cx + 20 * s, cy - 36 * s), (cx, cy + 18 * s)), (24, 24, 30, alpha))
        arcade.draw_circle_filled(cx, cy + 22 * s, 13 * s, (35, 35, 42, alpha))
        arcade.draw_rect_filled(arcade.XYWH(cx + 5 * d * s, cy + 22 * s, 12 * s, 4 * s), (195, 155, 55))
        dagger_x = (34 + atk * 30) * d * s
        arcade.draw_line(cx + 16 * d * s, cy - 8 * s, cx + dagger_x, cy + 4 * s, (165, 175, 180), 3)

    elif role == "Мумия":
        arcade.draw_rect_filled(arcade.XYWH(cx, cy - 8 * s, 30 * s, 44 * s), (176, 160, 125))
        for by in range(-26, 20, 8):
            arcade.draw_line(cx - 15 * s, cy + by * s, cx + 15 * s, cy + (by + 3) * s, (125, 110, 82), 3)
        arcade.draw_circle_filled(cx, cy + 24 * s, 14 * s, (176, 160, 125))
        arcade.draw_circle_filled(cx + 6 * d * s, cy + 25 * s, 3 * s, (80, 210, 195))
        if atk > 0:
            arcade.draw_line(cx + 14 * d * s, cy + 6 * s, cx + (25 + atk * 55) * d * s, cy + 14 * s, (195, 180, 145), 4)

    elif role == "Некромант":
        hover = math.sin(t * 4.0) * 5 * s + atk * 14 * s
        arcade.draw_polygon_filled(((cx - 28 * s, cy - 38 * s + hover), (cx + 28 * s, cy - 38 * s + hover), (cx, cy + 22 * s + hover)), (44, 24, 62))
        arcade.draw_circle_filled(cx, cy + 24 * s + hover, 14 * s, (195, 188, 172))
        arcade.draw_polygon_filled(((cx - 15 * s, cy + 36 * s + hover), (cx + 15 * s, cy + 36 * s + hover), (cx, cy + 56 * s + hover)), (85, 30, 105))
        sx = cx + 25 * d * s + atk * 15 * d * s
        arcade.draw_line(sx, cy - 36 * s + hover, sx, cy + 40 * s + hover, (28, 24, 32), 4)
        arcade.draw_circle_filled(sx, cy + 42 * s + hover, (10 + atk * 8) * s, (70, 210, 120))

    elif role == "Костяной Гигант":
        slam_y = -atk * 18 * s
        arcade.draw_rect_filled(arcade.XYWH(cx, cy - 2 * s + slam_y, 64 * s, 68 * s), (188, 180, 162))
        arcade.draw_rect_outline(arcade.XYWH(cx, cy - 2 * s + slam_y, 64 * s, 68 * s), (95, 90, 82), 3)
        arcade.draw_circle_filled(cx, cy + 38 * s + slam_y, 20 * s, (196, 188, 170))
        arcade.draw_circle_filled(cx + 8 * d * s, cy + 40 * s + slam_y, 5 * s, (215, 45, 45))
        arcade.draw_circle_filled(cx - 38 * s, cy + 16 * s + b + slam_y, 18 * s, (145, 138, 125))
        arcade.draw_circle_filled(cx + 38 * s, cy + 16 * s + b + slam_y, 18 * s, (145, 138, 125))

    elif role == "Злой Волшебник":
        arcade.draw_polygon_filled(((cx - 25 * s, cy - 40 * s), (cx + 25 * s, cy - 40 * s), (cx, cy + 20 * s)), (78, 20, 56))
        arcade.draw_circle_filled(cx, cy + 24 * s, 14 * s, (165, 160, 168))
        arcade.draw_polygon_filled(((cx - 25 * s, cy + 32 * s), (cx + 25 * s, cy + 32 * s), (cx, cy + 68 * s)), (24, 20, 30))
        sx = cx + 25 * d * s
        arcade.draw_line(sx, cy - 40 * s, sx, cy + 38 * s, (168, 134, 62), 4)
        orb_r = (10 + math.sin(t * 7) * 2.5 + atk * 10) * s
        arcade.draw_circle_filled(sx, cy + 42 * s, orb_r, (175, 45, 155))

    elif role == "Тёмный Рыцарь":
        # Черный плащ властелина за спиной
        cape_wave = math.sin(t * 4.0) * 5 * s
        arcade.draw_polygon_filled(
            ((cx - 14 * d * s, cy + 20 * s), (cx - 38 * d * s + cape_wave, cy - 46 * s), (cx + 18 * d * s, cy - 44 * s)),
            (18, 16, 22)
        )

        # Ноги и готически заостренная броня
        arcade.draw_rect_filled(arcade.XYWH(cx - 10 * s, cy - 34 * s, 11 * s, 24 * s), (48, 46, 52))
        arcade.draw_rect_filled(arcade.XYWH(cx + 10 * s, cy - 34 * s, 11 * s, 24 * s), (48, 46, 52))

        # Массивная ребристая кираса
        arcade.draw_polygon_filled(
            ((cx - 22 * s, cy + 16 * s), (cx + 22 * s, cy + 16 * s), (cx + 15 * s, cy - 22 * s), (cx - 15 * s, cy - 22 * s)),
            (58, 55, 62)
        )
        arcade.draw_polygon_outline(
            ((cx - 22 * s, cy + 16 * s), (cx + 22 * s, cy + 16 * s), (cx + 15 * s, cy - 22 * s), (cx - 15 * s, cy - 22 * s)),
            (145, 140, 150), 2
        )

        # Острые шипастые наплечники
        for side in (-1, 1):
            px = cx + side * 24 * s
            py = cy + 14 * s + b * 0.5
            arcade.draw_polygon_filled(((px - 10 * s, py - 6 * s), (px + 10 * s, py - 6 * s), (px + side * 18 * s, py + 16 * s)), (95, 92, 102))
            arcade.draw_polygon_filled(((px - 6 * s, py), (px + 6 * s, py), (px + side * 12 * s, py + 24 * s)), (135, 130, 140))

        # Шлем с высокими острыми коронами-рогами
        hy = cy + 32 * s
        arcade.draw_ellipse_filled(cx, hy, 24 * s, 30 * s, (68, 65, 74))
        # Три острых шпиля на шлеме
        arcade.draw_polygon_filled(((cx - 10 * s, hy + 10 * s), (cx - 4 * s, hy + 10 * s), (cx - 9 * s, hy + 34 * s)), (125, 120, 130))
        arcade.draw_polygon_filled(((cx + 4 * s, hy + 10 * s), (cx + 10 * s, hy + 10 * s), (cx + 9 * s, hy + 34 * s)), (125, 120, 130))
        arcade.draw_polygon_filled(((cx - 5 * s, hy + 12 * s), (cx + 5 * s, hy + 12 * s), (cx, hy + 42 * s)), (155, 150, 160))
        # Узкие прорези глаз с тлеющим светом
        arcade.draw_circle_filled(cx + 5 * d * s, hy + 2 * s, 2.5 * s, (235, 110, 30))

        # Длинный зубчатый меч в одной руке (взмах при атаке)
        sword_x = cx - 24 * d * s
        sword_tip_x = sword_x - (22 - atk * 35) * d * s
        sword_tip_y = cy - (34 - atk * 45) * s
        arcade.draw_line(sword_x, cy - 4 * s, sword_tip_x, sword_tip_y, (185, 185, 195), 5)

        # Пылающая огненная булава в другой руке
        mace_x = cx + (28 + atk * 26) * d * s
        mace_y = cy - (10 - atk * 18) * s
        arcade.draw_line(cx + 16 * d * s, cy - 4 * s, mace_x, mace_y, (65, 50, 42), 5)
        fire_pulse = math.sin(t * 9.0) * 4 * s + atk * 10 * s
        arcade.draw_circle_filled(mace_x, mace_y, 18 * s + fire_pulse, (235, 95, 20, 140))
        arcade.draw_circle_filled(mace_x, mace_y, 12 * s, (255, 155, 30))
        arcade.draw_circle_filled(mace_x, mace_y, 6 * s, (255, 235, 140))

    elif role == "Скелет-Палач":
        # Массивный скелет в капюшоне палача с огромной секирой
        arcade.draw_rect_filled(arcade.XYWH(cx, cy - 6 * s, 34 * s, 48 * s), (195, 188, 170))
        for ry in (-18, -8, 2):
            arcade.draw_line(cx - 17 * s, cy + ry * s, cx + 17 * s, cy + ry * s, (95, 90, 82), 3)
        arcade.draw_circle_filled(cx, cy + 28 * s, 16 * s, (205, 198, 180))
        arcade.draw_polygon_filled(((cx - 20 * s, cy + 24 * s), (cx + 20 * s, cy + 24 * s), (cx, cy + 50 * s)), (28, 24, 30))
        arcade.draw_circle_filled(cx + 6 * d * s, cy + 28 * s, 3.5 * s, (220, 50, 50))
        # Огромная двусторонняя секира
        ax_x = cx + (28 + atk * 26) * d * s
        ax_y = cy + (26 - atk * 48) * s
        arcade.draw_line(cx + 18 * d * s, cy - 22 * s, ax_x, ax_y, (72, 46, 28), 6)
        arcade.draw_ellipse_filled(ax_x, ax_y, 32 * s, 20 * s, (165, 170, 180))
        arcade.draw_ellipse_outline(ax_x, ax_y, 32 * s, 20 * s, BORDER_GOLD, 2)

    elif role == "Скелет-Маг":
        # Скелет-чернокнижник в рваной багровой мантии с некро-посохом
        arcade.draw_polygon_filled(((cx - 24 * s, cy - 38 * s), (cx + 24 * s, cy - 38 * s), (cx, cy + 18 * s)), (75, 22, 34))
        arcade.draw_circle_filled(cx, cy + 24 * s, 14 * s, (198, 190, 172))
        arcade.draw_circle_filled(cx + 5 * d * s, cy + 25 * s, 3 * s, (165, 65, 225))
        # Посох с фиолетовым кристаллом
        sx = cx + 22 * d * s
        arcade.draw_line(sx, cy - 38 * s, sx, cy + 36 * s, (45, 35, 50), 4)
        orb_r = (9 + math.sin(t * 7.0) * 2.5 + atk * 8) * s
        arcade.draw_circle_filled(sx, cy + 40 * s, orb_r, (155, 55, 220))


    else:  # Цербер
        lunge = atk * 35 * d * s
        arcade.draw_ellipse_filled(cx + lunge, cy - 10 * s, 68 * s, 42 * s, (92, 22, 22))
        arcade.draw_ellipse_outline(cx + lunge, cy - 10 * s, 68 * s, 42 * s, (185, 75, 35), 2)
        for hy, hx in ((24, 18), (12, 28), (33, 8)):
            head_x = cx + hx * d * s + lunge
            head_y = cy + hy * s
            arcade.draw_circle_filled(head_x, head_y, 12 * s, (125, 30, 30))
            arcade.draw_circle_filled(head_x + 4 * d * s, head_y + 2 * s, 2.5 * s, (235, 175, 45))
