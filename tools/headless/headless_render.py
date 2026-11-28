"""Рендер записанных draw-операций headless-стаба arcade в PNG (Pillow).

Система координат arcade: начало слева снизу, Y вверх.
Система координат Pillow: начало слева сверху, Y вниз. Перевод: py = H - y.
"""

from __future__ import annotations

import functools

from PIL import Image, ImageDraw, ImageFont

FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


@functools.lru_cache(maxsize=256)
def _font(size: int, bold: bool):
    path = FONT_BOLD if bold else FONT_REGULAR
    try:
        return ImageFont.truetype(path, max(6, int(size)))
    except OSError:
        return ImageFont.load_default()


def _rgba(c) -> tuple:
    if c is None:
        return (0, 0, 0, 255)
    if len(c) == 3:
        return (int(c[0]), int(c[1]), int(c[2]), 255)
    return (int(c[0]), int(c[1]), int(c[2]), int(c[3]))


def measure_text(text: str, size: int, bold: bool) -> float:
    """Приблизительная ширина текста в пикселях (для content_width)."""
    f = _font(size, bold)
    w = 0.0
    for line in str(text).split("\n"):
        w = max(w, f.getlength(line))
    return w


def _wrap(line: str, f, max_w: int) -> list[str]:
    """Перенос по словам, если строка не влезает в width."""
    if max_w <= 0 or f.getlength(line) <= max_w:
        return [line]
    words = line.split(" ")
    out, cur = [], ""
    for word in words:
        cand = (cur + " " + word).strip()
        if cur and f.getlength(cand) > max_w:
            out.append(cur)
            cur = word
        else:
            cur = cand
    if cur:
        out.append(cur)
    return out or [""]


def _draw_text_op(draw, text, x, y, color, size, bold, anchor_x, anchor_y,
                  width, align, multiline, H):
    f = _font(size, bold)
    lines = str(text).split("\n")
    if multiline and width > 0:
        lines = [ln for raw in lines for ln in _wrap(raw, f, width)]

    line_h = size * 1.25
    n = len(lines)
    base_ax = {"left": "l", "center": "m", "right": "r"}.get(anchor_x, "l")

    # Вертикальное позиционирование первой строки (в координатах изображения)
    if anchor_y == "center":
        baseline0 = (H - y) + (n - 1) * line_h / 2 + size * 0.35
    elif anchor_y == "top":
        baseline0 = (H - y) + size * 0.8
    else:  # baseline
        baseline0 = H - y

    # Горизонтальный бокс (учитывая width и anchor_x)
    if width > 0:
        if anchor_x == "center":
            box_left = x - width / 2
        elif anchor_x == "right":
            box_left = x - width
        else:
            box_left = x
    else:
        box_left = None

    fill = _rgba(color)
    for i, line in enumerate(lines):
        lw = f.getlength(line)
        by = baseline0 + i * line_h
        if box_left is not None:
            if align == "center":
                lx = box_left + (width - lw) / 2
            elif align == "right":
                lx = box_left + width - lw
            else:
                lx = box_left
            draw.text((lx, by), line, font=f, fill=fill, anchor="ls")
        else:
            draw.text((x, by), line, font=f, fill=fill, anchor=base_ax + "s")


def render(ops, width: int, height: int, bg_color, out_path: str) -> None:
    img = Image.new("RGBA", (width, height), _rgba(bg_color))
    draw = ImageDraw.Draw(img, "RGBA")

    for op in ops:
        kind = op[0]

        if kind == "clear":
            draw.rectangle([0, 0, width, height], fill=_rgba(op[1]))

        elif kind == "line":
            _, x1, y1, x2, y2, col, lw = op
            draw.line([(x1, height - y1), (x2, height - y2)],
                      fill=_rgba(col), width=max(1, int(round(lw))))

        elif kind == "line_strip":
            _, pts, col, lw = op
            if len(pts) >= 2:
                im_pts = [(px, height - py) for px, py in pts]
                draw.line(im_pts, fill=_rgba(col), width=max(1, int(round(lw))), joint="curve")

        elif kind == "rect_filled":
            _, rect, col = op
            box = [rect.left, height - rect.top, rect.right, height - rect.bottom]
            draw.rectangle(box, fill=_rgba(col))

        elif kind == "rect_outline":
            _, rect, col, lw = op
            box = [rect.left, height - rect.top, rect.right, height - rect.bottom]
            w = max(1, int(round(lw)))
            # рисуем концентрические прямоугольники, чтобы обойти толщину PIL
            for k in range(w):
                kbox = [box[0] + k, box[1] + k, box[2] - k, box[3] - k]
                if kbox[0] <= kbox[2] and kbox[1] <= kbox[3]:
                    draw.rectangle(kbox, outline=_rgba(col))

        elif kind == "circle_filled":
            _, cx, cy, r, col = op
            box = [cx - r, height - (cy + r), cx + r, height - (cy - r)]
            draw.ellipse(box, fill=_rgba(col))

        elif kind == "circle_outline":
            _, cx, cy, r, col, lw = op
            box = [cx - r, height - (cy + r), cx + r, height - (cy - r)]
            draw.ellipse(box, outline=_rgba(col), width=max(1, int(round(lw))))

        elif kind == "ellipse_filled":
            _, cx, cy, ew, eh, col, _tilt = op
            box = [cx - ew / 2, height - (cy + eh / 2), cx + ew / 2, height - (cy - eh / 2)]
            draw.ellipse(box, fill=_rgba(col))

        elif kind == "ellipse_outline":
            _, cx, cy, ew, eh, col, lw, _tilt = op
            box = [cx - ew / 2, height - (cy + eh / 2), cx + ew / 2, height - (cy - eh / 2)]
            draw.ellipse(box, outline=_rgba(col), width=max(1, int(round(lw))))

        elif kind == "arc_outline":
            _, cx, cy, ew, eh, col, a0, a1, lw = op
            box = [cx - ew / 2, height - (cy + eh / 2), cx + ew / 2, height - (cy - eh / 2)]
            # arcade: CCW от 0° (вправо); Pillow: CW в экранных координатах
            draw.arc(box, start=-a1, end=-a0, fill=_rgba(col), width=max(1, int(round(lw))))

        elif kind == "arc_filled":
            _, cx, cy, ew, eh, col, a0, a1 = op
            box = [cx - ew / 2, height - (cy + eh / 2), cx + ew / 2, height - (cy - eh / 2)]
            draw.pieslice(box, start=-a1, end=-a0, fill=_rgba(col))

        elif kind == "polygon_filled":
            _, pts, col = op
            if len(pts) >= 3:
                draw.polygon([(px, height - py) for px, py in pts], fill=_rgba(col))

        elif kind == "polygon_outline":
            _, pts, col, lw = op
            if len(pts) >= 2:
                im_pts = [(px, height - py) for px, py in pts] + [(pts[0][0], height - pts[0][1])]
                draw.line(im_pts, fill=_rgba(col), width=max(1, int(round(lw))))

        elif kind == "triangle_filled":
            _, x1, y1, x2, y2, x3, y3, col = op
            draw.polygon([(x1, height - y1), (x2, height - y2), (x3, height - y3)], fill=_rgba(col))

        elif kind == "text":
            _, text, x, y, col, size, bold, ax, ay, wdt, align, ml = op
            _draw_text_op(draw, text, x, y, col, size, bold, ax, ay, wdt, align, ml, height)

    img.convert("RGB").save(out_path, "PNG")
