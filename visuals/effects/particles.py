import arcade


class SpellProjectile:
    def __init__(
        self,
        start_x: float,
        start_y: float,
        target_x: float,
        target_y: float,
        color: tuple,
        radius: float = 16,
    ):
        self.x = start_x
        self.y = start_y
        self.target_x = target_x
        self.target_y = target_y
        self.end_x = target_x
        self.color = color[:3]
        self.radius = radius
        self.speed = 1950.0
        self.exploded = False
        self.explode_timer = 0.0
        self.explode_duration = 0.28


    def update(self, dt: float) -> bool:
        if not self.exploded:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            dist = (dx * dx + dy * dy) ** 0.5
            step = self.speed * dt
            if dist <= step or dist < 5.0:
                self.x = self.target_x
                self.y = self.target_y
                self.exploded = True
                self.explode_timer = self.explode_duration
            else:
                self.x += (dx / dist) * step
                self.y += (dy / dist) * step
            return True

        self.explode_timer -= dt
        self.radius += 260.0 * dt
        return self.explode_timer > 0.0

    def draw(self):
        if not self.exploded:
            arcade.draw_circle_filled(self.x, self.y, self.radius * 1.45, (*self.color, 75))
            arcade.draw_circle_filled(self.x, self.y, self.radius, self.color)
            arcade.draw_circle_filled(self.x, self.y, self.radius * 0.45, (255, 255, 255, 200))
        else:
            ratio = max(0.0, self.explode_timer / self.explode_duration)
            alpha = int(135 * ratio)
            arcade.draw_circle_filled(self.x, self.y, self.radius, (*self.color, alpha))


class FloatingEffect:
    def __init__(self, x: float, y: float, text: str, color: tuple):
        self.x = x
        self.y = y
        self.timer = 1.15
        self.duration = 1.15
        self.label = arcade.Text(
            text,
            round(x),
            round(y),
            color[:3],
            20,
            bold=True,
            font_name="Arial",
            anchor_x="center",
            anchor_y="center",
        )

    def update(self, dt: float) -> bool:
        self.timer -= dt
        self.y += 48.0 * dt
        self.label.x = round(self.x)
        self.label.y = round(self.y)
        alpha = int(255 * max(0.0, min(1.0, self.timer / (self.duration * 0.45))))
        r, g, b = self.label.color[:3]
        self.label.color = (r, g, b, alpha)
        return self.timer > 0.0

    def draw(self):
        self.label.draw()
