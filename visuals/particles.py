import math
import random
import arcade


class SpellProjectile:
    """Анимированный снаряд, летящий от атакующего к цели."""

    def __init__(self, start_x: float, start_y: float, end_x: float, end_y: float, color, radius: float = 14):
        self.x = start_x
        self.y = start_y
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.color = color
        self.radius = radius
        self.duration = 0.28
        self.elapsed = 0.0
        self.trail = []
        self._txt = arcade.Text(text, x, y, color, 21, bold=True, anchor_x="center", anchor_y="center")

    def update(self, dt: float) -> bool:
        self.elapsed += dt
        t = min(1.0, self.elapsed / self.duration)
        self.x = self.start_x + (self.end_x - self.start_x) * t
        self.y = self.start_y + (self.end_y - self.start_y) * t + math.sin(t * math.pi) * 45
        self.trail.append((self.x, self.y, self.radius))
        if len(self.trail) > 8:
            self.trail.pop(0)
        return t < 1.0

    def draw(self):
        self._txt.y = self.y
        self._txt.draw()
        for i, (tx, ty, r) in enumerate(self.trail):
            factor = (i + 1) / len(self.trail)
            arcade.draw_circle_filled(tx, ty, r * factor * 0.8, self.color)
        arcade.draw_circle_filled(self.x, self.y, self.radius, (235, 225, 210))


class FloatingEffect:
    """Всплывающий текст урона/лечения и система частиц."""

    def __init__(self, x: float, y: float, text: str, color):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.timer = 1.05
        self.particles = [
            {
                "x": x,
                "y": y,
                "vx": random.uniform(-140, 140),
                "vy": random.uniform(-50, 160),
                "size": random.uniform(4, 9),
            }
            for _ in range(20)
        ]

    def update(self, dt: float) -> bool:
        self.timer -= dt
        self.y += 45 * dt
        for p in self.particles:
            p["x"] += p["vx"] * dt
            p["y"] += p["vy"] * dt
            p["vy"] -= 200 * dt
        return self.timer > 0

    def draw(self):
        for p in self.particles:
            arcade.draw_circle_filled(p["x"], p["y"], p["size"] * max(0, self.timer), self.color)
        arcade.draw_text(
            self.text, self.x, self.y, self.color, 21, bold=True, anchor_x="center", anchor_y="center"
        )
