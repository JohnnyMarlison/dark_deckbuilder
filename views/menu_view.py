import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BG_DARK, BORDER_GOLD, TEXT_PARCHMENT, TEXT_MUTED
from core.card import Card
from core.effects import DamageEffect
from visuals.avatar import CharacterAvatar
from visuals.card_widget import CardWidget
from visuals.particles import SpellProjectile, FloatingEffect
from visuals.text_cache import TextCache

HERO_SHOWCASE = (
    ("Воин", "Сокрушение", "Атака", 2, "Мощный удар клинком", (168, 134, 62)),
    ("Элементалист", "Огненный шар", "Заклинание", 2, "Испепеляющее пламя", (215, 85, 30)),
    ("Паладин", "Небесный гнев", "Заклинание", 2, "Кара небесного света", (220, 195, 95)),
    ("Ассасин", "Удар в спину", "Атака", 2, "Смертоносный выпад", (75, 205, 125)),
)

ENEMY_SHOWCASE = (
    ("Гоблин", "Ржавый заточ", "Атака", "Подлый удар", (180, 185, 190)),
    ("Огр", "Пролом черепа", "Атака", "Удар дубиной", (165, 115, 65)),
    ("Скелет-стрелок", "Проклятая стрела", "Атака", "Выстрел из тьмы", (110, 220, 130)),
    ("Слизняк", "Кислотный плевок", "Заклинание", "Едкая слизь", (90, 210, 90)),
    ("Злой Волшебник", "Черный метеор", "Заклинание", "Темная магия", (175, 45, 155)),
    ("Некромант", "Жатва душ", "Заклинание", "Некротический луч", (70, 210, 120)),
    ("Цербер", "Дыхание Тартара", "Заклинание", "Адское пламя", (215, 65, 35)),
    ("Костяной Гигант", "Обвал склепа", "Атака", "Сокрушение", (195, 188, 170)),
)


class MenuView(arcade.View):
    def __init__(self):

        super().__init__()
        self.buttons = (
            {"label": "ИГРАТЬ", "action": "PLAY", "y": 635, "color": (38, 68, 52)},
            {"label": "КАК ИГРАТЬ", "action": "TUTORIAL", "y": 545, "color": (74, 58, 32)},
            {"label": "РЕКОРДЫ", "action": "RECORDS", "y": 455, "color": (36, 52, 74)},
            {"label": "ВЫХОД", "action": "EXIT", "y": 365, "color": (105, 30, 32)},
        )

        self.ui_text = TextCache()

        self.hero_idx = 0
        self.enemy_idx = 0
        self.left_avatar: CharacterAvatar | None = None
        self.right_avatar: CharacterAvatar | None = None
        self.left_card: CardWidget | None = None
        self.right_card: CardWidget | None = None

        self.projectiles: list[SpellProjectile] = []
        self.effects: list[FloatingEffect] = []

        self.hero_cast_timer = 1.0
        self.enemy_cast_timer = 2.4
        self.hero_swap_timer = 4.2
        self.enemy_swap_timer = 5.5

        self._spawn_hero()
        self._spawn_enemy()

    def on_show_view(self):
        arcade.set_background_color(BG_DARK)

    def _spawn_hero(self):
        role = HERO_SHOWCASE[self.hero_idx][0]
        self.left_avatar = CharacterAvatar(role, 240, 520, scale=1.55, flip=False)
        self.effects.append(FloatingEffect(240, 520, "", (140, 130, 115)))

    def _spawn_enemy(self):
        role = ENEMY_SHOWCASE[self.enemy_idx][0]
        self.right_avatar = CharacterAvatar(role, SCREEN_WIDTH - 240, 520, scale=1.55, flip=True)
        self.effects.append(FloatingEffect(SCREEN_WIDTH - 240, 520, "", (145, 55, 55)))

    def _trigger_hero_cast(self):
        role, cname, ctype, cost, desc, color = HERO_SHOWCASE[self.hero_idx]
        if self.left_avatar:
            self.left_avatar.trigger("casting", 0.55)
        dummy = Card("demo", cname, ctype, cost, desc, [DamageEffect(10)])
        w = CardWidget(dummy, x=240, y=530, cost=cost)
        w.target_x = 465
        w.target_y = 550
        w.is_playing = True
        self.left_card = w
        self.projectiles.append(SpellProjectile(275, 540, SCREEN_WIDTH - 265, 540, color, radius=14))

    def _trigger_enemy_cast(self):
        role, cname, ctype, desc, color = ENEMY_SHOWCASE[self.enemy_idx]
        if self.right_avatar:
            self.right_avatar.trigger("casting", 0.55)
        dummy = Card("demo_e", cname, ctype, 0, desc, [DamageEffect(10)])
        w = CardWidget(dummy, x=SCREEN_WIDTH - 240, y=530, cost=0)
        w.target_x = SCREEN_WIDTH - 465
        w.target_y = 550
        w.is_playing = True
        self.right_card = w
        self.projectiles.append(SpellProjectile(SCREEN_WIDTH - 275, 540, 265, 540, color, radius=14))

    def on_update(self, delta_time: float):
        if self.left_avatar:
            self.left_avatar.update(delta_time)
        if self.right_avatar:
            self.right_avatar.update(delta_time)

        self.hero_cast_timer -= delta_time
        if self.hero_cast_timer <= 0:
            self._trigger_hero_cast()
            self.hero_cast_timer = 3.8

        self.hero_swap_timer -= delta_time
        if self.hero_swap_timer <= 0:
            self.hero_idx = (self.hero_idx + 1) % len(HERO_SHOWCASE)
            self._spawn_hero()
            self.left_card = None
            self.hero_swap_timer = 4.5
            self.hero_cast_timer = 0.8

        self.enemy_cast_timer -= delta_time
        if self.enemy_cast_timer <= 0:
            self._trigger_enemy_cast()
            self.enemy_cast_timer = 3.8

        self.enemy_swap_timer -= delta_time
        if self.enemy_swap_timer <= 0:
            self.enemy_idx = (self.enemy_idx + 1) % len(ENEMY_SHOWCASE)
            self._spawn_enemy()
            self.right_card = None
            self.enemy_swap_timer = 4.8
            self.enemy_cast_timer = 0.9

        if self.left_card:
            self.left_card.update(delta_time)
        if self.right_card:
            self.right_card.update(delta_time)

        active_projs = []
        for p in self.projectiles:
            if p.update(delta_time):
                active_projs.append(p)
            else:
                if p.end_x > SCREEN_WIDTH / 2 and self.right_avatar:
                    self.right_avatar.trigger("hurt", 0.35)
                elif p.end_x < SCREEN_WIDTH / 2 and self.left_avatar:
                    self.left_avatar.trigger("hurt", 0.35)
        self.projectiles = active_projs

        self.effects = [e for e in self.effects if e.update(delta_time)]

    def on_draw(self):
        self.clear()

        arcade.draw_ellipse_filled(240, 455, 290, 80, (22, 20, 28, 190))
        arcade.draw_ellipse_filled(SCREEN_WIDTH - 240, 455, 290, 80, (28, 18, 22, 190))

        if self.left_avatar:
            self.left_avatar.draw()
        if self.right_avatar:
            self.right_avatar.draw()

        if self.left_card:
            self.left_card.draw(can_afford=True)
        if self.right_card:
            self.right_card.draw(can_afford=True)

        for p in self.projectiles:
            p.draw()
        for e in self.effects:
            e.draw()

        # Центральная подложка меню (центр по Y = 565, ширина = 660, высота = 580 -> границы от 275 до 855)
        arcade.draw_rect_filled(arcade.XYWH(SCREEN_WIDTH / 2, 575, 660, 620), (14, 13, 18, 225))
        arcade.draw_rect_outline(arcade.XYWH(SCREEN_WIDTH / 2, 575, 660, 620), (75, 62, 48, 160), 2)

        self.ui_text.draw("ДАНЖКРАУЛЕР", SCREEN_WIDTH / 2, 815, BORDER_GOLD, 38, bold=True, anchor_x="center")
        self.ui_text.draw("Мрачные подземелья • Модульная архитектура v3", SCREEN_WIDTH / 2, 760, TEXT_MUTED, 16,
                         anchor_x="center")

        for btn in self.buttons:
            arcade.draw_rect_filled(arcade.XYWH(SCREEN_WIDTH / 2, btn["y"], 340, 72), btn["color"])
            arcade.draw_rect_outline(arcade.XYWH(SCREEN_WIDTH / 2, btn["y"], 340, 72), BORDER_GOLD, 2.5)
            self.ui_text.draw(btn["label"], SCREEN_WIDTH / 2, btn["y"], TEXT_PARCHMENT, 23, bold=True, anchor_x="center", anchor_y="center")

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return
        for btn in self.buttons:
            if SCREEN_WIDTH / 2 - 170 <= x <= SCREEN_WIDTH / 2 + 170 and btn["y"] - 36 <= y <= btn["y"] + 36:
                if btn["action"] == "PLAY":
                    from views.hero_select_view import HeroSelectView
                    self.window.show_view(HeroSelectView())
                elif btn["action"] == "TUTORIAL":
                    from views.tutorial_view import TutorialView
                    self.window.show_view(TutorialView())

                elif btn["action"] == "RECORDS":
                    from views.records_view import RecordsView
                    self.window.show_view(RecordsView())
                elif btn["action"] == "EXIT":
                    arcade.close_window()
                return
