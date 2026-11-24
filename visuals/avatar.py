import math
import random
import arcade
from config import BORDER_GOLD, TEXT_PARCHMENT
from visuals.hero_sprites import draw_hero_sprite
from visuals.enemy_sprites import draw_enemy_sprite


class CharacterAvatar:
    """Фигурка персонажа на каменном пьедестале со столбом света и анимациями."""

    def __init__(self, role: str, x: float, y: float, scale: float = 1.0, flip: bool = False):
        self.role = role
        self.base_x = x
        self.base_y = y
        self.x = x
        self.y = y
        self.scale = scale
        self.flip = -1 if flip else 1

        self.state = "idle"
        self.state_timer = 0.0
        self.state_duration = 0.5
        self.time = random.uniform(0, 6.28)
        self.weapon_angle = 0.0
        self.breath_offset = 0.0
        self.cast_progress = 0.0

    def trigger(self, state: str, duration: float = 0.5):
        self.state = state
        self.state_timer = duration
        self.state_duration = max(0.01, duration)

    def update(self, dt: float):
        self.time += dt
        if self.state_timer > 0:
            self.state_timer -= dt
            if self.state_timer <= 0:
                self.state = "idle"
                self.cast_progress = 0.0

        self.breath_offset = math.sin(self.time * 3.0) * 2.5 * self.scale
        offset_x = 0.0
        offset_y = self.breath_offset
        self.weapon_angle = math.sin(self.time * 2.5) * 4.0
        self.cast_progress = 0.0

        if self.state == "thinking":
            offset_x = math.sin(self.time * 5.0) * 2.5 * self.scale
            offset_y += abs(math.sin(self.time * 4.0)) * 3.0 * self.scale
            self.weapon_angle = 10.0 + math.sin(self.time * 7.0) * 4.0
        elif self.state == "casting":
            self.cast_progress = math.sin((1.0 - self.state_timer / self.state_duration) * math.pi)
            offset_x = self.cast_progress * 50.0 * self.flip * self.scale
            offset_y += self.cast_progress * 15.0 * self.scale
            self.weapon_angle = -35.0 * self.cast_progress
        elif self.state == "hurt":
            offset_x = math.sin(self.time * 55.0) * 11.0 * self.scale - 7.0 * self.flip * self.scale
            self.weapon_angle = 20.0
        elif self.state == "heal":
            offset_y += 11.0 * self.scale
        elif self.state == "victory":
            offset_y += abs(math.sin(self.time * 6.0)) * 16.0 * self.scale
            self.weapon_angle = -25.0

        self.x = self.base_x + offset_x
        self.y = self.base_y + offset_y

    def draw(self):
        s = self.scale
        d = self.flip
        cx, cy = self.x, self.y
        b = self.breath_offset

        px, py = self.base_x, self.base_y - 48 * s

        # Луч прожектора сверху
        beam_color = (145, 55, 55, 24) if self.flip == -1 else (168, 134, 62, 24)
        beam = (
            (px - 28 * s, py + 150 * s),
            (px + 28 * s, py + 150 * s),
            (px + 48 * s, py),
            (px - 48 * s, py),
        )
        arcade.draw_polygon_filled(beam, beam_color)

        # Каменный пьедестал
        arcade.draw_ellipse_filled(px, py - 5 * s, 96 * s, 26 * s, (26, 24, 32))
        arcade.draw_ellipse_filled(px, py, 92 * s, 24 * s, (46, 43, 54))
        arcade.draw_ellipse_outline(px, py, 92 * s, 24 * s, BORDER_GOLD, 2)
        arcade.draw_ellipse_filled(px, py + 1 * s, 64 * s, 15 * s, (14, 13, 18, 170))

        # Боевые реакции
        if self.state == "hurt":
            arcade.draw_circle_filled(cx, cy, 58 * s, (190, 25, 25, 105))
        elif self.state == "heal":
            arcade.draw_circle_filled(cx, cy, 58 * s, (45, 165, 95, 105))
        elif self.state == "victory":
            arcade.draw_circle_filled(cx, cy, 65 * s, (185, 145, 55, 90))

        if self.role in ("Воин", "Элементалист", "Паладин", "Ассасин"):
            draw_hero_sprite(self.role, cx, cy, s, d, b, self.time, self.weapon_angle)
        else:
            draw_enemy_sprite(self.role, cx, cy, s, d, b, self.time, self.state, self.cast_progress)

        if self.state == "thinking":
            bx = cx + 28 * d * s
            by = cy + 54 * s
            arcade.draw_ellipse_filled(bx, by, 38 * s, 21 * s, (45, 42, 52, 220))
            arcade.draw_ellipse_outline(bx, by, 38 * s, 21 * s, BORDER_GOLD, 1.5)
            dots = int(self.time * 3.5) % 3 + 1
            arcade.draw_text("." * dots, bx, by - 5 * s, TEXT_PARCHMENT, int(16 * s), bold=True, anchor_x="center")
