import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BG_DARK, PANEL_DARK, BORDER_GOLD, TEXT_PARCHMENT, TEXT_MUTED
from core.hero import load_hero_templates
from core.run_state import RunState
from visuals.avatar import CharacterAvatar


class HeroSelectView(arcade.View):
    def __init__(self):
        super().__init__()
        self.templates = load_hero_templates()
        self.back_btn = (150, SCREEN_HEIGHT - 65, 200, 50)
        self.hero_cards = []
        self.hovered_hero: dict | None = None

        start_x = 345
        gap = 410
        for i, (name, info) in enumerate(self.templates.items()):
            bx = start_x + i * gap
            self.hero_cards.append({
                "name": name,
                "info": info,
                "x": bx,
                "y": 710,
                "w": 330,
                "h": 310,
                "avatar": CharacterAvatar(name, bx, 380, scale=1.5),
            })

    def on_show_view(self):
        arcade.set_background_color(BG_DARK)

    def on_update(self, delta_time: float):
        for item in self.hero_cards:
            item["avatar"].update(delta_time)

    def on_draw(self):
        self.clear()
        bx, by, bw, bh = self.back_btn
        arcade.draw_rect_filled(arcade.XYWH(bx, by, bw, bh), PANEL_DARK)
        arcade.draw_rect_outline(arcade.XYWH(bx, by, bw, bh), BORDER_GOLD, 2)
        arcade.draw_text("← В меню", bx, by, TEXT_PARCHMENT, 17, bold=True, anchor_x="center", anchor_y="center")

        arcade.draw_text("ВЫБЕРИТЕ ИЗБРАННОГО", SCREEN_WIDTH / 2, SCREEN_HEIGHT - 85, BORDER_GOLD, 36, bold=True, anchor_x="center")

        for item in self.hero_cards:
            info = item["info"]
            is_hovered = (self.hovered_hero == item)
            border_col = arcade.color.YELLOW if is_hovered else BORDER_GOLD
            border_w = 4 if is_hovered else 2

            arcade.draw_rect_filled(arcade.XYWH(item["x"], item["y"], item["w"], item["h"]), PANEL_DARK)
            arcade.draw_rect_outline(arcade.XYWH(item["x"], item["y"], item["w"], item["h"]), border_col, border_w)

            arcade.draw_text(item["name"], item["x"], item["y"] + 115, TEXT_PARCHMENT, 24, bold=True, anchor_x="center")
            arcade.draw_text(f"HP: {info['hp']}  |  Стамина: {info['stamina']}", item["x"], item["y"] + 70, (115, 185, 130), 16, anchor_x="center")
            arcade.draw_text(f"Сложность: {info.get('difficulty', 'Средняя')}", item["x"], item["y"] + 30, BORDER_GOLD, 14, anchor_x="center")
            arcade.draw_text(f"Стиль: {info.get('style', '')}", item["x"], item["y"] - 20, TEXT_MUTED, 14, width=item["w"] - 32, align="center", anchor_x="center", anchor_y="center", multiline=True)
            arcade.draw_text(f"Карт в колоде: {len(info['deck'])}", item["x"], item["y"] - 115, TEXT_PARCHMENT, 14, anchor_x="center")
            item["avatar"].draw()

        # Нижняя панель подробного досье при наведении на героя
        arcade.draw_rect_filled(arcade.XYWH(SCREEN_WIDTH / 2, 125, 1560, 175), (20, 18, 26, 240))
        arcade.draw_rect_outline(arcade.XYWH(SCREEN_WIDTH / 2, 125, 1560, 175), BORDER_GOLD, 2)

        if self.hovered_hero:
            hname = self.hovered_hero["name"]
            hinfo = self.hovered_hero["info"]
            arcade.draw_text(
                f"{hname.upper()}  •  Главная механика: {hinfo.get('mechanic', '')}",
                220, 175, BORDER_GOLD, 19, bold=True, anchor_x="left"
            )
            arcade.draw_text(
                f"Сложность освоения: {hinfo.get('difficulty', '')}   |   Стиль игры: {hinfo.get('style', '')}",
                220, 140, (115, 185, 130), 16, anchor_x="left"
            )
            arcade.draw_text(
                hinfo.get("desc", ""),
                220, 88, TEXT_PARCHMENT, 16, width=1480, anchor_x="left", anchor_y="center", multiline=True
            )
        else:
            arcade.draw_text(
                "Наведите курсор на любого героя, чтобы изучить его стиль игры, механику и сложность освоения",
                SCREEN_WIDTH / 2, 125, TEXT_MUTED, 18, anchor_x="center", anchor_y="center"
            )

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        found = None
        for item in self.hero_cards:
            in_card = item["x"] - item["w"] / 2 <= x <= item["x"] + item["w"] / 2 and item["y"] - item["h"] / 2 <= y <= item["y"] + item["h"] / 2
            in_avatar = abs(x - item["avatar"].base_x) <= 75 and abs(y - item["avatar"].base_y) <= 95
            if in_card or in_avatar:
                found = item
                item["avatar"].state = "thinking"
            else:
                item["avatar"].state = "idle"
        self.hovered_hero = found

    def _go_back(self):
        from views.menu_view import MenuView
        self.window.show_view(MenuView())

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return
        bx, by, bw, bh = self.back_btn
        if bx - bw / 2 <= x <= bx + bw / 2 and by - bh / 2 <= y <= by + bh / 2:
            self._go_back()
            return

        if self.hovered_hero:
            from views.battle_view import BattleView
            self.window.show_view(BattleView(RunState(self.hovered_hero["name"])))

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self._go_back()
