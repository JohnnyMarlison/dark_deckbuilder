import json
import os
from core.effects import Effect, CombatEvent, build_effects, DamageEffect


class Card:
    """Модель игровой карты (без привязки к графике)."""

    def __init__(self, card_id: str, name: str, card_type: str, cost: int, desc: str, effects: list[Effect],
                 exhaust: bool = False):
        self.card_id = card_id
        self.name = name
        self.card_type = card_type
        self.cost = cost
        self.desc = desc
        self.effects = effects
        self.exhaust = exhaust

    def copy(self) -> "Card":
        return Card(self.card_id, self.name, self.card_type, self.cost, self.desc, list(self.effects),
                    exhaust=self.exhaust)

    @property
    def has_damage(self) -> bool:
        return any(isinstance(e, DamageEffect) for e in self.effects)

    def play(self, player, enemy) -> list[CombatEvent]:
        events: list[CombatEvent] = []
        ctx = {"source_is_player": True, "scale": 1.0}
        for eff in self.effects:
            events.extend(eff.apply(player, enemy, ctx))
        return events

    def create_upgraded_copy(self) -> "Card":
        """Создает усиленную версию карты для награды после босса."""
        from core.effects import DamageEffect, BlockEffect, HealEffect, DrawEffect, StaminaEffect

        new_effects = []
        desc_parts = []
        for eff in self.effects:
            if isinstance(eff, DamageEffect):
                bonus = max(3, int(eff.value * 0.45))
                new_val = eff.value + bonus
                new_effects.append(DamageEffect(new_val, pierce=eff.pierce))
                desc_parts.append(f"Наносит {new_val} урона")
            elif isinstance(eff, BlockEffect):
                bonus = max(3, int(eff.value * 0.45))
                new_val = eff.value + bonus
                new_effects.append(BlockEffect(new_val))
                desc_parts.append(f"Дает {new_val} брони")
            elif isinstance(eff, HealEffect):
                bonus = max(3, int(eff.value * 0.45))
                new_val = eff.value + bonus
                new_effects.append(HealEffect(new_val))
                desc_parts.append(f"Лечит {new_val} HP")
            elif isinstance(eff, DrawEffect):
                new_effects.append(DrawEffect(eff.value))
                desc_parts.append(f"+{eff.value} карта")
            elif isinstance(eff, StaminaEffect):
                new_effects.append(StaminaEffect(eff.value))
                desc_parts.append(f"+{eff.value} Стамины")

        new_desc = ", ".join(desc_parts) if desc_parts else self.desc
        if self.exhaust and "Изгнание" not in new_desc:
            new_desc += ". Изгнание."
        return Card(f"{self.card_id}_plus", f"{self.name}+", self.card_type, self.cost, new_desc, new_effects,
                    exhaust=self.exhaust)


class EnemyAction:
    """Карточка действия противника."""

    def __init__(self, action_type: str, name: str, effects: list[Effect], scale: float = 1.0):
        self.action_type = action_type
        self.name = name
        self.effects = effects
        self.scale = scale

    @property
    def desc(self) -> str:
        return ", ".join(e.describe(self.scale) for e in self.effects if e.describe(self.scale))

    @property
    def has_damage(self) -> bool:
        return any(isinstance(e, DamageEffect) for e in self.effects)

    def execute(self, enemy, player) -> list[CombatEvent]:
        events: list[CombatEvent] = []
        ctx = {"source_is_player": False, "scale": self.scale}
        for eff in self.effects:
            events.extend(eff.apply(enemy, player, ctx))
        return events


def load_card_library() -> dict[str, Card]:
    path = os.path.join("data", "cards.json")
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    library: dict[str, Card] = {}
    for cid, info in raw.items():
        effects = build_effects(info.get("effects", []))
        library[cid] = Card(
            cid, info["name"], info["type"], info["cost"], info["desc"],
            effects, exhaust=info.get("exhaust", False)
        )
    return library


