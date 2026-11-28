"""Headless-заглушка arcade для песочницы без OpenGL/X11.

Имитирует ровно ту часть API arcade, которую использует проект, и записывает
все draw-вызовы в список операций. См. headless_render.py — рендер операций в PNG.

ВАЖНО: этот пакет подменяет настоящий arcade ТОЛЬКО когда каталог
tools/headless добавлен в sys.path ПЕРЕД site-packages (см. run_demo.py).
Обычный запуск игры (python main.py) использует настоящий arcade.
"""

MOUSE_BUTTON_LEFT = 1

# ---------------------------------------------------------------- события/константы


class _Key:
    SPACE = 32
    ENTER = 65293
    ESCAPE = 65307
    LEFT = 65361
    RIGHT = 65363
    UP = 65362
    DOWN = 65364


key = _Key()


class _Color:
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)


color = _Color()

# ---------------------------------------------------------------- запись кадра

_frame_ops: list[tuple] = []
_bg_color: tuple = (0, 0, 0)


def begin_frame() -> None:
    """Очищает список операций текущего кадра (вызывать перед on_draw)."""
    _frame_ops.clear()


def get_frame_ops() -> list[tuple]:
    return _frame_ops


def get_background_color() -> tuple:
    return _bg_color


def _record(op: tuple) -> None:
    _frame_ops.append(op)


def set_background_color(c) -> None:
    global _bg_color
    _bg_color = tuple(c)


# ---------------------------------------------------------------- геометрия


class XYWH:
    """Прямоугольник по центру и размерам (аналог arcade.XYWH)."""

    __slots__ = ("x", "y", "width", "height")

    def __init__(self, x, y, width, height):
        self.x = float(x)
        self.y = float(y)
        self.width = float(width)
        self.height = float(height)

    @property
    def left(self):
        return self.x - self.width / 2

    @property
    def right(self):
        return self.x + self.width / 2

    @property
    def bottom(self):
        return self.y - self.height / 2

    @property
    def top(self):
        return self.y + self.height / 2

    def __repr__(self):
        return f"XYWH({self.x}, {self.y}, {self.width}, {self.height})"


# ---------------------------------------------------------------- примитивы


def draw_line(x1, y1, x2, y2, color_, line_width=1):
    _record(("line", float(x1), float(y1), float(x2), float(y2), tuple(color_), float(line_width)))


def draw_line_strip(point_list, color_, line_width=1):
    _record(("line_strip", [(float(x), float(y)) for x, y in point_list], tuple(color_), float(line_width)))


def draw_rect_filled(rect, color_):
    _record(("rect_filled", rect, tuple(color_)))


def draw_rect_outline(rect, color_, line_width=1):
    _record(("rect_outline", rect, tuple(color_), float(line_width)))


def draw_circle_filled(x, y, radius, color_):
    _record(("circle_filled", float(x), float(y), float(radius), tuple(color_)))


def draw_circle_outline(x, y, radius, color_, line_width=1):
    _record(("circle_outline", float(x), float(y), float(radius), tuple(color_), float(line_width)))


def draw_ellipse_filled(center_x, center_y, width, height, color_, tilt_angle=0):
    _record(("ellipse_filled", float(center_x), float(center_y), float(width), float(height), tuple(color_), float(tilt_angle)))


def draw_ellipse_outline(center_x, center_y, width, height, color_, line_width=1, tilt_angle=0):
    _record(("ellipse_outline", float(center_x), float(center_y), float(width), float(height),
             tuple(color_), float(line_width), float(tilt_angle)))


def draw_arc_outline(center_x, center_y, width, height, color_, start_angle, end_angle, line_width=1, tilt_angle=0):
    _record(("arc_outline", float(center_x), float(center_y), float(width), float(height),
             tuple(color_), float(start_angle), float(end_angle), float(line_width)))


def draw_arc_filled(center_x, center_y, width, height, color_, start_angle, end_angle, tilt_angle=0):
    _record(("arc_filled", float(center_x), float(center_y), float(width), float(height),
             tuple(color_), float(start_angle), float(end_angle)))


def draw_polygon_filled(point_list, color_):
    _record(("polygon_filled", [(float(x), float(y)) for x, y in point_list], tuple(color_)))


def draw_polygon_outline(point_list, color_, line_width=1):
    _record(("polygon_outline", [(float(x), float(y)) for x, y in point_list], tuple(color_), float(line_width)))


def draw_triangle_filled(x1, y1, x2, y2, x3, y3, color_):
    _record(("triangle_filled", float(x1), float(y1), float(x2), float(y2), float(x3), float(y3), tuple(color_)))


def draw_text(text, x, y, color_, font_size=12, width=0, align="left", bold=False,
              italic=False, font_name="Arial", anchor_x="left", anchor_y="baseline",
              multiline=False, rotation=0, **_kwargs):
    _record(("text", str(text), float(x), float(y), tuple(color_), int(font_size),
             bool(bold), anchor_x, anchor_y, int(width or 0), align, bool(multiline)))


# ---------------------------------------------------------------- текст


class Text:
    """Кэшируемый текстовый объект (аналог arcade.Text)."""

    def __init__(self, text="", x=0, y=0, color=(255, 255, 255), font_size=12,
                 width=0, align="left", bold=False, italic=False, font_name="Arial",
                 anchor_x="left", anchor_y="baseline", multiline=False, rotation=0, **_kw):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.font_size = font_size
        self.width = width or 0
        self.align = align
        self.bold = bold
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y
        self.multiline = multiline

    @property
    def content_width(self) -> float:
        from headless_render import measure_text
        return measure_text(self.text, self.font_size, self.bold)

    def draw(self):
        _record(("text", str(self.text), float(self.x), float(self.y), tuple(self.color),
                 int(self.font_size), bool(self.bold), self.anchor_x, self.anchor_y,
                 int(self.width), self.align, bool(self.multiline)))


# ---------------------------------------------------------------- окно/взгляд


class View:
    """Базовый взгляд: держит ссылку на окно и умеет clear()."""

    window = None

    def clear(self, color=None):
        c = tuple(color) if color is not None else tuple(_bg_color)
        _record(("clear", c))


class _Ctx:
    """Заглушка контекста (нужна battle_modals для scissor-обрезки)."""

    def __init__(self):
        self.scissor = None


class Window:
    def __init__(self, width=1920, height=1080, title="arcade window", **_kw):
        self.width = width
        self.height = height
        self.title = title
        self.ctx = _Ctx()
        self._view = None
        self._closed = False

    def show_view(self, view):
        self._view = view
        view.window = self
        cb = getattr(view, "on_show_view", None)
        if callable(cb):
            cb()

    def on_update(self, delta_time: float = 1 / 60):
        if self._view is not None:
            self._view.on_update(delta_time)

    def on_draw(self):
        if self._view is not None:
            self._view.on_draw()

    def switch_to(self):
        pass

    def close(self):
        self._closed = True

    def set_vsync(self, _v):
        pass


# ---------------------------------------------------------------- звук


class Sound:
    def __init__(self, path=None, **_kw):
        self.path = path

    def play(self, volume=1.0):
        pass

    def stop(self):
        pass


def load_sound(path, **_kw):
    return Sound(path)


def play_sound(sound, volume=1.0):
    pass


# ---------------------------------------------------------------- цикл


def run():
    """В headless-режиме цикл кадров крутит драйвер (run_demo.py)."""
    raise RuntimeError("arcade.run() недоступен в headless-стабе; кадры крутит run_demo.py")


def close_window():
    pass
