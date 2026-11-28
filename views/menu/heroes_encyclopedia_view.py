from collections import Counter
import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BG_DARK, PANEL_DARK, PANEL_ENEMY, BORDER_GOLD, TEXT_PARCHMENT, TEXT_MUTED
from core.hero import load_hero_templates
from core.card import Card, load_card_library
from core.effects import build_effects
from core.records import load_records
from core.enemy import load_enemy_pools
from visuals.sprites.avatar import CharacterAvatar
from visuals.ui.card_widget import CardWidget
from visuals.ui.icons import draw_stat_icon
from visuals.ui.text_cache import TextCache


class HeroesEncyclopediaView(arcade.View):
    """Энциклопедия мира: Герои (с личной колодой) и Враги (Мобы и Боссы с их действиями)."""

    def __init__(self, return_view: arcade.View | None = None):
        super().__init__()
        self.return_view = return_view
        self.ui_text = TextCache()
        self.back_btn = (150, SCREEN_HEIGHT - 55, 200, 48)

        # Главные вкладки ("HEROES" | "ENEMIES") и подвкладки врагов ("MOBS" | "BOSSES")
        self.main_tab = "HEROES"
        self.enemy_subtab = "MOBS"
        self.seen_enemies = set(load_records().get("seen_enemies", []))


        self.main_tab_btns = (
            {"id": "HEROES", "label": "ГЕРОИ", "x": SCREEN_WIDTH / 2 - 140, "y": SCREEN_HEIGHT - 148, "w": 250, "h": 46},
            {"id": "ENEMIES", "label": "ВРАГИ", "x": SCREEN_WIDTH / 2 + 140, "y": SCREEN_HEIGHT - 148, "w": 250, "h": 46},
        )
        self.sub_tab_btns = (
            {"id": "MOBS", "label": "РЯДОВЫЕ МОБЫ", "x": SCREEN_WIDTH / 2 - 150, "y": SCREEN_HEIGHT - 205, "w": 270, "h": 40},
            {"id": "BOSSES", "label": "БОССЫ И ЭЛИТА", "x": SCREEN_WIDTH / 2 + 150, "y": SCREEN_HEIGHT - 205, "w": 270, "h": 40},
        )

        self.scroll_y = 0.0
        self.max_scroll = 0.0
        self.block_height = 340
        self.block_gap = 26

        self.active_modal: dict | None = None
        self.modal_close_btn = (SCREEN_WIDTH / 2, 128, 260, 50)
        self.action_buttons: list[tuple[float, float, float, float, dict]] = []

        self.hero_entries = self._build_hero_entries()
        self.mob_entries, self.boss_entries = self._build_enemy_entries()
        self._recalc_scroll()

    def _build_hero_entries(self) -> list[dict]:
        templates = load_hero_templates()
        library = load_card_library()
        entries = []
        for name, info in templates.items():
            deck_ids = [cid for cid in info.get("deck", []) if cid in library]
            counts = Counter(deck_ids)
            modal_cards = [{"widget": CardWidget(library[cid]), "qty": qty} for cid, qty in counts.items()]
            entries.append({
                "kind": "HERO",
                "name": name,
                "hp": info["hp"],
                "stamina": info["stamina"],
                "difficulty": info.get("difficulty", "Средняя"),
                "style": info.get("style", ""),
                "mechanic": info.get("mechanic", ""),
                "desc": info.get("desc", ""),
                "total_cards": len(deck_ids),
                "avatar": CharacterAvatar(name, 300, 0, scale=1.45),
                "cards": modal_cards,
            })
        return entries

    def _build_enemy_entries(self) -> tuple[list[dict], list[dict]]:
        pools = load_enemy_pools()

        def make_entry(raw: dict, tier: str, is_boss: bool) -> dict:
            modal_cards = []
            for idx, act in enumerate(raw.get("actions", [])):
                effs = build_effects(act.get("effects", []))
                desc = ", ".join(e.describe(1.0) for e in effs if e.describe(1.0))
                dummy = Card(f"act_{idx}", act["name"], act["type"], 0, desc, effs)
                modal_cards.append({"widget": CardWidget(dummy), "qty": None})

            scale = 1.75 if raw.get("role") == "Тёмный Рыцарь" else (1.55 if is_boss else 1.45)
            return {
                "kind": "ENEMY",
                "is_boss": is_boss,
                "name": raw["name"],
                "role": raw["role"],
                "hp": raw["hp"],
                "tier": tier,
                "actions_count": len(modal_cards),
                "avatar": CharacterAvatar(raw["role"], 300, 0, scale=scale, flip=True),
                "cards": modal_cards,
            }

        mobs = [make_entry(e, "Рядовой противник (Мир 1–2)", False) for e in pools["regular"]]
        bosses = [make_entry(e, "Элитная гвардия (Мир 3)", True) for e in pools["elite"]]
        bosses.extend(make_entry(e, "Босс акта (Мир 1–2)", True) for e in pools["act_bosses"])
        bosses.extend(make_entry(e, "Финальный Сверхбосс (Мир 3)", True) for e in pools["final_bosses"])
        return mobs, bosses

    def _current_entries(self) -> list[dict]:
        if self.main_tab == "HEROES":
            return self.hero_entries
        return self.mob_entries if self.enemy_subtab == "MOBS" else self.boss_entries

    def _top_margin(self) -> float:
        return 885.0 if self.main_tab == "HEROES" else 830.0

    def _recalc_scroll(self):
        self.scroll_y = 0.0
        entries = self._current_entries()
        total_h = len(entries) * (self.block_height + self.block_gap)
        visible_h = self._top_margin() - 40
        self.max_scroll = max(0.0, total_h - visible_h)

    def on_show_view(self):
        arcade.set_background_color(BG_DARK)

    def on_update(self, delta_time: float):
        for entry in self._current_entries():
            entry["avatar"].update(delta_time)

    def on_mouse_scroll(self, x: int, y: int, _scroll_x: int, scroll_y: int):
        if self.active_modal is None:
            self.scroll_y = max(0.0, min(self.max_scroll, self.scroll_y - scroll_y * 55.0))

    def on_draw(self):
        self.clear()
        self.action_buttons.clear()

        entries = self._current_entries()
        top_y = self._top_margin()

        for idx, entry in enumerate(entries):
            center_y = (top_y - self.block_height / 2) - idx * (self.block_height + self.block_gap) + self.scroll_y
            if center_y + self.block_height / 2 < 0 or center_y - self.block_height / 2 > SCREEN_HEIGHT:
                continue

            bx, bw, bh = SCREEN_WIDTH / 2, 1560, self.block_height
            is_boss = entry.get("is_boss", False)
            card_bg = (28, 15, 20) if is_boss else (PANEL_ENEMY if entry["kind"] == "ENEMY" else PANEL_DARK)
            border_col = (185, 48, 52) if is_boss else BORDER_GOLD

            arcade.draw_rect_filled(arcade.XYWH(bx, center_y, bw, bh), card_bg)
            arcade.draw_rect_outline(arcade.XYWH(bx, center_y, bw, bh), border_col, 2.5 if is_boss else 2)

            tx = 460
            if entry["kind"] == "HERO":
                av = entry["avatar"]
                av.base_x = 300
                av.base_y = center_y - 10
                av.draw()

                self.ui_text.draw(entry["name"], tx, center_y + 118, BORDER_GOLD, 28, bold=True)
                draw_stat_icon("hp", tx + 10, center_y + 78, size=11)
                self.ui_text.draw(f"HP: {entry['hp']}", tx + 30, center_y + 72, (115, 185, 130), 17, bold=True)
                draw_stat_icon("stamina", tx + 155, center_y + 78, size=11)
                self.ui_text.draw(f"Стамина: {entry['stamina']}", tx + 175, center_y + 72, BORDER_GOLD, 17, bold=True)

                self.ui_text.draw(f"Сложность: {entry['difficulty']}", tx, center_y + 36, TEXT_PARCHMENT, 16, bold=True)
                self.ui_text.draw(f"Темп / стиль: {entry['style']}", tx, center_y + 6, (145, 185, 215), 16)
                self.ui_text.draw(f"Ключевая механика: {entry['mechanic']}", tx, center_y - 24, BORDER_GOLD, 15)
                self.ui_text.draw(entry["desc"], tx, center_y - 95, TEXT_MUTED, 15, width=740, anchor_y="center", multiline=True)

                btn_title = "Личная колода карт"
                btn_sub = f"Открыть ({entry['total_cards']} карт)"
            else:
                is_discovered = (entry["name"] in self.seen_enemies)
                if is_discovered:
                    av = entry["avatar"]
                    av.base_x = 300
                    av.base_y = center_y - 10
                    av.draw()
                    self.ui_text.draw(entry["name"], tx, center_y + 105, BORDER_GOLD if is_boss else TEXT_PARCHMENT, 26,
                                      bold=True)
                    draw_stat_icon("hp", tx + 10, center_y + 62, size=11)
                    self.ui_text.draw(f"Базовое HP: {entry['hp']}", tx + 30, center_y + 56, (215, 110, 105), 18,
                                      bold=True)
                    self.ui_text.draw(f"Категория: {entry['tier']}", tx, center_y + 18, (185, 175, 165), 16)
                    self.ui_text.draw(f"Архетип спрайта: {entry['role']}", tx, center_y - 16, TEXT_MUTED, 15)
                    self.ui_text.draw(
                        "В бою выбирает одно из своих уникальных действий каждый ход. В режиме НГ+ здоровье и урон усиливаются.",
                        tx, center_y - 80, TEXT_MUTED, 15, width=740, anchor_y="center", multiline=True
                    )
                else:
                    # Тёмный силуэт неизвестного противника
                    arcade.draw_ellipse_filled(300, center_y - 75, 150, 36, (18, 16, 22))
                    arcade.draw_circle_filled(300, center_y + 5, 58, (14, 13, 18))
                    arcade.draw_circle_outline(300, center_y + 5, 58, (65, 45, 48) if is_boss else (55, 52, 60), 2)
                    self.ui_text.draw("?", 300, center_y + 5, TEXT_MUTED, 44, bold=True, anchor_x="center",
                                      anchor_y="center")

                    self.ui_text.draw("??? (НЕИЗВЕСТНЫЙ ПРОТИВНИК)", tx, center_y + 95, TEXT_MUTED, 25, bold=True)
                    self.ui_text.draw("HP: ???", tx, center_y + 50, (125, 85, 85), 18, bold=True)
                    self.ui_text.draw(f"Подсказка: {entry['tier']}", tx, center_y + 12, (145, 140, 135), 16)
                    self.ui_text.draw(
                        "Встретьте этого противника во время похода, чтобы раскрыть его облик, здоровье и арсенал атак.",
                        tx, center_y - 65, (110, 105, 105), 15, width=740, anchor_y="center", multiline=True
                    )

                btn_x, btn_y, btn_w, btn_h = 1460, center_y, 340, 110
                if is_discovered:
                    arcade.draw_rect_filled(arcade.XYWH(btn_x, btn_y, btn_w, btn_h), (34, 30, 44))
                    arcade.draw_rect_outline(arcade.XYWH(btn_x, btn_y, btn_w, btn_h), BORDER_GOLD, 2.5)
                    draw_stat_icon("deck", btn_x - 125, btn_y + 14, size=14)
                    self.ui_text.draw("Арсенал способностей", btn_x + 15, btn_y + 14, TEXT_PARCHMENT, 18, bold=True,
                                      anchor_x="center", anchor_y="center")
                    self.ui_text.draw(f"Открыть ({entry['actions_count']} действ.)", btn_x + 15, btn_y - 20,
                                      BORDER_GOLD, 15, anchor_x="center", anchor_y="center")
                    # Добавляем кнопку в список кликабельных ТОЛЬКО если враг открыт!
                    self.action_buttons.append((btn_x, btn_y, btn_w, btn_h, entry))
                else:
                    arcade.draw_rect_filled(arcade.XYWH(btn_x, btn_y, btn_w, btn_h), (20, 19, 25))
                    arcade.draw_rect_outline(arcade.XYWH(btn_x, btn_y, btn_w, btn_h), (55, 50, 56), 1.5)
                    self.ui_text.draw("ЗАБЛОКИРОВАНО", btn_x, btn_y + 12, TEXT_MUTED, 17, bold=True, anchor_x="center",
                                      anchor_y="center")
                    self.ui_text.draw("Не изучено в бою", btn_x, btn_y - 18, (95, 90, 90), 14, anchor_x="center",
                                      anchor_y="center")

                btn_title = "Арсенал способностей"
                btn_sub = f"Открыть ({entry['actions_count']} действ.)"

            btn_x, btn_y, btn_w, btn_h = 1460, center_y, 340, 110
            arcade.draw_rect_filled(arcade.XYWH(btn_x, btn_y, btn_w, btn_h), (34, 30, 44))
            arcade.draw_rect_outline(arcade.XYWH(btn_x, btn_y, btn_w, btn_h), BORDER_GOLD, 2.5)
            draw_stat_icon("deck", btn_x - 125, btn_y + 14, size=14)
            self.ui_text.draw(btn_title, btn_x + 15, btn_y + 14, TEXT_PARCHMENT, 18, bold=True, anchor_x="center", anchor_y="center")
            self.ui_text.draw(btn_sub, btn_x + 15, btn_y - 20, BORDER_GOLD, 15, anchor_x="center", anchor_y="center")
            self.action_buttons.append((btn_x, btn_y, btn_w, btn_h, entry))

        self._draw_fixed_header()
        if self.active_modal is not None:
            self._draw_modal()

    def _draw_fixed_header(self):
        header_h = 180 if self.main_tab == "HEROES" else 235
        arcade.draw_rect_filled(arcade.XYWH(SCREEN_WIDTH / 2, SCREEN_HEIGHT - header_h / 2, SCREEN_WIDTH, header_h), (14, 13, 18, 252))
        arcade.draw_line(0, SCREEN_HEIGHT - header_h, SCREEN_WIDTH, SCREEN_HEIGHT - header_h, BORDER_GOLD, 2)

        bx, by, bw, bh = self.back_btn
        arcade.draw_rect_filled(arcade.XYWH(bx, by, bw, bh), PANEL_DARK)
        arcade.draw_rect_outline(arcade.XYWH(bx, by, bw, bh), BORDER_GOLD, 2)
        self.ui_text.draw("← В меню", bx, by, TEXT_PARCHMENT, 17, bold=True, anchor_x="center", anchor_y="center")

        self.ui_text.draw("ЭНЦИКЛОПЕДИЯ ПЕРСОНАЖЕЙ И ВРАГОВ", SCREEN_WIDTH / 2, SCREEN_HEIGHT - 55, BORDER_GOLD, 32, bold=True, anchor_x="center", anchor_y="center")
        self.ui_text.draw("Колёсико мыши — прокрутка", SCREEN_WIDTH - 200, SCREEN_HEIGHT - 55, TEXT_MUTED, 14, anchor_x="center", anchor_y="center")

        # Главные вкладки: ГЕРОИ / ВРАГИ
        for tab in self.main_tab_btns:
            active = (self.main_tab == tab["id"])
            bg = (58, 48, 34) if active else PANEL_DARK
            b_col = arcade.color.YELLOW if active else BORDER_GOLD
            arcade.draw_rect_filled(arcade.XYWH(tab["x"], tab["y"], tab["w"], tab["h"]), bg)
            arcade.draw_rect_outline(arcade.XYWH(tab["x"], tab["y"], tab["w"], tab["h"]), b_col, 3 if active else 1.5)
            self.ui_text.draw(tab["label"], tab["x"], tab["y"], TEXT_PARCHMENT, 18, bold=True, anchor_x="center", anchor_y="center")

        # Подвкладки внутри ВРАГОВ: РЯДОВЫЕ МОБЫ / БОССЫ И ЭЛИТА + счётчик изученных врагов
        if self.main_tab == "ENEMIES":
            for sub in self.sub_tab_btns:
                active = (self.enemy_subtab == sub["id"])
                bg = (75, 28, 32) if active else (24, 22, 30)
                b_col = arcade.color.YELLOW if active else (140, 52, 56)
                arcade.draw_rect_filled(arcade.XYWH(sub["x"], sub["y"], sub["w"], sub["h"]), bg)
                arcade.draw_rect_outline(arcade.XYWH(sub["x"], sub["y"], sub["w"], sub["h"]), b_col,
                                         2.5 if active else 1.5)
                self.ui_text.draw(sub["label"], sub["x"], sub["y"], TEXT_PARCHMENT, 15, bold=True, anchor_x="center",
                                  anchor_y="center")

            cur_list = self._current_entries()
            opened = sum(1 for e in cur_list if e["name"] in self.seen_enemies)
            hidden = len(cur_list) - opened
            self.ui_text.draw(
                f"Изучено: {opened} из {len(cur_list)}  (Скрыто: {hidden})",
                SCREEN_WIDTH - 220, SCREEN_HEIGHT - 205, BORDER_GOLD, 15, bold=True, anchor_x="center",
                anchor_y="center"
            )

        if self.max_scroll > 0:
            track_h = SCREEN_HEIGHT - header_h - 40
            track_y = (SCREEN_HEIGHT - header_h) / 2
            arcade.draw_rect_filled(arcade.XYWH(SCREEN_WIDTH - 24, track_y, 10, track_h), (28, 26, 34))
            ratio = self.scroll_y / self.max_scroll
            thumb_h = max(60, track_h * 0.45)
            thumb_y = (SCREEN_HEIGHT - header_h - 15 - thumb_h / 2) - ratio * (track_h - thumb_h - 30)
            arcade.draw_rect_filled(arcade.XYWH(SCREEN_WIDTH - 24, thumb_y, 10, thumb_h), BORDER_GOLD)

    def _draw_modal(self):
        entry = self.active_modal
        arcade.draw_rect_filled(arcade.XYWH(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT),
                                (10, 9, 14, 228))

        # Увеличенная рамка окна (от y = 90 до y = 1000)
        arcade.draw_rect_filled(arcade.XYWH(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 5, 1520, 910), (20, 18, 26))
        arcade.draw_rect_outline(arcade.XYWH(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 5, 1520, 910), BORDER_GOLD, 3)

        title_prefix = "СТАРТОВАЯ КОЛОДА" if entry["kind"] == "HERO" else "ВОЗМОЖНЫЕ ДЕЙСТВИЯ В БОЮ"
        self.ui_text.draw(f"{title_prefix}: {entry['name'].upper()}", SCREEN_WIDTH / 2, 938, BORDER_GOLD, 26, bold=True,
                          anchor_x="center")

        cards = entry["cards"]
        cols, col_gap, row_gap, start_y = 5, 255, 355, 735
        for idx, c_item in enumerate(cards):
            row, col = idx // cols, idx % cols
            items_in_row = min(cols, len(cards) - row * cols)
            row_start_x = SCREEN_WIDTH / 2 - (items_in_row - 1) * col_gap / 2
            w = c_item["widget"]
            w.x = row_start_x + col * col_gap
            w.y = start_y - row * row_gap
            w.draw(can_afford=True)

            if c_item["qty"] is not None:
                self.ui_text.draw(f"×{c_item['qty']} в колоде", w.x, w.y - w.height / 2 - 22, BORDER_GOLD, 15,
                                  bold=True, anchor_x="center")

        cx, cy, cw, ch = self.modal_close_btn
        arcade.draw_rect_filled(arcade.XYWH(cx, cy, cw, ch), (105, 34, 34))
        arcade.draw_rect_outline(arcade.XYWH(cx, cy, cw, ch), BORDER_GOLD, 2)
        self.ui_text.draw("Закрыть окно", cx, cy, TEXT_PARCHMENT, 17, bold=True, anchor_x="center", anchor_y="center")

    def _go_back(self):
        if self.return_view is not None:
            self.window.show_view(self.return_view)
        else:
            from views.menu.menu_view import MenuView
            self.window.show_view(MenuView())

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        if self.active_modal is not None:
            cx, cy, cw, ch = self.modal_close_btn
            in_close = (cx - cw / 2 <= x <= cx + cw / 2 and cy - ch / 2 <= y <= cy + ch / 2)
            outside = not (SCREEN_WIDTH / 2 - 760 <= x <= SCREEN_WIDTH / 2 + 760 and 130 <= y <= 970)
            if in_close or outside:
                self.active_modal = None
            return

        bx, by, bw, bh = self.back_btn
        if bx - bw / 2 <= x <= bx + bw / 2 and by - bh / 2 <= y <= by + bh / 2:
            self._go_back()
            return

        for tab in self.main_tab_btns:
            if tab["x"] - tab["w"] / 2 <= x <= tab["x"] + tab["w"] / 2 and tab["y"] - tab["h"] / 2 <= y <= tab["y"] + tab["h"] / 2:
                if self.main_tab != tab["id"]:
                    self.main_tab = tab["id"]
                    self._recalc_scroll()
                return

        if self.main_tab == "ENEMIES":
            for sub in self.sub_tab_btns:
                if sub["x"] - sub["w"] / 2 <= x <= sub["x"] + sub["w"] / 2 and sub["y"] - sub["h"] / 2 <= y <= sub["y"] + sub["h"] / 2:
                    if self.enemy_subtab != sub["id"]:
                        self.enemy_subtab = sub["id"]
                        self._recalc_scroll()
                    return

        header_limit = SCREEN_HEIGHT - (180 if self.main_tab == "HEROES" else 235)
        if y < header_limit:
            for btn_x, btn_y, btn_w, btn_h, entry in self.action_buttons:
                if btn_x - btn_w / 2 <= x <= btn_x + btn_w / 2 and btn_y - btn_h / 2 <= y <= btn_y + btn_h / 2:
                    if entry["kind"] == "ENEMY" and entry["name"] not in self.seen_enemies:
                        return
                    self.active_modal = entry
                    return

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            if self.active_modal is not None:
                self.active_modal = None
            else:
                self._go_back()
        elif self.active_modal is None:
            if key == arcade.key.DOWN:
                self.scroll_y = min(self.max_scroll, self.scroll_y + 80)
            elif key == arcade.key.UP:
                self.scroll_y = max(0.0, self.scroll_y - 80)
