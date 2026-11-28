import math
import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BG_DARK, BORDER_GOLD, TEXT_PARCHMENT
from core.card import Card, load_card_library
from core.combat import CombatEngine, CombatEvent
from core.enemy import Enemy
from core.events import bus
from core.records import check_stage_achievements
from core.run_state import RunState
from visuals.effects.vfx_director import VFXDirector
from visuals.locations import draw_location_background
from visuals.sprites.avatar import CharacterAvatar
from visuals.ui.card_widget import CardWidget
from visuals.ui.icons import draw_enemy_choice_icons
from visuals.ui.text_cache import TextCache
from views.battle.battle_hud import BattleHUD
from views.battle.battle_modals import BattleModals
from views.battle.pause_menu import BattlePauseMenu



class BattleView(arcade.View):
    def __init__(self, run: RunState):
        super().__init__()
        self.run = run
        self.hero = run.hero
        self.enemy: Enemy | None = None
        self.engine = CombatEngine(self.run)
        self.scale = 1.0



        self.substate = "FIGHT"  # "FIGHT" | "BOSS_VICTORY"
        self.message = ""
        self.turn_count = 1
        self.boss_rewards: list[Card] = []

        self.player_avatar: CharacterAvatar | None = None
        self.enemy_avatar: CharacterAvatar | None = None

        self.hand_widgets: list[CardWidget] = []
        self.playing_widget: CardWidget | None = None
        self.play_timer = 0.0

        self.enemy_playing_widget: CardWidget | None = None
        self.enemy_attack_pending = False
        self.enemy_turn_timer = 0.0

        # Координаты кнопок (левый стек опущен к нижнему краю, чтобы сверху осталось место под перки)
        self.end_turn_btn = (SCREEN_WIDTH - 150, 220, 230, 58)
        self.deck_btn = (115, 172, 175, 54)
        self.discard_btn = (115, 106, 175, 54)
        self.pause_btn_rect = (115, 48, 175, 36)

        self.end_turn_hovered = False
        self.end_turn_scale = 1.0

        self.deck_hovered = False
        self.discard_hovered = False
        self.pause_btn_hovered = False


        self.hourglass_angle = 0.0
        self.deck_anim_time = 0.0
        self.discard_anim_time = 0.0

        self.ui_text = TextCache()
        self.vfx = VFXDirector(self)
        self.hud = BattleHUD(self)
        self.modals = BattleModals(self)
        self.pause_menu = BattlePauseMenu(self)

        self.auto_end_timer = 0.0

        self._stage_initialized = False

    def on_show_view(self):
        arcade.set_background_color(BG_DARK)
        if not self._stage_initialized:
            self._stage_initialized = True
            self._setup_stage()

    def _setup_stage(self):
        self.auto_end_timer = 0.0
        self.substate = "FIGHT"
        self.turn_count = 1
        self.playing_widget = None
        self.enemy_playing_widget = None
        self.enemy_attack_pending = False
        self.vfx.clear()

        self.enemy = self.engine.setup_encounter()
        start_events = self.engine.begin_player_turn()
        self._spawn_visuals_for_events(start_events)

        self.player_avatar = CharacterAvatar(self.hero.name, x=695, y=568, scale=1.85, flip=False)
        enemy_scale = 2.25 if self.enemy.role in ("Тёмный Рыцарь", "Скелет-гигант") else (
            2.05 if self.enemy.is_boss else 1.85)
        self.enemy_avatar = CharacterAvatar(self.enemy.role, x=SCREEN_WIDTH - 695, y=568, scale=enemy_scale, flip=True)

        self.message = f"Этап {self.run.round_idx}/3 (Ход {self.turn_count}). Ваш ход!"
        self._sync_hand_widgets()

    def _sync_hand_widgets(self):
        cards = self.hero.hand
        if not cards:
            self.hand_widgets.clear()
            return

        existing_map = {id(w.data): w for w in self.hand_widgets}
        new_widgets: list[CardWidget] = []

        max_span = 1240
        step = min(255, max_span / max(1, len(cards)))
        start_x = SCREEN_WIDTH / 2 - (len(cards) - 1) * step / 2
        deck_x, deck_y = self.deck_btn[0], self.deck_btn[1]

        for idx, c in enumerate(cards):
            tx = start_x + idx * step
            ty = 200
            w = existing_map.get(id(c))
            if w is None:
                w = CardWidget(c, x=deck_x, y=deck_y, cost=c.cost)
                w.scale = 0.25
            w.target_x = tx
            w.target_y = ty
            new_widgets.append(w)

        self.hand_widgets = new_widgets

    def _spawn_visuals_for_events(self, events):
        if not isinstance(events, (list, tuple)):
            return
        for ev in events:
            if isinstance(ev, str) or not isinstance(ev, CombatEvent):
                continue
            if ev.kind == "damage":
                bus.emit("damage_dealt", target=ev.target, value=ev.value, blocked=ev.blocked)
            elif ev.kind == "block":
                bus.emit("block_gained", target=ev.target, value=ev.value)
            elif ev.kind == "strip_block":
                bus.emit("strip_block", target=ev.target, value=ev.value)
            elif ev.kind == "heal" and ev.value > 0:
                bus.emit("heal_gained", target=ev.target, value=ev.value)
            elif ev.kind == "stamina":
                bus.emit("stamina_gained", value=ev.value)
            elif ev.kind == "steal_stamina":
                bus.emit("stamina_stolen", value=ev.value)

    def _start_play_card(self, widget: CardWidget):
        if self.playing_widget or self.enemy_attack_pending or self.substate != "FIGHT":
            return
        card = widget.data
        if self.hero.stamina < card.cost:
            self.message = "Недостаточно стамины!"
            return

        # Списание стамины произойдёт один раз внутри engine.play_player_card()
        if card in self.hero.hand:
            self.hero.hand.remove(card)
        self._sync_hand_widgets()

        widget.is_playing = True
        widget.hovered = False
        widget.target_x = SCREEN_WIDTH / 2
        widget.target_y = 590
        self.playing_widget = widget
        self.play_timer = 0.35
        bus.emit("card_played", card=card)

    def _open_stage_reward(self):
        import importlib
        import pkgutil
        import views

        self.vfx.unbind()
        for _, mod_name, is_pkg in pkgutil.walk_packages(views.__path__, views.__name__ + "."):
            if is_pkg or "reward" not in mod_name.lower():
                continue
            module = importlib.import_module(mod_name)
            for attr_name in ("StageRewardView", "RewardView"):
                reward_cls = getattr(module, attr_name, None)
                if reward_cls is not None:
                    self.window.show_view(reward_cls(self.run))
                    return
        raise ModuleNotFoundError("Не найден экран наград в пакете views/")

    def _resolve_player_card(self, widget: CardWidget):
        events, outcome = self.engine.play_player_card(widget.data)
        self._spawn_visuals_for_events(events)
        self._sync_hand_widgets()


        if outcome == "STAGE_REWARD":
            self._open_stage_reward()
        elif outcome == "BOSS_REWARD":
            self._prepare_boss_victory()
        elif outcome == "FINAL_VICTORY":
            self.vfx.unbind()
            self._prepare_boss_victory()

        if outcome == "GAME_OVER":
            self.vfx.unbind()
            self.substate = "GAME_OVER"
            self.ng_exit_btn = (SCREEN_WIDTH / 2, 415, 330, 62)
            self.message = "ВЫ ПАЛИ ВО ТЬМЕ !"
            return

        if outcome == "CONTINUE" and not self.hero.hand and self.substate == "FIGHT":
                self.auto_end_timer = 0.35


    def _prepare_boss_victory(self):
        all_cards = list(load_card_library().values())
        class_tag = self.hero.name.upper()
        pool = [c for c in all_cards if c.hero_class == class_tag or c.neutral]
        import random
        chosen = random.sample(pool, min(4, len(pool)))
        self.boss_rewards = [c.create_upgraded_copy() for c in chosen]
        self.modals.setup_boss_rewards(self.boss_rewards)
        self.substate = "BOSS_VICTORY"
        self.message = "Босс повержен! Выберите 2 карты в награду."

    def _end_player_turn(self):
        if self.playing_widget or self.enemy_attack_pending or not self.enemy or self.substate != "FIGHT":
            return
        res = self.engine.end_player_turn()
        act = (res if not isinstance(res, tuple) else res) or getattr(self.enemy, "planned_action", None)
        self._sync_hand_widgets()

        self.enemy_attack_pending = True
        self.enemy_turn_timer = 0.75
        self.message = f"Этап {self.run.round_idx}/3 (Ход {self.turn_count}). Ход противника..."

        if act:
            ew = CardWidget(act, x=SCREEN_WIDTH - 695, y=585, cost=0)
            ew.target_x = SCREEN_WIDTH / 2
            ew.target_y = 610
            ew.is_playing = True
            self.enemy_playing_widget = ew
            bus.emit("enemy_action_started", action=act)

        self._sync_hand_widgets()

    def _resolve_enemy_turn(self):
        self.enemy_playing_widget = None
        if not self.enemy or not self.engine:
            return

        events, status = self.engine.resolve_enemy_turn()
        self._spawn_visuals_for_events(events)

        if status == "GAME_OVER":
            self.vfx.unbind()
            self.substate = "GAME_OVER"
            self.ng_exit_btn = (SCREEN_WIDTH / 2, 415, 330, 62)
            self.message = "ВЫ ПАЛИ ВО ТЬМЕ !"
            return

        start_events = self.engine.begin_player_turn()
        self._spawn_visuals_for_events(start_events)
        self.turn_count += 1
        self.message = f"Этап {self.run.round_idx}/3 (Ход {self.turn_count}). Ваш ход!"
        self._sync_hand_widgets()


    def _advance_after_boss(self):
        self.vfx.unbind()
        ng = getattr(self.run, "ng_level", 0)
        if self.enemy:
            check_stage_achievements(self.hero.name, self.run.stage, ng, self.enemy.role)

        if self.run.stage >= 3:
            self.vfx.unbind()
            self.substate = "FINAL_VICTORY"
            self.ng_continue_btn = (SCREEN_WIDTH / 2 - 190, 415, 330, 62)
            self.ng_exit_btn = (SCREEN_WIDTH / 2 + 190, 415, 330, 62)
        else:
            self.run.advance_world()
            self.window.show_view(BattleView(self.run))

    def on_update(self, delta_time: float):
        if self.pause_menu.is_open:
            return

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

        if self.auto_end_timer > 0:
            self.auto_end_timer -= delta_time
            if self.auto_end_timer <= 0:
                self.auto_end_timer = 0.0
                if not self.hero.hand and self.substate == "FIGHT" and not self.playing_widget and not self.enemy_attack_pending:
                    self._end_player_turn()

        self.hourglass_angle = (self.hourglass_angle - delta_time * 1.8) % (math.pi * 2) if (self.end_turn_hovered and self.substate == "FIGHT") else 0.0
        self.deck_anim_time += delta_time * (3.5 if self.deck_hovered else 0.8)
        self.discard_anim_time += delta_time * (3.5 if self.discard_hovered else 0.8)

        self.vfx.update(delta_time)
        can_end = (self.substate == "FIGHT" and not self.enemy_attack_pending and self.playing_widget is None)
        target_scale = 1.08 if (self.end_turn_hovered and can_end) else 1.0
        self.end_turn_scale += (target_scale - self.end_turn_scale) * min(1.0, delta_time * 14.0)

    def on_draw(self):
        self.clear()
        anim_time = self.player_avatar.time if self.player_avatar else 0.0
        draw_location_background(self.run.current_location_name, anim_time)

        shake_x, shake_y = self.vfx.get_shake_offset()
        arcade.draw_ellipse_filled(SCREEN_WIDTH / 2 + shake_x, 505 + shake_y, 1220, 145, (18, 17, 24, 225))
        arcade.draw_ellipse_outline(SCREEN_WIDTH / 2 + shake_x, 505 + shake_y, 1220, 145, (75, 62, 48, 160), 2)

        if self.player_avatar:
            self.player_avatar.draw()
        if self.enemy_avatar:
            self.enemy_avatar.draw()
            if self.substate == "FIGHT" and not self.enemy_attack_pending:
                draw_enemy_choice_icons(self.enemy_avatar.base_x, self.enemy_avatar.base_y + 160, self.enemy_avatar.time)

        self.vfx.draw_projectiles()
        self.hud.draw()

        px, py, pw, ph = self.pause_btn_rect
        arcade.draw_rect_filled(arcade.XYWH(px, py, pw, ph), (36, 33, 46) if self.pause_btn_hovered else (22, 20, 28))
        arcade.draw_rect_outline(arcade.XYWH(px, py, pw, ph), arcade.color.YELLOW if self.pause_btn_hovered else BORDER_GOLD, 1.5)
        self.ui_text.draw("Пауза [ESC]", px, py, TEXT_PARCHMENT, 14, bold=True, anchor_x="center", anchor_y="center")

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

        self.vfx.draw_foreground()
        self.hud.draw_tooltip()

        if self.substate == "BOSS_VICTORY":
            self.modals.draw_boss_victory_overlay()
        if self.modals.is_open:
            self.modals.draw_pile_modal()

        self.pause_menu.draw()

        # В конце on_draw():
        if self.substate in ("FINAL_VICTORY", "GAME_OVER"):
            is_win = (self.substate == "FINAL_VICTORY")
            arcade.draw_rect_filled(arcade.XYWH(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT), (10, 9, 14, 225))
            arcade.draw_rect_filled(arcade.XYWH(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 40, 780, 340), (18, 16, 24, 248))
            arcade.draw_rect_outline(arcade.XYWH(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 40, 780, 340), BORDER_GOLD, 3)

            title = "ВЛАДЫКА ТЬМЫ ПОВЕРЖЕН!" if is_win else "ВЫ ПАЛИ ВО ТЬМЕ..."
            sub = f"Победа одержана за {getattr(self.run, 'total_turns', self.turn_count)} ходов (НГ+{getattr(self.run, 'ng_level', 0)})!" if is_win else "Тьма поглотила героя, но летопись сохранила ваш путь."
            self.ui_text.draw(title, SCREEN_WIDTH / 2, 650, BORDER_GOLD, 32, bold=True, anchor_x="center")
            self.ui_text.draw(sub, SCREEN_WIDTH / 2, 585, TEXT_PARCHMENT, 17, anchor_x="center")

            if is_win:
                cx, cy, cw, ch = self.ng_continue_btn
                arcade.draw_rect_filled(arcade.XYWH(cx, cy, cw, ch), (38, 76, 52))
                arcade.draw_rect_outline(arcade.XYWH(cx, cy, cw, ch), BORDER_GOLD, 2)
                self.ui_text.draw(f"Продолжить (НГ+{getattr(self.run, 'ng_level', 0) + 1})", cx, cy, TEXT_PARCHMENT, 17, bold=True, anchor_x="center", anchor_y="center")

            ex, ey, ew, eh = self.ng_exit_btn
            arcade.draw_rect_filled(arcade.XYWH(ex, ey, ew, eh), (42, 48, 72))
            arcade.draw_rect_outline(arcade.XYWH(ex, ey, ew, eh), BORDER_GOLD, 2)
            self.ui_text.draw("В главное меню", ex, ey, TEXT_PARCHMENT, 17, bold=True, anchor_x="center", anchor_y="center")


    @staticmethod
    def _in_rect(x: float, y: float, rect: tuple[float, float, float, float]) -> bool:
        rx, ry, rw, rh = rect
        return rx - rw / 2 <= x <= rx + rw / 2 and ry - rh / 2 <= y <= ry + rh / 2

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.mouse_x = x
        self.mouse_y = y

        if self.pause_menu.is_open:
            self.pause_menu.on_mouse_motion(x, y)
            return

        if self.substate in ("FINAL_VICTORY", "GAME_OVER"):
            return

        if self.modals.is_open or self.substate == "BOSS_VICTORY":
            self.modals.on_mouse_motion(x, y)
            return

        self.end_turn_hovered = self._in_rect(x, y, self.end_turn_btn)
        self.deck_hovered = self._in_rect(x, y, self.deck_btn)
        self.discard_hovered = self._in_rect(x, y, self.discard_btn)
        self.pause_btn_hovered = self._in_rect(x, y, self.pause_btn_rect)

        for w in self.hand_widgets:
            w.hovered = (self.substate == "FIGHT" and not self.playing_widget and not self.enemy_attack_pending and w.contains_point(x, y))

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        if self.substate in ("FINAL_VICTORY", "GAME_OVER"):
            if self.substate == "FINAL_VICTORY" and self._in_rect(x, y, self.ng_continue_btn):
                self.run.start_new_game_plus()
                self.window.show_view(BattleView(self.run))
                return
            if self._in_rect(x, y, self.ng_exit_btn):
                from views.menu.menu_view import MenuView
                self.window.show_view(MenuView())
            return

        if self.pause_menu.handle_click(x, y):
            return
        if self.modals.handle_click(x, y):
            return
        if self._in_rect(x, y, self.pause_btn_rect):
            self.pause_menu.open()
            return
        if self._in_rect(x, y, self.deck_btn):
            bus.emit("ui_click")
            self.modals.open_pile("Колода добора", self.hero.draw_pile)
            return
        if self._in_rect(x, y, self.discard_btn):
            bus.emit("ui_click")
            self.modals.open_pile("Стопка сброса", self.hero.discard_pile)
            return
        if self._in_rect(x, y, self.end_turn_btn):
            bus.emit("ui_click")
            self._end_player_turn()
            return

        if self.substate == "FIGHT" and not self.playing_widget and not self.enemy_attack_pending:
            for w in reversed(self.hand_widgets):
                if w.contains_point(x, y):
                    self._start_play_card(w)
                    return

    def on_mouse_scroll(self, x: int, y: int, _scroll_x: int, scroll_y: int):
        self.modals.on_mouse_scroll(scroll_y)

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.ESCAPE:
            if self.modals.is_open:
                self.modals.close()
            else:
                self.pause_menu.handle_escape()
            return
        if self.pause_menu.is_open or self.modals.is_open:
            return
        if key in (arcade.key.SPACE, arcade.key.ENTER):
            self._end_player_turn()
