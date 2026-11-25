import arcade
from config import SCREEN_WIDTH, PANEL_DARK, PANEL_ENEMY, BORDER_GOLD, TEXT_PARCHMENT, TEXT_MUTED
from visuals.ui.icons import draw_card_icon, draw_stat_icon


class BattleHudRenderer:
    """Отвечает за отрисовку всего HUD боя: панелей статов, кнопок и усилений."""

    def __init__(self, view):
        self.v = view

    def draw(self):
        self._draw_hero_panel()
        self._draw_enemy_panel()
        self._draw_top_header()
        self._draw_bottom_controls()

    def _draw_hero_panel(self):
        hero = self.v.hero
        ui = self.v.ui_text

        arcade.draw_rect_filled(arcade.XYWH(195, 910, 310, 210), PANEL_DARK)
        arcade.draw_rect_outline(arcade.XYWH(195, 910, 310, 210), BORDER_GOLD, 2)
        ui.draw(hero.name, 195, 975, TEXT_PARCHMENT, 22, bold=True, anchor_x="center")

        draw_stat_icon("hp", 95, 938, size=11)
        ui.draw(f"HP: {hero.hp} / {hero.max_hp}", 118, 932, (115, 185, 130), 17)

        draw_stat_icon("block", 95, 901, size=11)
        ui.draw(f"Броня: {hero.block}", 118, 895, (110, 160, 205), 17)

        draw_stat_icon("stamina", 95, 859, size=11)
        ui.draw(f"Стамина: {hero.stamina} / {hero.max_stamina}", 118, 852, BORDER_GOLD, 19, bold=True)

    def _draw_enemy_panel(self):
        enemy = self.v.enemy
        if not enemy:
            return
        ui = self.v.ui_text

        ex_panel, ey_panel = SCREEN_WIDTH - 230, 895
        pw, ph = 390, 250
        if enemy.is_boss:
            arcade.draw_rect_filled(arcade.XYWH(ex_panel, ey_panel, pw, ph), (26, 12, 18))
            arcade.draw_rect_outline(arcade.XYWH(ex_panel, ey_panel, pw, ph), (175, 42, 48), 3.5)
            arcade.draw_rect_outline(arcade.XYWH(ex_panel, ey_panel, pw - 12, ph - 12), BORDER_GOLD, 1.5)
            for dx in (-pw / 2 + 8, pw / 2 - 8):
                for dy in (-ph / 2 + 8, ph / 2 - 8):
                    arcade.draw_circle_filled(ex_panel + dx, ey_panel + dy, 4, BORDER_GOLD)
        else:
            arcade.draw_rect_filled(arcade.XYWH(ex_panel, ey_panel, pw, ph), PANEL_ENEMY)
            arcade.draw_rect_outline(arcade.XYWH(ex_panel, ey_panel, pw, ph), (140, 42, 46), 2.5)

        name_color = BORDER_GOLD if enemy.is_boss else TEXT_PARCHMENT
        ui.draw(enemy.name, ex_panel, ey_panel + 82, name_color, 17, bold=True, width=pw - 36, align="center", anchor_x="center", anchor_y="center", multiline=True)

        draw_stat_icon("hp", ex_panel - 135, ey_panel + 38, size=10)
        ui.draw(f"{enemy.hp}/{enemy.max_hp}", ex_panel - 116, ey_panel + 32, (215, 110, 105), 16, bold=True)

        draw_stat_icon("block", ex_panel + 25, ey_panel + 38, size=10)
        ui.draw(f"Броня: {enemy.block}", ex_panel + 44, ey_panel + 32, (110, 160, 205), 16)

        ui.draw("Намерение: ??? (Скрыто)", ex_panel, ey_panel - 4, TEXT_MUTED, 15, bold=True, anchor_x="center")
        ui.draw(f"Прошлый ход:\n{enemy.last_action_text}", ex_panel, ey_panel - 65, TEXT_PARCHMENT, 13, width=pw - 40, align="center", anchor_x="center", anchor_y="center", multiline=True)

    def _draw_top_header(self):
        run = self.v.run
        ng_badge = f" [НГ+{run.ng_level}]" if run.ng_level > 0 else ""
        round_str = "БОСС ЛОКАЦИИ" if run.round_idx == 3 else f"Раунд {run.round_idx} из 3"
        self.v.ui_text.draw(
            f"{run.location_title}{ng_badge}  •  {round_str}  •  Ход {run.total_turns}",
            SCREEN_WIDTH / 2, 1020, BORDER_GOLD, 21, bold=True, anchor_x="center"
        )

    def _draw_bottom_controls(self):
        ui = self.v.ui_text
        hero = self.v.hero

        # Увеличенная подложка нижней панели игрока (от y=20 до y=365)
        arcade.draw_rect_filled(arcade.XYWH(SCREEN_WIDTH / 2, 192, 1850, 345), (16, 15, 21, 195))
        arcade.draw_rect_outline(arcade.XYWH(SCREEN_WIDTH / 2, 192, 1850, 345), (55, 48, 42, 150), 1.5)

        # Интерактивная кнопка Колоды
        dx, dy, dw, dh = self.v.deck_btn_rect
        d_bg = (36, 33, 46) if self.v.deck_hovered else PANEL_DARK
        d_border = arcade.color.YELLOW if self.v.deck_hovered else (95, 80, 62)
        arcade.draw_rect_filled(arcade.XYWH(dx, dy, dw, dh), d_bg)
        arcade.draw_rect_outline(arcade.XYWH(dx, dy, dw, dh), d_border, 2.5 if self.v.deck_hovered else 1.5)
        draw_stat_icon("deck", 112, dy, size=12, angle=self.v.deck_anim_time)
        ui.draw(f"Колода: {len(hero.draw_pile)}", 138, dy - 6, TEXT_PARCHMENT, 17, bold=True)

        # Интерактивная кнопка Сброса
        sx, sy, sw, sh = self.v.discard_btn_rect
        s_bg = (36, 33, 46) if self.v.discard_hovered else PANEL_DARK
        s_border = arcade.color.YELLOW if self.v.discard_hovered else (95, 80, 62)
        arcade.draw_rect_filled(arcade.XYWH(sx, sy, sw, sh), s_bg)
        arcade.draw_rect_outline(arcade.XYWH(sx, sy, sw, sh), s_border, 2.5 if self.v.discard_hovered else 1.5)
        draw_stat_icon("discard", 112, sy, size=12, angle=self.v.discard_anim_time)
        ui.draw(f"Сброс: {len(hero.discard_pile)}", 138, sy - 6, TEXT_PARCHMENT if self.v.discard_hovered else TEXT_MUTED, 17, bold=self.v.discard_hovered)

        self._draw_active_bonuses()

        # Кнопка завершения хода
        if self.v.substate == "FIGHT":
            bx, by, bw, bh = self.v.end_turn_btn
            btn_bg = (145, 56, 42) if self.v.end_turn_hovered else (110, 42, 32)
            btn_border = arcade.color.YELLOW if self.v.end_turn_hovered else BORDER_GOLD
            arcade.draw_rect_filled(arcade.XYWH(bx, by, bw, bh), btn_bg)
            arcade.draw_rect_outline(arcade.XYWH(bx, by, bw, bh), btn_border, 3.5 if self.v.end_turn_hovered else 2.0)
            draw_stat_icon("end_turn", bx - 78, by, size=12, angle=self.v.hourglass_angle)
            ui.draw("Закончить ход", bx + 14, by, TEXT_PARCHMENT, 17, bold=True, anchor_x="center", anchor_y="center")

        ui.draw(self.v.message, SCREEN_WIDTH / 2, 385, BORDER_GOLD, 18, bold=True, anchor_x="center")

    def get_active_bonus_items(self) -> list[tuple[str, str, str]]:
        """Возвращает список (тип_иконки, бейдж, полное_описание) для всех активных баффов похода."""
        b = self.v.run.bonuses
        items = []
        if b.get("max_hp", 0) > 0:
            items.append(("Защита", f"+{b['max_hp']} HP", f"Закалка плоти: максимальное здоровье увеличено на +{b['max_hp']} ед."))
        if b.get("neutral_damage", 0) > 0:
            items.append(("Атака", f"Н+{b['neutral_damage']}", f"Нейтральная атака: урон всех нейтральных атак увеличен на +{b['neutral_damage']}."))
        if b.get("hero_damage", 0) > 0:
            items.append(("Атака", f"Г+{b['hero_damage']}", f"Мастерство героя: урон всех классовых атак увеличен на +{b['hero_damage']}."))
        if b.get("neutral_heal", 0) > 0:
            items.append(("Исцеление", f"Н+{b['neutral_heal']}", f"Нейтральное лечение: исцеление нейтральных карт увеличено на +{b['neutral_heal']}."))
        if b.get("hero_heal", 0) > 0:
            items.append(("Исцеление", f"Г+{b['hero_heal']}", f"Мастерство героя: исцеление классовых карт увеличено на +{b['hero_heal']}."))
        if b.get("neutral_block", 0) > 0:
            items.append(("Защита", f"Н+{b['neutral_block']}", f"Нейтральная защита: броня нейтральных карт увеличена на +{b['neutral_block']}."))
        if b.get("hero_block", 0) > 0:
            items.append(("Защита", f"Г+{b['hero_block']}", f"Мастерство героя: броня классовых карт увеличена на +{b['hero_block']}."))
        return items

    def _draw_active_bonuses(self):
        items = self.get_active_bonus_items()
        if not items:
            return

        ui = self.v.ui_text
        ui.draw("УСИЛЕНИЯ ПОХОДА:", 80, 325, TEXT_MUTED, 12, bold=True)
        for i, (icon_type, badge, _) in enumerate(items[:4]):
            bx = 108 + i * 64
            by = 282
            arcade.draw_circle_filled(bx, by, 20, PANEL_DARK)
            arcade.draw_circle_outline(bx, by, 20, BORDER_GOLD, 1.5)
            draw_card_icon(icon_type, bx, by, size=14)
            ui.draw(badge, bx, by - 33, BORDER_GOLD, 11, bold=True, anchor_x="center")

        if self.v.hovered_bonus_desc:
            arcade.draw_rect_filled(arcade.XYWH(285, 385, 420, 48), (18, 16, 24, 245))
            arcade.draw_rect_outline(arcade.XYWH(285, 385, 420, 48), BORDER_GOLD, 1.5)
            ui.draw(self.v.hovered_bonus_desc, 285, 385, TEXT_PARCHMENT, 12, width=400, align="center", anchor_x="center", anchor_y="center", multiline=True)
