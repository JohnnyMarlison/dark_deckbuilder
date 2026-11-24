import arcade
from config import TYPE_COLORS, BORDER_GOLD, TEXT_PARCHMENT
from visuals.icons import draw_card_icon


class CardWidget:
    """Оптимизированный виджет карты с кэшированием объектов arcade.Text."""

    def __init__(self, card_data, x: float = 0.0, y: float = 0.0, cost: int | None = None):
        self.data = card_data
        self.name = card_data.name
        self.card_type = getattr(card_data, "card_type", getattr(card_data, "action_type", "Атака"))
        self.cost = cost if cost is not None else getattr(card_data, "cost", 0)
        self.desc = card_data.desc

        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.width = 200
        self.height = 285
        self.hovered = False
        self.is_playing = False

        # Создаем текстовые объекты ОДИН РАЗ (устраняет PerformanceWarning)
        self._txt_cost = arcade.Text(
            str(self.cost), x, y, (15, 14, 18), 16, bold=True, anchor_x="center", anchor_y="center"
        )
        self._txt_type = arcade.Text(
            self.card_type.upper(), x, y, (190, 182, 170), 11, bold=True, anchor_x="center", anchor_y="center"
        )
        self._txt_name = arcade.Text(
            self.name, x, y, TEXT_PARCHMENT, 15, bold=True, anchor_x="center", anchor_y="center"
        )
        self._txt_desc = arcade.Text(
            self.desc, x, y, TEXT_PARCHMENT, 13,
            width=int(self.width - 24), align="center", anchor_x="center", anchor_y="center", multiline=True
        )

    def refresh_text(self):
        """Обновляет кэш текста, если характеристики карты изменились в бою."""
        self._txt_cost.text = str(self.cost)
        self._txt_name.text = self.name
        self._txt_desc.text = self.desc

    def is_clicked(self, mx: float, my: float) -> bool:
        # Проверяем хитбокс по целевой позиции, чтобы избежать двойных кликов при перекладке руки
        cx = self.x if self.hovered else self.target_x
        cy = self.y if self.hovered else self.target_y
        return (
            cx - self.width / 2 <= mx <= cx + self.width / 2
            and cy - self.height / 2 <= my <= cy + self.height / 2
        )

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

        arcade.draw_rect_filled(arcade.XYWH(self.x, self.y, w, h), bg_color)
        arcade.draw_rect_outline(arcade.XYWH(self.x, self.y, w, h), border_color, 3)

        # Стоимость стамины
        cost_x = self.x - w / 2 + 26
        cost_y = self.y + h / 2 - 26
        cost_bg = BORDER_GOLD if can_afford else (60, 58, 62)
        arcade.draw_circle_filled(cost_x, cost_y, 19, cost_bg)

        self._txt_cost.x = cost_x
        self._txt_cost.y = cost_y
        self._txt_cost.draw()

        # Тип карты
        self._txt_type.x = self.x + 14
        self._txt_type.y = self.y + h / 2 - 26
        self._txt_type.draw()

        # Название
        self._txt_name.x = self.x
        self._txt_name.y = self.y + 76
        self._txt_name.draw()

        # Центральная иконка
        arcade.draw_circle_filled(self.x, self.y + 15, 32, (0, 0, 0, 85))
        draw_card_icon(self.card_type, self.x, self.y + 15, size=29)

        # Описание
        self._txt_desc.x = self.x
        self._txt_desc.y = self.y - 72
        self._txt_desc.draw()
