import arcade


class TextCache:
    """Кэширует объекты arcade.Text по координатам и параметрам — сигнатура полностью совпадает с arcade.draw_text."""

    def __init__(self):
        self._items: dict[tuple, arcade.Text] = {}

    def draw(
        self,
        text: str,
        x: float,
        y: float,
        color,
        font_size: int = 14,
        width: int | None = None,
        align: str = "left",
        bold: bool = False,
        anchor_x: str = "left",
        anchor_y: str = "baseline",
        multiline: bool = False,
    ):
        key = (round(x, 1), round(y, 1), font_size, bold, anchor_x, anchor_y, multiline)
        obj = self._items.get(key)
        if obj is None:
            obj = arcade.Text(
                text, x, y, color, font_size,
                width=width or 0, align=align, bold=bold,
                anchor_x=anchor_x, anchor_y=anchor_y, multiline=multiline
            )
            self._items[key] = obj
        else:
            if obj.text != text:
                obj.text = text
            if obj.color != color:
                obj.color = color
        obj.draw()
