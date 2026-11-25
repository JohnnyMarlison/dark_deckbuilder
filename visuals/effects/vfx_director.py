import random
import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BORDER_GOLD, TEXT_MUTED
from core.events import bus
from visuals.effects.particles import SpellProjectile, FloatingEffect


class VFXDirector:
    """Управляет условными анимациями, вспышками, тряской, снарядами и текстом боя через EventBus."""

    def __init__(self, view):
        self.v = view
        self.player_x = 610
        self.enemy_x = SCREEN_WIDTH - 610

        self.effects: list[FloatingEffect] = []
        self.projectiles: list[SpellProjectile] = []
        self.screen_shake: float = 0.0
        self.shake_intensity: float = 6.0

        # Полноэкранная цветная вспышка (r, g, b, alpha) для сильных ударов и комбо
        self.flash_color: tuple[int, int, int] = (220, 45, 45)
        self.flash_alpha: float = 0.0

        self._bind_events()

    def _bind_events(self):
        bus.subscribe("card_played", self._on_card_played)
        bus.subscribe("enemy_action_started", self._on_enemy_action)
        bus.subscribe("damage_dealt", self._on_damage)
        bus.subscribe("block_gained", self._on_block)
        bus.subscribe("strip_block", self._on_strip_block)
        bus.subscribe("heal_gained", self._on_heal)
        bus.subscribe("stamina_gained", self._on_stamina)
        bus.subscribe("stamina_stolen", self._on_stamina_stolen)

    def unbind(self):
        """Отписывает режиссёра при закрытии экрана боя, чтобы не копить дубликаты."""
        bus.unsubscribe("card_played", self._on_card_played)
        bus.unsubscribe("enemy_action_started", self._on_enemy_action)
        bus.unsubscribe("damage_dealt", self._on_damage)
        bus.unsubscribe("block_gained", self._on_block)
        bus.unsubscribe("strip_block", self._on_strip_block)
        bus.unsubscribe("heal_gained", self._on_heal)
        bus.unsubscribe("stamina_gained", self._on_stamina)
        bus.unsubscribe("stamina_stolen", self._on_stamina_stolen)

    def clear(self):
        self.effects.clear()
        self.projectiles.clear()
        self.screen_shake = 0.0
        self.flash_alpha = 0.0

    # --- Реакции на события шины ---

    def _on_card_played(self, card=None, **_):
        if self.v.player_avatar:
            self.v.player_avatar.trigger("casting", 0.45)
        if card and getattr(card, "has_damage", False):
            color = BORDER_GOLD if card.card_type == "Атака" else (155, 65, 185)
            self.projectiles.append(
                SpellProjectile(self.player_x + 25, 605, self.enemy_x - 15, 600, color, radius=16)
            )

    def _on_enemy_action(self, action=None, **_):
        if self.v.enemy_avatar:
            self.v.enemy_avatar.trigger("casting", 0.65)
        if action and getattr(action, "action_type", "") in ("Атака", "Заклинание"):
            color = (145, 50, 175) if action.action_type == "Заклинание" else (215, 65, 40)
            self.projectiles.append(
                SpellProjectile(self.enemy_x - 25, 610, self.player_x + 15, 605, color, radius=16)
            )

    def _on_damage(self, target: str = "enemy", value: int = 0, blocked: int = 0, **_):
        is_crit = value >= 15

        if target == "enemy":
            self.screen_shake = 0.30 if is_crit else 0.18
            self.shake_intensity = 10.0 if is_crit else 5.5
            if is_crit:
                self.trigger_flash((255, 185, 65), alpha=65.0)
            if self.v.enemy_avatar:
                self.v.enemy_avatar.trigger("hurt", 0.5)

            txt = f"-{value} HP" if blocked == 0 else f"-{value} (блок {blocked})"
            if is_crit:
                txt = f"КРИТ! {txt}"
            self.effects.append(FloatingEffect(self.enemy_x, 650, txt, (235, 85, 45)))

        elif value > 0:
            self.screen_shake = 0.35 if is_crit else 0.22
            self.shake_intensity = 11.0 if is_crit else 6.0
            self.trigger_flash((215, 35, 35), alpha=85.0 if is_crit else 45.0)
            if self.v.player_avatar:
                self.v.player_avatar.trigger("hurt", 0.55)
            self.effects.append(FloatingEffect(self.player_x, 650, f"-{value} HP", (215, 55, 55)))
        else:
            if self.v.player_avatar:
                self.v.player_avatar.trigger("heal", 0.45)
            self.effects.append(FloatingEffect(self.player_x, 650, f"Блок ({blocked})", (110, 165, 210)))

    def _on_block(self, target: str = "player", value: int = 0, **_):
        tx = self.player_x if target == "player" else self.enemy_x
        av = self.v.player_avatar if target == "player" else self.v.enemy_avatar
        if av:
            av.trigger("heal", 0.45)
        self.effects.append(FloatingEffect(tx, 675, f"+{value} Брони", (110, 165, 210)))

    def _on_strip_block(self, target: str = "enemy", value: int = 0, **_):
        tx = self.enemy_x if target == "enemy" else self.player_x
        if value > 0:
            self.screen_shake = 0.22
            self.shake_intensity = 6.5
            self.trigger_flash((110, 195, 245), alpha=55.0)
            self.effects.append(FloatingEffect(tx, 675, f"Броня снята (-{value})", (110, 195, 245)))
        else:
            self.effects.append(FloatingEffect(tx, 675, "Брони нет", TEXT_MUTED))

    def _on_heal(self, target: str = "player", value: int = 0, **_):
        if value <= 0:
            return
        tx = self.player_x if target == "player" else self.enemy_x
        av = self.v.player_avatar if target == "player" else self.v.enemy_avatar
        if av:
            av.trigger("heal", 0.45)
        self.effects.append(FloatingEffect(tx, 630, f"+{value} HP", (95, 195, 130)))

    def _on_stamina(self, value: int = 0, **_):
        self.effects.append(FloatingEffect(self.player_x, 695, f"+{value} Стамины", BORDER_GOLD))

    def _on_stamina_stolen(self, value: int = 0, **_):
        self.effects.append(FloatingEffect(self.player_x, 695, f"-{value} Стамина", BORDER_GOLD))

    # --- Управление кадрами и отрисовкой ---

    def trigger_flash(self, color: tuple[int, int, int], alpha: float = 70.0):
        self.flash_color = color
        self.flash_alpha = max(self.flash_alpha, alpha)

    def get_shake_offset(self) -> tuple[float, float]:
        if self.screen_shake <= 0:
            return 0.0, 0.0
        return (
            random.uniform(-self.shake_intensity, self.shake_intensity),
            random.uniform(-self.shake_intensity, self.shake_intensity),
        )

    def update(self, dt: float):
        if self.screen_shake > 0:
            self.screen_shake = max(0.0, self.screen_shake - dt)
        if self.flash_alpha > 0:
            self.flash_alpha = max(0.0, self.flash_alpha - dt * 210.0)

        self.projectiles = [p for p in self.projectiles if p.update(dt)]
        self.effects = [e for e in self.effects if e.update(dt)]

    def draw_projectiles(self):
        for proj in self.projectiles:
            proj.draw()

    def draw_foreground(self):
        for eff in self.effects:
            eff.draw()

        if self.flash_alpha > 1.0:
            r, g, b = self.flash_color
            arcade.draw_rect_filled(
                arcade.XYWH(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT),
                (r, g, b, int(self.flash_alpha)),
            )
