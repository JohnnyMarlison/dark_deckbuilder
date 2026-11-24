import random
import math
import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BG_DARK, PANEL_DARK, PANEL_ENEMY, BORDER_GOLD, TEXT_PARCHMENT, TEXT_MUTED
from core.run_state import RunState
from core.combat import CombatEngine
from core.effects import CombatEvent
from core.enemy import Enemy
from visuals.avatar import CharacterAvatar
from visuals.card_widget import CardWidget
from visuals.particles import SpellProjectile, FloatingEffect
from visuals.icons import draw_enemy_choice_icons, draw_card_icon
from visuals.locations import draw_location_background
from visuals.achievement_popup import AchievementToastManager
from visuals.icons import draw_enemy_choice_icons, draw_card_icon, draw_stat_icon
from visuals.text_cache import TextCache


class BattleView(arcade.View):
    def __init__(self, run: RunState):
        super().__init__()
        self.engine = CombatEngine(run)
        self.run = run
        self.hero = run.hero
        self.enemy: Enemy | None = None

        self.player_avatar: CharacterAvatar | None = None
        self.enemy_avatar: CharacterAvatar | None = None

        self.hand_widgets: list[CardWidget] = []
        self.playing_widget: CardWidget | None = None
        self.enemy_playing_widget: CardWidget | None = None
        self.play_timer = 0.0

        self.effects: list[FloatingEffect] = []
        self.projectiles: list[SpellProjectile] = []
        self.screen_shake = 0.0
        self.enemy_turn_timer = 0.0
        self.enemy_attack_pending = False

        self.substate = "FIGHT"  # FIGHT, BOSS_VICTORY, GAME_OVER
        self.message = ""
        self.hovered_bonus_desc = ""
        self.ui_text = TextCache()

        self.toast_manager = AchievementToastManager()
        self.end_turn_btn = (SCREEN_WIDTH - 190, 185, 240, 64)
        self.ng_continue_btn = (SCREEN_WIDTH / 2 - 190, 420, 330, 66)
        self.ng_exit_btn = (SCREEN_WIDTH / 2 + 190, 420, 330, 66)
        self.end_turn_hovered = False
        self.hourglass_angle = 0.0


    def on_show_view(self):
        arcade.set_background_color(BG_DARK)
        self._setup_stage()

    def _setup_stage(self):
        self.enemy = self.engine.setup_encounter()
        self.player_avatar = CharacterAvatar(self.hero.name, 610, 590, scale=1.75, flip=False)
        enemy_scale = 2.25 if self.enemy.role == "Тёмный Рыцарь" else (1.95 if self.enemy.is_boss else 1.75)
        self.enemy_avatar = CharacterAvatar(self.enemy.role, SCREEN_WIDTH - 610, 590, scale=enemy_scale, flip=True)

        self.hand_widgets.clear()
        self.playing_widget = None
        self.enemy_playing_widget = None
        self.effects.clear()
        self.projectiles.clear()
        self.enemy_attack_pending = False
        self.substate = "FIGHT"
        self._begin_player_turn()

    def _sync_hand_widgets(self):
        existing = {w.data: w for w in self.hand_widgets}
        new_widgets: list[CardWidget] = []
        for card in self.hero.hand:
            if card in existing:
                new_widgets.append(existing[card])
            else:
                new_widgets.append(CardWidget(card, x=120, y=410))
        self.hand_widgets = new_widgets

        count = len(self.hand_widgets)
        if count == 0:
            return

        # Динамический шаг: при 4 картах зазор между ними 35px, при 5 — 25px, при 6 — 15px
        spacing = 235 if count <= 4 else (225 if count == 5 else 215)
        total_w = (count - 1) * spacing
        start_x = SCREEN_WIDTH / 2 - total_w / 2
        for i, w in enumerate(self.hand_widgets):
            w.target_x = start_x + i * spacing
            w.target_y = 185


    def _begin_player_turn(self):
        events = self.engine.begin_player_turn()
        self._spawn_visuals_for_events(events)
        self._sync_hand_widgets()
        self.message = f"Этап {self.run.round_idx}/3 (Ход {self.run.total_turns}). Враг взвешивает свой ход..."

    def _spawn_visuals_for_events(self, events: list[CombatEvent]):
        px, ex = 610, SCREEN_WIDTH - 610
        for ev in events:
            if ev.kind == "damage":
                if ev.target == "enemy":
                    self.screen_shake = 0.2
                    if self.enemy_avatar:
                        self.enemy_avatar.trigger("hurt", 0.5)
                    txt = f"-{ev.value} HP" if ev.blocked == 0 else f"-{ev.value} (блок {ev.blocked})"
                    self.effects.append(FloatingEffect(ex, 650, txt, (220, 75, 45)))
                else:
                    if ev.value > 0:
                        self.screen_shake = 0.25
                        if self.player_avatar:
                            self.player_avatar.trigger("hurt", 0.55)
                        self.effects.append(FloatingEffect(px, 650, f"-{ev.value} HP", (215, 55, 55)))
                    else:
                        if self.player_avatar:
                            self.player_avatar.trigger("heal", 0.45)
                        self.effects.append(FloatingEffect(px, 650, f"Блок ({ev.blocked})", (110, 165, 210)))

            elif ev.kind == "block":
                tx = px if ev.target == "player" else ex
                av = self.player_avatar if ev.target == "player" else self.enemy_avatar
                if av:
                    av.trigger("heal", 0.45)
                self.effects.append(FloatingEffect(tx, 675, f"+{ev.value} Брони", (110, 165, 210)))

            elif ev.kind == "heal" and ev.value > 0:
                tx = px if ev.target == "player" else ex
                av = self.player_avatar if ev.target == "player" else self.enemy_avatar
                if av:
                    av.trigger("heal", 0.45)
                self.effects.append(FloatingEffect(tx, 630, f"+{ev.value} HP", (95, 195, 130)))

            elif ev.kind == "stamina":
                self.effects.append(FloatingEffect(px, 695, f"+{ev.value} Стамины", BORDER_GOLD))

            elif ev.kind == "steal_stamina":
                self.effects.append(FloatingEffect(px, 695, f"-{ev.value} Стамина", BORDER_GOLD))

    def _start_play_card(self, widget: CardWidget):
        if self.playing_widget or self.enemy_attack_pending or self.substate != "FIGHT":
            return
        card = widget.data
        if self.hero.stamina < card.cost:
            self.message = "Недостаточно стамины!"
            return

        self.hero.stamina -= card.cost
        self.hero.hand.remove(card)
        self._sync_hand_widgets()

        widget.is_playing = True
        widget.hovered = False
        widget.target_x = SCREEN_WIDTH / 2
        widget.target_y = 590
        self.playing_widget = widget
        self.play_timer = 0.35

        if self.player_avatar:
            self.player_avatar.trigger("casting", 0.45)

        if card.has_damage:
            color = BORDER_GOLD if card.card_type == "Атака" else (155, 65, 185)
            self.projectiles.append(SpellProjectile(635, 605, SCREEN_WIDTH - 625, 600, color, radius=16))

    def _resolve_player_card(self, widget: CardWidget):
        card = widget.data
        events, outcome = self.engine.play_player_card(card)
        self._sync_hand_widgets()
        self._spawn_visuals_for_events(events)
        self.message = f"Разыграно: {card.name}"

        if outcome != "CONTINUE":
            if self.player_avatar:
                self.player_avatar.trigger("victory", 2.5)
            if outcome == "STAGE_REWARD":
                from views.stage_reward_view import StageRewardView
                self.window.show_view(StageRewardView(self.run))
            elif outcome == "BOSS_REWARD":
                from views.boss_reward_view import BossRewardView
                self.window.show_view(BossRewardView(self.run, is_final_boss=False))
            elif outcome == "FINAL_VICTORY":
                self.substate = "BOSS_VICTORY"

    def _end_player_turn(self):
        if self.playing_widget or self.enemy_attack_pending or not self.enemy or self.substate != "FIGHT":
            return

        act = self.engine.end_player_turn()
        self._sync_hand_widgets()
        self.enemy_attack_pending = True
        self.enemy_turn_timer = 0.65

        if act:
            ew = CardWidget(act, x=SCREEN_WIDTH - 610, y=600, cost=0)
            ew.target_x = SCREEN_WIDTH / 2
            ew.target_y = 595
            ew.is_playing = True
            self.enemy_playing_widget = ew

        if self.enemy_avatar:
            self.enemy_avatar.trigger("casting", 0.6)
        if act and act.has_damage:
            color = (145, 50, 175) if act.action_type == "Заклинание" else (195, 55, 35)
            self.projectiles.append(SpellProjectile(SCREEN_WIDTH - 635, 605, 625, 600, color, radius=16))


    def _resolve_enemy_turn(self):
        self.enemy_playing_widget = None
        events, outcome = self.engine.resolve_enemy_turn()
        self._spawn_visuals_for_events(events)

        if outcome == "GAME_OVER":
            self.substate = "GAME_OVER"
            self.message = "Вы пали во тьме! [R] — заново | [ESC] — главное меню"
            return

        self._begin_player_turn()
        if self.enemy:
            self.message = f"Прошлый ход врага: {self.enemy.last_action_text}"


    def on_update(self, delta_time: float):
        if self.screen_shake > 0:
            self.screen_shake = max(0.0, self.screen_shake - delta_time)

        if self.player_avatar:
            self.player_avatar.update(delta_time)
        if self.enemy_avatar:
            self.enemy_avatar.update(delta_time)

        for w in self.hand_widgets:
            w.update(delta_time)

        if self.playing_widget:
            self.playing_widget.update(delta_time)
            self.play_timer -= delta_time
            if self.play_timer <= 0:
                finished = self.playing_widget
                finished.is_playing = False
                self.playing_widget = None
                self._resolve_player_card(finished)

        if self.enemy_playing_widget:
            self.enemy_playing_widget.update(delta_time)

        if self.enemy_attack_pending:
            self.enemy_turn_timer -= delta_time
            if self.enemy_turn_timer <= 0:
                self.enemy_attack_pending = False
                self._resolve_enemy_turn()

        self.projectiles = [p for p in self.projectiles if p.update(delta_time)]
        self.effects = [e for e in self.effects if e.update(delta_time)]
        self.toast_manager.update(delta_time)

        if self.end_turn_hovered and self.substate == "FIGHT":
            self.hourglass_angle = (self.hourglass_angle - delta_time * 1.8) % (math.pi * 2)
        else:
            self.hourglass_angle = 0.0

    def on_draw(self):
        self.clear()
        anim_time = self.player_avatar.time if self.player_avatar else 0.0
        draw_location_background(self.run.current_location_name, anim_time)

        shake_x = random.uniform(-6, 6) if self.screen_shake > 0 else 0
        shake_y = random.uniform(-6, 6) if self.screen_shake > 0 else 0

        # Поле битвы на переднем плане (y = 505)
        arcade.draw_ellipse_filled(SCREEN_WIDTH / 2 + shake_x, 505 + shake_y, 1220, 145, (18, 17, 24, 225))
        arcade.draw_ellipse_outline(SCREEN_WIDTH / 2 + shake_x, 505 + shake_y, 1220, 145, (75, 62, 48, 160), 2)

        # Панель героя (верхний левый угол с иконками статов)
        arcade.draw_rect_filled(arcade.XYWH(195, 910, 310, 210), PANEL_DARK)
        arcade.draw_rect_outline(arcade.XYWH(195, 910, 310, 210), BORDER_GOLD, 2)
        self.ui_text.draw(self.hero.name, 195, 975, TEXT_PARCHMENT, 22, bold=True, anchor_x="center")

        draw_stat_icon("hp", 95, 938, size=11)
        self.ui_text.draw(f"HP: {self.hero.hp} / {self.hero.max_hp}", 118, 932, (115, 185, 130), 17, anchor_x="left")

        draw_stat_icon("block", 95, 901, size=11)
        self.ui_text.draw(f"Броня: {self.hero.block}", 118, 895, (110, 160, 205), 17, anchor_x="left")

        draw_stat_icon("stamina", 95, 859, size=11)
        self.ui_text.draw(f"Стамина: {self.hero.stamina} / {self.hero.max_stamina}", 118, 852, BORDER_GOLD, 19,
                         bold=True, anchor_x="left")

        # Панель врага (верхний правый угол с иконками HP и Брони)
        if self.enemy:
            ex_panel = SCREEN_WIDTH - 230
            ey_panel = 895
            pw, ph = 390, 250
            if self.enemy.is_boss:
                arcade.draw_rect_filled(arcade.XYWH(ex_panel, ey_panel, pw, ph), (26, 12, 18))
                arcade.draw_rect_outline(arcade.XYWH(ex_panel, ey_panel, pw, ph), (175, 42, 48), 3.5)
                arcade.draw_rect_outline(arcade.XYWH(ex_panel, ey_panel, pw - 12, ph - 12), BORDER_GOLD, 1.5)
                for dx in (-pw / 2 + 8, pw / 2 - 8):
                    for dy in (-ph / 2 + 8, ph / 2 - 8):
                        arcade.draw_circle_filled(ex_panel + dx, ey_panel + dy, 4, BORDER_GOLD)
            else:
                arcade.draw_rect_filled(arcade.XYWH(ex_panel, ey_panel, pw, ph), PANEL_ENEMY)
                arcade.draw_rect_outline(arcade.XYWH(ex_panel, ey_panel, pw, ph), (140, 42, 46), 2.5)

            name_color = BORDER_GOLD if self.enemy.is_boss else TEXT_PARCHMENT
            self.ui_text.draw(self.enemy.name, ex_panel, ey_panel + 82, name_color, 17, bold=True, width=pw - 36,
                             align="center", anchor_x="center", anchor_y="center", multiline=True)

            # Иконки и значения HP и Брони врага в одну строку
            draw_stat_icon("hp", ex_panel - 135, ey_panel + 38, size=10)
            self.ui_text.draw(f"{self.enemy.hp}/{self.enemy.max_hp}", ex_panel - 116, ey_panel + 32, (215, 110, 105), 16,
                             bold=True, anchor_x="left")

            draw_stat_icon("block", ex_panel + 25, ey_panel + 38, size=10)
            self.ui_text.draw(f"Броня: {self.enemy.block}", ex_panel + 44, ey_panel + 32, (110, 160, 205), 16,
                             anchor_x="left")

            self.ui_text.draw("Намерение: ??? (Скрыто)", ex_panel, ey_panel - 4, TEXT_MUTED, 15, bold=True,
                             anchor_x="center")
            self.ui_text.draw(f"Прошлый ход:\n{self.enemy.last_action_text}", ex_panel, ey_panel - 65, TEXT_PARCHMENT,
                             13, width=pw - 40, align="center", anchor_x="center", anchor_y="center", multiline=True)

        ng_badge = f" [НГ+{self.run.ng_level}]" if self.run.ng_level > 0 else ""
        round_str = "БОСС ЛОКАЦИИ" if self.run.round_idx == 3 else f"Раунд {self.run.round_idx} из 3"
        self.ui_text.draw(f"{self.run.location_title}{ng_badge}  •  {round_str}  •  Ход {self.run.total_turns}",
                         SCREEN_WIDTH / 2, 1020, BORDER_GOLD, 21, bold=True, anchor_x="center")

        if self.player_avatar:
            self.player_avatar.draw()
        if self.enemy_avatar:
            self.enemy_avatar.draw()
            if self.substate == "FIGHT" and not self.enemy_attack_pending:
                draw_enemy_choice_icons(self.enemy_avatar.base_x, self.enemy_avatar.base_y + 160,
                                        self.enemy_avatar.time)

        for proj in self.projectiles:
            proj.draw()

        # Нижняя панель игрока: подложка интерфейса и выровненные по высоте элементы (y = 185)
        arcade.draw_rect_filled(arcade.XYWH(SCREEN_WIDTH / 2, 185, 1840, 290), (16, 15, 21, 185))
        arcade.draw_rect_outline(arcade.XYWH(SCREEN_WIDTH / 2, 185, 1840, 290), (55, 48, 42, 150), 1.5)

        # Блок Колоды и Сброса (нижний ярус левой панели, центр y = 115)
        arcade.draw_rect_filled(arcade.XYWH(195, 115, 230, 110), PANEL_DARK)
        arcade.draw_rect_outline(arcade.XYWH(195, 115, 230, 110), (75, 62, 48), 1.5)

        draw_stat_icon("deck", 115, 142, size=12)
        self.ui_text.draw(f"Колода: {len(self.hero.draw_pile)}", 142, 135, TEXT_PARCHMENT, 18, bold=True,
                         anchor_x="left")

        draw_stat_icon("discard", 115, 88, size=12)
        self.ui_text.draw(f"Сброс: {len(self.hero.discard_pile)}", 142, 81, TEXT_MUTED, 17, anchor_x="left")

        self._draw_active_bonuses()

        # Кнопка завершения хода справа внизу (подсвечивается при наведении, часы медленно вращаются)
        if self.substate == "FIGHT":
            bx, by, bw, bh = self.end_turn_btn
            btn_bg = (145, 56, 42) if self.end_turn_hovered else (110, 42, 32)
            btn_border = arcade.color.YELLOW if self.end_turn_hovered else BORDER_GOLD
            btn_w = 3.5 if self.end_turn_hovered else 2.0

            arcade.draw_rect_filled(arcade.XYWH(bx, by, bw, bh), btn_bg)
            arcade.draw_rect_outline(arcade.XYWH(bx, by, bw, bh), btn_border, btn_w)

            # Медленный бесконечный цикл вращения часов (полный оборот ~4.2 сек)
            hourglass_angle = -(anim_time * 1.5) % (math.pi * 2)
            draw_stat_icon("end_turn", bx - 78, by, size=12, angle=self.hourglass_angle)
            self.ui_text.draw("Закончить ход", bx + 14, by, TEXT_PARCHMENT, 17, bold=True, anchor_x="center",
                             anchor_y="center")


        self.ui_text.draw(self.message, SCREEN_WIDTH / 2, 360, BORDER_GOLD, 18, bold=True, anchor_x="center")

        for w in self.hand_widgets:
            if not w.hovered:
                w.draw(can_afford=(self.hero.stamina >= w.cost))
        for w in self.hand_widgets:
            if w.hovered:
                w.draw(can_afford=(self.hero.stamina >= w.cost))

        if self.playing_widget:
            self.playing_widget.draw(can_afford=True)
        if self.enemy_playing_widget:
            self.enemy_playing_widget.draw(can_afford=True)

        for eff in self.effects:
            eff.draw()

        if self.substate == "BOSS_VICTORY":
            self._draw_boss_victory_overlay()

        self.toast_manager.draw()

    def _draw_active_bonuses(self):
        """Отрисовывает медальоны усилений на верхнем ярусе левой панели (y = 268)."""
        items = []
        if self.run.bonuses.get("max_hp", 0) > 0:
            val = self.run.bonuses["max_hp"]
            items.append(("Защита", f"+{val} HP"))
        if self.run.bonuses.get("damage", 0) > 0:
            val = self.run.bonuses["damage"]
            items.append(("Атака", f"+{val} Урон"))
        if self.run.bonuses.get("heal", 0) > 0:
            val = self.run.bonuses["heal"]
            items.append(("Исцеление", f"+{val} Хил"))

        if not items:
            return

        arcade.draw_text("УСИЛЕНИЯ ПОХОДА:", 80, 315, TEXT_MUTED, 12, bold=True, anchor_x="left")
        for i, (icon_type, badge) in enumerate(items):
            bx = 112 + i * 82
            by = 268
            arcade.draw_circle_filled(bx, by, 23, PANEL_DARK)
            arcade.draw_circle_outline(bx, by, 23, BORDER_GOLD, 2)
            draw_card_icon(icon_type, bx, by, size=16)
            arcade.draw_text(badge, bx, by - 38, BORDER_GOLD, 12, bold=True, anchor_x="center")

        if self.hovered_bonus_desc:
            arcade.draw_rect_filled(arcade.XYWH(285, 375, 410, 48), (18, 16, 24, 245))
            arcade.draw_rect_outline(arcade.XYWH(285, 375, 410, 48), BORDER_GOLD, 1.5)
            arcade.draw_text(
                self.hovered_bonus_desc, 285, 375, TEXT_PARCHMENT, 12,
                width=390, align="center", anchor_x="center", anchor_y="center", multiline=True
            )

    def _draw_boss_victory_overlay(self):
        arcade.draw_rect_filled(arcade.XYWH(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 40, 760, 340), (16, 14, 22, 245))
        arcade.draw_rect_outline(arcade.XYWH(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 40, 760, 340), BORDER_GOLD, 3)

        arcade.draw_text("ВЛАДЫКА ТЬМЫ ПОВЕРЖЕН!", SCREEN_WIDTH / 2, 650, BORDER_GOLD, 32, bold=True, anchor_x="center")
        arcade.draw_text(f"Летопись обновлена! Пройдено за {self.run.total_turns} ходов (Режим: НГ+{self.run.ng_level}).", SCREEN_WIDTH / 2, 590, TEXT_PARCHMENT, 16, anchor_x="center")
        arcade.draw_text("Спуститься глубже во тьму (НГ+) или вернуться в главное меню?", SCREEN_WIDTH / 2, 545, TEXT_MUTED, 15, anchor_x="center")

        cx, cy, cw, ch = self.ng_continue_btn
        arcade.draw_rect_filled(arcade.XYWH(cx, cy, cw, ch), (38, 68, 52))
        arcade.draw_rect_outline(arcade.XYWH(cx, cy, cw, ch), BORDER_GOLD, 2)
        arcade.draw_text(f"Продолжить (НГ+{self.run.ng_level + 1})", cx, cy, TEXT_PARCHMENT, 17, bold=True, anchor_x="center", anchor_y="center")

        ex, ey, ew, eh = self.ng_exit_btn
        arcade.draw_rect_filled(arcade.XYWH(ex, ey, ew, eh), (36, 52, 74))
        arcade.draw_rect_outline(arcade.XYWH(ex, ey, ew, eh), BORDER_GOLD, 2)
        arcade.draw_text("Выйти в меню", ex, ey, TEXT_PARCHMENT, 17, bold=True, anchor_x="center", anchor_y="center")

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.hovered_bonus_desc = ""
        bonus_list = []
        if self.run.bonuses.get("max_hp", 0) > 0:
            bonus_list.append(f"Закалка плоти: максимальное здоровье увеличено на +{self.run.bonuses['max_hp']} ед.")
        if self.run.bonuses.get("damage", 0) > 0:
            bonus_list.append(f"Заточка клинков: все атакующие карты наносят на +{self.run.bonuses['damage']} урона больше.")
        if self.run.bonuses.get("heal", 0) > 0:
            bonus_list.append(f"Благословение жизни: все лечащие карты восстанавливают на +{self.run.bonuses['heal']} HP больше.")

        for i, desc in enumerate(bonus_list):
            if abs(x - (112 + i * 82)) <= 26 and abs(y - 268) <= 26:
                self.hovered_bonus_desc = desc
                break

        bx, by, bw, bh = self.end_turn_btn
        self.end_turn_hovered = (
                self.substate == "FIGHT"
                and bx - bw / 2 <= x <= bx + bw / 2
                and by - bh / 2 <= y <= by + bh / 2
        )

        if self.substate != "FIGHT" or self.playing_widget or self.enemy_attack_pending:
            return
        any_hovered = False
        for w in self.hand_widgets:
            if not any_hovered and w.is_clicked(x, y):
                w.hovered = True
                any_hovered = True
            else:
                w.hovered = False

        if self.player_avatar and self.player_avatar.state in ("idle", "thinking"):
            self.player_avatar.state = "thinking" if any_hovered else "idle"

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        if self.substate == "BOSS_VICTORY":
            cx, cy, cw, ch = self.ng_continue_btn
            if cx - cw / 2 <= x <= cx + cw / 2 and cy - ch / 2 <= y <= cy + ch / 2:
                from views.boss_reward_view import BossRewardView
                self.window.show_view(BossRewardView(self.run, is_final_boss=True))
                return
            ex, ey, ew, eh = self.ng_exit_btn
            if ex - ew / 2 <= x <= ex + ew / 2 and ey - eh / 2 <= y <= ey + eh / 2:
                from views.menu_view import MenuView
                self.window.show_view(MenuView())
                return

        elif self.substate == "FIGHT":
            for w in list(self.hand_widgets):
                if w.is_clicked(x, y):
                    self._start_play_card(w)
                    return
            bx, by, bw, bh = self.end_turn_btn
            if bx - bw / 2 <= x <= bx + bw / 2 and by - bh / 2 <= y <= by + bh / 2:
                self._end_player_turn()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            from views.menu_view import MenuView
            self.window.show_view(MenuView())
        elif key == arcade.key.R and self.substate == "GAME_OVER":
            from views.hero_select_view import HeroSelectView
            self.window.show_view(HeroSelectView())
