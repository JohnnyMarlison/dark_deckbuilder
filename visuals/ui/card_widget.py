import arcade
from config import TYPE_COLORS, BORDER_GOLD, TEXT_PARCHMENT
from visuals.ui.icons import draw_card_icon

CLASS_ACCENTS = {
    "ВОИН": (175, 185, 195),          # Стальной серый
    "ЭЛЕМЕНТАЛИСТ": (65, 185, 225),   # Стихийный лазурно-бирюзовый
    "ПАЛАДИН": (245, 220, 120),       # Сияющее золото света
    "АССАСИН": (170, 100, 225),       # Сумеречный фиолет
}


class CardWidget:
    """Оптимизированный виджет карты с кэшированием объектов arcade.Text."""

    def __init__(self, card_data, x: float = 0.0, y: float = 0.0, cost: int | None = None):
        from core.effects import SelfDamageEffect
        self.hp_cost = sum(
            e.value for e in getattr(card_data, "effects", [])
            if isinstance(e, SelfDamageEffect)
        )
        self._txt_hp_cost = arcade.Text(
            f"-{self.hp_cost}", x, y, TEXT_PARCHMENT, 13, bold=True, anchor_x="center", anchor_y="center"
        )

        self.hero_class = getattr(card_data, "hero_class", "")
        self.neutral = getattr(card_data, "neutral", True)
        self._txt_class = arcade.Text(
            self.hero_class,
            x,
            y,
            BORDER_GOLD,
            11,
            font_name="Arial",
            bold=True,
            anchor_x="center",
            anchor_y="center",
        )

        self.data = card_data
        self.name = card_data.name
        self.card_type = getattr(card_data, "card_type", getattr(card_data, "action_type", "Атака"))
        self.cost = cost if cost is not None else getattr(card_data, "cost", 0)
        self.desc = card_data.desc

        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.width = 224
        self.height = 310
        self.hovered = False
        self.is_playing = False

        # Создаем текстовые объекты ОДИН РАЗ (устраняет PerformanceWarning)
        self._txt_cost = arcade.Text(
            str(self.cost), x, y, (15, 14, 18), 16, bold=True, anchor_x="center", anchor_y="center"
        )
        self._txt_type = arcade.Text(
            self.card_type.upper(),
            x,
            y,
            (215, 208, 195),
            13,
            font_name="Arial",
            bold=True,
            anchor_x="center",
            anchor_y="center",
        )

        self._txt_name = arcade.Text(
            self.name, x, y, TEXT_PARCHMENT, 14,
            width=int(self.width - 20), align="center", bold=True,
            anchor_x="center", anchor_y="center", multiline=True
        )

        self._txt_desc = arcade.Text(
            self.desc, x, y, TEXT_PARCHMENT, 13,
            width=int(self.width - 26), align="center", anchor_x="center", anchor_y="center", multiline=True
        )

    def is_clicked(self, mx: float, my: float) -> bool:
        # Проверяем хитбокс по целевой позиции, чтобы избежать двойных кликов при перекладке руки
        cx = self.x if self.hovered else self.target_x
        cy = self.y if self.hovered else self.target_y
        return (
            cx - self.width / 2 <= mx <= cx + self.width / 2
            and cy - self.height / 2 <= my <= cy + self.height / 2
        )

    def contains_point(self, x: float, y: float) -> bool:
        if hasattr(self, "hit_test"):
            return self.hit_test(x, y)
        hw = getattr(self, "width", 190) / 2
        hh = getattr(self, "height", 270) / 2
        return self.x - hw <= x <= self.x + hw and self.y - hh <= y <= self.y + hh


    def update(self, dt: float):
        goal_y = self.target_y + (28 if self.hovered and not self.is_playing else 0)
        speed = 14.0 if self.is_playing else 10.0
        self.x += (self.target_x - self.x) * min(1.0, dt * speed)
        self.y += (goal_y - self.y) * min(1.0, dt * speed)

    def draw(self, can_afford: bool = True):
        scale = 1.07 if (self.hovered or self.is_playing) else 1.0
        w = self.width * scale
        h = self.height * scale

        bg_color = TYPE_COLORS.get(self.card_type, (45, 42, 52))
        border_color = arcade.color.YELLOW if self.hovered else (BORDER_GOLD if can_afford else (80, 75, 70))

        # 1. Фон и внешняя рамка карты
        arcade.draw_rect_filled(arcade.XYWH(self.x, self.y, w, h), bg_color)
        arcade.draw_rect_outline(arcade.XYWH(self.x, self.y, w, h), border_color, 3)

        # 2. Внутренняя классовая рамка (рисуется ДО кружков стоимости, чтобы не заезжать на них)
        is_hero_card = (not self.neutral and bool(self.hero_class))
        hero_color = CLASS_ACCENTS.get(self.hero_class, BORDER_GOLD)

        # 1. Главная внешняя рамка: в цвет героя для классовых карт, золотая для нейтральных
        if self.hovered:
            outer_border = arcade.color.YELLOW
        elif is_hero_card:
            outer_border = hero_color if can_afford else (95, 95, 105)
        else:
            outer_border = BORDER_GOLD if can_afford else (80, 75, 70)

        arcade.draw_rect_filled(arcade.XYWH(self.x, self.y, w, h), bg_color)
        arcade.draw_rect_outline(arcade.XYWH(self.x, self.y, w, h), outer_border, 3)

        # 2. Внутреннее обрамление с угловыми заклёпками — золотистое (BORDER_GOLD)
        if is_hero_card:
            inner_w = w - 14
            inner_h = h - 14
            arcade.draw_rect_outline(arcade.XYWH(self.x, self.y, inner_w, inner_h), BORDER_GOLD, 1.5)
            for dx in (-inner_w / 2, inner_w / 2):
                for dy in (-inner_h / 2, inner_h / 2):
                    arcade.draw_circle_filled(self.x + dx, self.y + dy, 3.5, BORDER_GOLD)

        # 3. Медальоны стоимости (смещены на +4px вправо и -4px вниз от старых 25/-24 -> 29/-28)
        cost_x = self.x - w / 2 + 29
        cost_y = self.y + h / 2 - 28
        cost_bg = BORDER_GOLD if can_afford else (60, 58, 62)
        arcade.draw_circle_filled(cost_x, cost_y, 17, cost_bg)
        self._txt_cost.x = round(cost_x)
        self._txt_cost.y = round(cost_y)
        self._txt_cost.draw()

        # Цена здоровья справа сверху (смещена внутрь карты зеркально, чтобы не касаться рамки)
        if self.hp_cost > 0:
            hp_x = self.x + w / 2 - 29
            arcade.draw_circle_filled(hp_x, cost_y, 17, (155, 32, 36))
            arcade.draw_circle_outline(hp_x, cost_y, 17, (235, 110, 110), 1.5)
            self._txt_hp_cost.x = round(hp_x)
            self._txt_hp_cost.y = round(cost_y)
            self._txt_hp_cost.draw()

        # 4. Тип, название, иконка и описание
        self._txt_type.x = round(self.x)
        self._txt_type.y = round(self.y + h / 2 - 52)
        self._txt_type.draw()

        self._txt_name.x = round(self.x)
        self._txt_name.y = round(self.y + 62)
        self._txt_name.draw()

        arcade.draw_circle_filled(self.x, self.y + 4, 32, (0, 0, 0, 85))
        draw_card_icon(self.card_type, self.x, self.y + 4, size=29)

        self._txt_desc.x = round(self.x)
        self._txt_desc.y = round(self.y - 74)
        self._txt_desc.draw()

        # 5. Нижняя плашка с названием класса (динамическая ширина + боковые отступы)
        if is_hero_card:
            plate_y = self.y - h / 2 + 16
            text_w = getattr(self._txt_class, "content_width", len(self.hero_class) * 8.5)
            plate_w = max(96, min(w - 26, text_w + 32))
            plate_h = 20
            arcade.draw_rect_filled(arcade.XYWH(self.x, plate_y, plate_w, plate_h), (18, 16, 24, 242))
            arcade.draw_rect_outline(arcade.XYWH(self.x, plate_y, plate_w, plate_h), BORDER_GOLD, 1.2)
            self._txt_class.x = round(self.x)
            self._txt_class.y = round(plate_y)
            self._txt_class.draw()



