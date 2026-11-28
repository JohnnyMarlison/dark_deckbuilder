import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT, PANEL_DARK, BORDER_GOLD, TEXT_PARCHMENT, TEXT_MUTED
from visuals.ui.icons import draw_stat_icon, draw_hourglass_icon, draw_pile_icon


class BattleHUD:
    """Отрисовка интерфейса боя: верхняя плашка, числовые статы, статус по центру и кнопки."""

    def __init__(self, view):
        self.v = view

    def draw(self):
        ui = self.v.ui_text
        hero = self.v.hero
        enemy = self.v.enemy
        run = self.v.run

        # 1. Верхняя информационная панель этапа
        arcade.draw_rect_filled(arcade.XYWH(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 30, SCREEN_WIDTH, 60), (16, 15, 22, 235))
        arcade.draw_line(0, SCREEN_HEIGHT - 60, SCREEN_WIDTH, SCREEN_HEIGHT - 60, BORDER_GOLD, 2)

        stage_title = f"МИР {run.stage}: {run.current_location_name.upper()}  |  РАУНД {run.round_idx}/3"
        if getattr(run, "ng_level", 0) > 0:
            stage_title += f"  [НГ+{run.ng_level}]"
        ui.draw(stage_title, 42, SCREEN_HEIGHT - 30, BORDER_GOLD, 19, bold=True, anchor_y="center")

        # 2. Карточка характеристик Героя (числовые метрики с иконками)
        px, py, pw, ph = 265, SCREEN_HEIGHT - 148, 450, 125
        arcade.draw_rect_filled(arcade.XYWH(px, py, pw, ph), PANEL_DARK)
        arcade.draw_rect_outline(arcade.XYWH(px, py, pw, ph), BORDER_GOLD, 2)

        ui.draw(hero.name.upper(), px - pw / 2 + 22, py + 34, BORDER_GOLD, 20, bold=True, anchor_y="center")

        row_y = py - 14
        draw_stat_icon("hp", px - pw / 2 + 30, row_y, size=14)
        ui.draw(f"{hero.hp}/{hero.max_hp}", px - pw / 2 + 52, row_y, (235, 95, 85), 18, bold=True, anchor_y="center")

        draw_stat_icon("block", px - 35, row_y, size=14)
        ui.draw(f"{hero.block}", px - 13, row_y, (115, 175, 225), 18, bold=True, anchor_y="center")

        draw_stat_icon("stamina", px + 55, row_y, size=14)
        ui.draw(f"{hero.stamina}/{hero.max_stamina}", px + 78, row_y, BORDER_GOLD, 18, bold=True, anchor_y="center")

        # 3. Карточка характеристик Врага (адаптивная ширина и высота с динамическими отступами)
        if enemy:
            intent = getattr(enemy, "planned_action", None)
            if enemy.is_boss:
                intent_txt = "Намерение: ??? (Скрыто)"
                intent_col = TEXT_MUTED
            else:
                intent_txt = f"Намерение: [{intent.action_type}] {intent.desc}" if intent else "Намерение: Выжидает"
                intent_col = (235, 195, 120)

            last_txt = getattr(enemy, "last_action_text", "") or "Прошлый ход: —"

            est_name_w = len(enemy.name) * 12.2 + 96
            enemy_w = max(475, min(700, est_name_w))
            inner_w = enemy_w - 44

            # Оцениваем количество строк намерения и прошлого хода для динамической высоты карточки
            chars_per_line = max(24, int(inner_w / 8.2))
            intent_lines = max(1, (len(intent_txt) + chars_per_line - 1) // chars_per_line)
            last_lines = max(1, (len(last_txt) + chars_per_line - 1) // chars_per_line)

            intent_block_h = intent_lines * 21
            last_block_h = last_lines * 19
            enemy_h = 116 + intent_block_h + last_block_h
            enemy_x = SCREEN_WIDTH - 28 - enemy_w / 2
            enemy_y = SCREEN_HEIGHT - 78 - enemy_h / 2

            if enemy.is_boss:
                arcade.draw_rect_filled(arcade.XYWH(enemy_x, enemy_y, enemy_w, enemy_h), (26, 12, 18, 245))
                arcade.draw_rect_outline(arcade.XYWH(enemy_x, enemy_y, enemy_w, enemy_h), (215, 48, 54), 3.5)
                arcade.draw_rect_outline(arcade.XYWH(enemy_x, enemy_y, enemy_w - 10, enemy_h - 10), BORDER_GOLD, 1.5)
                for dx in (-enemy_w / 2 + 8, enemy_w / 2 - 8):
                    for dy in (-enemy_h / 2 + 8, enemy_h / 2 - 8):
                        arcade.draw_circle_filled(enemy_x + dx, enemy_y + dy, 3.8, BORDER_GOLD)
            else:
                arcade.draw_rect_filled(arcade.XYWH(enemy_x, enemy_y, enemy_w, enemy_h), PANEL_DARK)
                arcade.draw_rect_outline(arcade.XYWH(enemy_x, enemy_y, enemy_w, enemy_h), BORDER_GOLD, 2.0)

            top_y = enemy_y + enemy_h / 2
            name_col = (255, 215, 110) if enemy.is_boss else BORDER_GOLD
            ui.draw(enemy.name, enemy_x, top_y - 26, name_col, 18, bold=True, anchor_x="center", anchor_y="center")

            erow_y = top_y - 62
            draw_stat_icon("hp", enemy_x - 148, erow_y, size=13)
            ui.draw(f"HP: {enemy.hp}/{enemy.max_hp}", enemy_x - 128, erow_y, (235, 95, 85), 17, bold=True,
                    anchor_y="center")

            draw_stat_icon("block", enemy_x + 65, erow_y, size=13)
            ui.draw(f"Броня: {enemy.block}", enemy_x + 85, erow_y, (115, 175, 225), 17, bold=True, anchor_y="center")

            intent_y = erow_y - 24 - intent_block_h / 2
            ui.draw(intent_txt, enemy_x, intent_y, intent_col, 14, bold=True, width=inner_w, align="center",
                    anchor_x="center", anchor_y="center", multiline=True)

            last_y = intent_y - intent_block_h / 2 - 12 - last_block_h / 2
            ui.draw(last_txt, enemy_x, last_y, TEXT_MUTED, 13, width=inner_w, align="center", anchor_x="center",
                    anchor_y="center", multiline=True)

        # 4. Индикатор этапа и статуса хода — строго в зазоре между ареной и картами
        if self.v.message:
            msg_y = 398
            arcade.draw_rect_filled(arcade.XYWH(SCREEN_WIDTH / 2, msg_y, 760, 32), (18, 17, 24, 225))
            arcade.draw_rect_outline(arcade.XYWH(SCREEN_WIDTH / 2, msg_y, 760, 32), (85, 70, 52, 180), 1.2)
            ui.draw(self.v.message, SCREEN_WIDTH / 2, msg_y, TEXT_PARCHMENT, 16, bold=True, anchor_x="center", anchor_y="center")

        # 5. Кнопки стопок Колоды и Сброса (слева внизу, с разными анимированными иконками)
        for rect, is_hov, anim_t, title, count, is_disc in (
                (self.v.deck_btn, self.v.deck_hovered, self.v.deck_anim_time, "Колода", len(hero.draw_pile), False),
                (self.v.discard_btn, self.v.discard_hovered, self.v.discard_anim_time, "Сброс", len(hero.discard_pile), True),
        ):
            bx, by, bw, bh = rect
            bg = (36, 33, 46) if is_hov else (22, 20, 28)
            brd = arcade.color.YELLOW if is_hov else BORDER_GOLD
            arcade.draw_rect_filled(arcade.XYWH(bx, by, bw, bh), bg)
            arcade.draw_rect_outline(arcade.XYWH(bx, by, bw, bh), brd, 2.5 if is_hov else 1.8)
            draw_pile_icon(bx - bw / 2 + 28, by, anim_t, size=10.0, is_discard=is_disc)
            ui.draw(f"{title}: {count}", bx + 18, by, TEXT_PARCHMENT, 15, bold=True, anchor_x="center", anchor_y="center")

        # 6. Кнопка «Закончить ход» (справа внизу, с плавным увеличением при наведении)
        btn_x, btn_y, base_w, base_h = self.v.end_turn_btn
        sc = getattr(self.v, "end_turn_scale", 1.0)
        btn_w, btn_h = base_w * sc, base_h * sc

        can_end = (self.v.substate == "FIGHT" and not self.v.enemy_attack_pending and self.v.playing_widget is None)
        btn_bg = (128, 44, 38) if (self.v.end_turn_hovered and can_end) else ((96, 34, 30) if can_end else (42, 38, 44))
        btn_brd = arcade.color.YELLOW if (self.v.end_turn_hovered and can_end) else BORDER_GOLD

        arcade.draw_rect_filled(arcade.XYWH(btn_x, btn_y, btn_w, btn_h), btn_bg)
        arcade.draw_rect_outline(arcade.XYWH(btn_x, btn_y, btn_w, btn_h), btn_brd,
                                 2.8 if (self.v.end_turn_hovered and can_end) else 2)
        draw_hourglass_icon(btn_x - btn_w / 2 + 30 * sc, btn_y, self.v.hourglass_angle, size=13.0 * sc)
        ui.draw("Закончить ход", btn_x + 16 * sc, btn_y, TEXT_PARCHMENT, round(17 * sc), bold=True, anchor_x="center",
                anchor_y="center")

        self._draw_active_bonuses()

    _BONUS_META = {
        "max_hp": ("Защита", "+{v} HP", "Закалка плоти: максимальное здоровье увеличено на +{v} ед."),
        "damage": ("Атака", "+{v} Урон", "Заточка клинков: урон атакующих карт увеличен на +{v}."),
        "heal": ("Исцеление", "+{v} Хил", "Благословение жизни: лечение карт увеличено на +{v}."),
        "block": ("Защита", "+{v} Блок", "Укрепление брони: защита карт увеличена на +{v}."),
        "stamina": ("Заклинание", "+{v} Стам.", "Источник сил: максимальная стамина увеличена на +{v}."),
        "hero_damage": ("Атака", "+{v} Урон", "Мастерство героя: урон личных карт героя увеличен на +{v}."),
        "hero_heal": ("Исцеление", "+{v} Хил", "Мастерство героя: лечение личных карт героя увеличено на +{v}."),
        "hero_block": ("Защита", "+{v} Блок", "Мастерство героя: броня личных карт героя увеличена на +{v}."),
        "neutral_damage": ("Атака", "+{v} Урон", "Тайные знания: урон нейтральных карт увеличен на +{v}."),
        "neutral_heal": ("Исцеление", "+{v} Хил", "Тайные знания: лечение нейтральных карт увеличено на +{v}."),
        "neutral_block": ("Защита", "+{v} Блок", "Тайные знания: броня нейтральных карт увеличена на +{v}."),
    }

    @staticmethod
    def _humanize_bonus(key: str, val: int | float) -> tuple[str, str, str]:
        if key in BattleHUD._BONUS_META:
            icon_type, badge_tpl, desc_tpl = BattleHUD._BONUS_META[key]
            return icon_type, badge_tpl.format(v=val), desc_tpl.format(v=val)

        scope = "личных карт героя" if "hero" in key else ("нейтральных карт" if "neutral" in key else "всех карт")
        if "block" in key or "armor" in key:
            return "Защита", f"+{val} Блок", f"Укрепление защиты: броня {scope} увеличена на +{val}."
        if "heal" in key:
            return "Исцеление", f"+{val} Хил", f"Благословение жизни: лечение {scope} увеличено на +{val}."
        if "damage" in key or "dmg" in key:
            return "Атака", f"+{val} Урон", f"Боевая закалка: урон {scope} увеличен на +{val}."
        return "Заклинание", f"+{val}", f"Благословение похода: усиление {scope} на +{val}."

    def _draw_active_bonuses(self):
        from visuals.ui.icons import draw_card_icon

        bonuses = getattr(self.v.run, "bonuses", {}) or {}
        items: list[tuple[str, str, str]] = []
        for key, val in bonuses.items():
            if not isinstance(val, (int, float)) or val <= 0:
                continue
            items.append(self._humanize_bonus(key, val))

        self._hovered_bonus_desc = ""
        if not items:
            return

        ui = self.v.ui_text
        mx = getattr(self.v, "mouse_x", -1)
        my = getattr(self.v, "mouse_y", -1)

        rows = (len(items) + 2) // 3
        top_row_y = 262 + (rows - 1) * 78
        self._bonuses_top_y = top_row_y + 42

        ui.draw("УСИЛЕНИЯ ПОХОДА:", 28, self._bonuses_top_y, TEXT_MUTED, 11, bold=True, anchor_x="left")
        for i, (icon_type, badge, desc) in enumerate(items):
            col = i % 3
            row = i // 3
            bx = 58 + col * 74
            by = 262 + row * 78
            is_hov = (abs(mx - bx) <= 24 and abs(my - by) <= 24)
            if is_hov:
                self._hovered_bonus_desc = desc

            arcade.draw_circle_filled(bx, by, 20, (36, 33, 46) if is_hov else PANEL_DARK)
            arcade.draw_circle_outline(bx, by, 20, arcade.color.YELLOW if is_hov else BORDER_GOLD,
                                       2.2 if is_hov else 1.6)
            draw_card_icon(icon_type, bx, by, size=14)
            ui.draw(badge, bx, by - 36, BORDER_GOLD, 11, bold=True, anchor_x="center", anchor_y="center")

    def draw_tooltip(self):
        """Отрисовывает всплывающую подсказку усиления строго поверх карт и всех элементов боя."""
        desc = getattr(self, "_hovered_bonus_desc", "")
        if not desc:
            return
        arcade.draw_rect_filled(arcade.XYWH(225, 348, 396, 54), (18, 16, 24, 252))
        arcade.draw_rect_outline(arcade.XYWH(225, 348, 396, 54), BORDER_GOLD, 2.0)
        self.v.ui_text.draw(
            desc, 225, 348, TEXT_PARCHMENT, 12,
            width=370, align="center", anchor_x="center", anchor_y="center", multiline=True
        )