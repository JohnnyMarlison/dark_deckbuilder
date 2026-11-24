import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BG_DARK, PANEL_DARK, PANEL_ENEMY, BORDER_GOLD, TEXT_PARCHMENT, TEXT_MUTED
from core.card import Card
from core.effects import DamageEffect, BlockEffect
from visuals.avatar import CharacterAvatar
from visuals.card_widget import CardWidget
from visuals.icons import draw_enemy_choice_icons


TUTORIAL_STEPS = (
    {
        "title": "ЭТАП 1 ИЗ 4: ВЫБОР ГЕРОЯ И СВОЯ КОЛОДА",
        "subtitle": "Каждый герой обладает уникальным стилем боя и стартовой колодой.",
        "lines": (
            "• В начале похода вы выбираете одного из 4 Избранных (Воин, Элементалист, Паладин или Ассасин).",
            "• У каждого героя свой запас Здоровья (HP), Стамины (энергии на ход) и набор карт.",
            "• Наведите курсор на героя на экране выбора, чтобы изучить его сложность и главную механику.",
        ),
    },
    {
        "title": "ЭТАП 2 ИЗ 4: РОЗЫГРЫШ КАРТ И СТАМИНА",
        "subtitle": "В свой ход вы тянете 4 карты из колоды и тратите стамину на их применение.",
        "lines": (
            "• В левом верхнем углу каждой карты указана её цена в Стамине (золотой кружок).",
            "• Красные карты — Атака, Синие — Защита (броня), Фиолетовые — Заклинания, Зеленые — Исцеление.",
            "• Броня поглощает входящий урон врага, но сгорает в начале вашего следующего хода!",
        ),
    },
    {
        "title": "ЭТАП 3 ИЗ 4: СКРЫТЫЙ ХОД ПРОТИВНИКА",
        "subtitle": "Враги не раскрывают свои карты заранее — вам придется читать их повадки.",
        "lines": (
            "• Пока идет ваш ход, над врагом перебираются 4 тусклые иконки — он взвешивает варианты.",
            "• Нажмите «Закончить ход», когда потратите стамину. После этого враг разыграет свою карту.",
            "• Внимание: некоторые враги пробивают броню насквозь, лечатся или воруют вашу стамину!",
        ),
    },
    {
        "title": "ЭТАП 4 ИЗ 4: АНАЛИЗ, 3 ЭТАПА И ЛЕТОПИСЬ ПОБЕД",
        "subtitle": "Изучайте прошлый ход врага и пройдите 3 уровня, чтобы сразить Владыку Тьмы.",
        "lines": (
            "• В правой верхней панели всегда записан «Прошлый ход» врага — используйте это для тактики.",
            "• Поход состоит из 3 этапов: 2 рядовых чудовища и финальный Босс на 3-м уровне.",
            "• После победы над Боссом рекорд запишется в Летопись, а вы сможете рискнуть и пойти в НГ+!",
        ),
    },
)


class TutorialView(arcade.View):
    def __init__(self):
        super().__init__()
        self.step = 0
        self.back_menu_btn = (150, SCREEN_HEIGHT - 65, 200, 50)
        self.prev_btn = (SCREEN_WIDTH / 2 - 220, 140, 240, 58)
        self.next_btn = (SCREEN_WIDTH / 2 + 220, 140, 240, 58)

        # Демонстрационные объекты для наглядности этапов
        self.demo_hero = CharacterAvatar("Паладин", 560, 440, scale=1.45, flip=False)
        self.demo_enemy = CharacterAvatar("Некромант", SCREEN_WIDTH - 560, 440, scale=1.55, flip=True)
        self.demo_atk = CardWidget(Card("d1", "Удар мечом", "Атака", 1, "Наносит 7 урона", [DamageEffect(7)]), x=760, y=450, cost=1)
        self.demo_def = CardWidget(Card("d2", "Глухая оборона", "Защита", 1, "Дает 6 брони", [BlockEffect(6)]), x=960, y=450, cost=1)
        self.demo_heal = CardWidget(Card("d3", "Молитва света", "Исцеление", 1, "Лечит 8 HP", []), x=1160, y=450, cost=1)

    def on_show_view(self):
        arcade.set_background_color(BG_DARK)

    def on_update(self, delta_time: float):
        self.demo_hero.update(delta_time)
        self.demo_enemy.update(delta_time)

    def on_draw(self):
        self.clear()

        # Кнопка возврата в главное меню
        bx, by, bw, bh = self.back_menu_btn
        arcade.draw_rect_filled(arcade.XYWH(bx, by, bw, bh), PANEL_DARK)
        arcade.draw_rect_outline(arcade.XYWH(bx, by, bw, bh), BORDER_GOLD, 2)
        arcade.draw_text("← В меню", bx, by, TEXT_PARCHMENT, 17, bold=True, anchor_x="center", anchor_y="center")

        # Индикатор прогресса этапов (4 точки сверху)
        for i in range(len(TUTORIAL_STEPS)):
            dot_x = SCREEN_WIDTH / 2 - 90 + i * 60
            is_cur = (i == self.step)
            arcade.draw_circle_filled(dot_x, SCREEN_HEIGHT - 65, 12 if is_cur else 8, BORDER_GOLD if is_cur else (65, 60, 55))

        data = TUTORIAL_STEPS[self.step]

        # Главная карточка текущего этапа обучения
        arcade.draw_rect_filled(arcade.XYWH(SCREEN_WIDTH / 2, 565, 1340, 680), PANEL_DARK)
        arcade.draw_rect_outline(arcade.XYWH(SCREEN_WIDTH / 2, 565, 1340, 680), BORDER_GOLD, 2.5)

        arcade.draw_text(data["title"], SCREEN_WIDTH / 2, 845, BORDER_GOLD, 28, bold=True, anchor_x="center")
        arcade.draw_text(data["subtitle"], SCREEN_WIDTH / 2, 795, TEXT_PARCHMENT, 18, anchor_x="center")

        # Визуальная демонстрация для каждого этапа
        if self.step == 0:
            self.demo_hero.base_x = SCREEN_WIDTH / 2
            self.demo_hero.draw()
            arcade.draw_text("Наведите курсор на героя при выборе — откроется его досье!", SCREEN_WIDTH / 2, 330, BORDER_GOLD, 16, anchor_x="center")

        elif self.step == 1:
            self.demo_atk.draw(can_afford=True)
            self.demo_def.draw(can_afford=True)
            self.demo_heal.draw(can_afford=True)

        elif self.step == 2:
            self.demo_hero.base_x = 640
            self.demo_hero.draw()
            self.demo_enemy.draw()
            draw_enemy_choice_icons(self.demo_enemy.base_x, self.demo_enemy.base_y + 155, self.demo_enemy.time)
            arcade.draw_text("Враг скрывает выбор до конца вашего хода", SCREEN_WIDTH / 2, 330, (215, 110, 105), 16, anchor_x="center")

        elif self.step == 3:
            arcade.draw_rect_filled(arcade.XYWH(SCREEN_WIDTH / 2, 460, 520, 150), PANEL_ENEMY)
            arcade.draw_rect_outline(arcade.XYWH(SCREEN_WIDTH / 2, 460, 520, 150), (140, 42, 46), 2)
            arcade.draw_text("БОСС: Архи-Некромант", SCREEN_WIDTH / 2, 505, TEXT_PARCHMENT, 18, bold=True, anchor_x="center")
            arcade.draw_text("Прошлый ход:\n[Заклинание] Жатва душ: Наносит 14 урона, Лечит 12 HP", SCREEN_WIDTH / 2, 440, TEXT_PARCHMENT, 14, width=480, align="center", anchor_x="center", anchor_y="center", multiline=True)

        # Текстовые подсказки снизу карточки
        for idx, line in enumerate(data["lines"]):
            arcade.draw_text(line, 360, 685 - idx * 34, TEXT_PARCHMENT, 16, anchor_x="left")

        # Кнопки навигации Назад / Далее
        if self.step > 0:
            px, py, pw, ph = self.prev_btn
            arcade.draw_rect_filled(arcade.XYWH(px, py, pw, ph), (36, 52, 74))
            arcade.draw_rect_outline(arcade.XYWH(px, py, pw, ph), BORDER_GOLD, 2)
            arcade.draw_text("← Предыдущий этап", px, py, TEXT_PARCHMENT, 17, bold=True, anchor_x="center", anchor_y="center")

        nx, ny, nw, nh = self.next_btn
        is_last = (self.step == len(TUTORIAL_STEPS) - 1)
        arcade.draw_rect_filled(arcade.XYWH(nx, ny, nw, nh), (38, 68, 52))
        arcade.draw_rect_outline(arcade.XYWH(nx, ny, nw, nh), BORDER_GOLD, 2)
        btn_label = "В бой (Выбор героя) →" if is_last else "Следующий этап →"
        arcade.draw_text(btn_label, nx, ny, TEXT_PARCHMENT, 17, bold=True, anchor_x="center", anchor_y="center")

    def _go_menu(self):
        from views.menu_view import MenuView
        self.window.show_view(MenuView())

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        bx, by, bw, bh = self.back_menu_btn
        if bx - bw / 2 <= x <= bx + bw / 2 and by - bh / 2 <= y <= by + bh / 2:
            self._go_menu()
            return

        if self.step > 0:
            px, py, pw, ph = self.prev_btn
            if px - pw / 2 <= x <= px + pw / 2 and py - ph / 2 <= y <= py + ph / 2:
                self.step -= 1
                return

        nx, ny, nw, nh = self.next_btn
        if nx - nw / 2 <= x <= nx + nw / 2 and ny - nh / 2 <= y <= ny + nh / 2:
            if self.step < len(TUTORIAL_STEPS) - 1:
                self.step += 1
            else:
                from views.hero_select_view import HeroSelectView
                self.window.show_view(HeroSelectView())

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self._go_menu()
        elif key == arcade.key.RIGHT and self.step < len(TUTORIAL_STEPS) - 1:
            self.step += 1
        elif key == arcade.key.LEFT and self.step > 0:
            self.step -= 1
