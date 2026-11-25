import json
import os
from core.effects import (
    Effect,
    CombatEvent,
    DamageEffect,
    BlockDamageEffect,
    BlockEffect,
    HealEffect,
    StripBlockEffect,
    build_effects,
)

class Card:
    """Модель игровой карты (без привязки к графике)."""

    def __init__(
            self,
            card_id: str,
            name: str,
            card_type: str,
            cost: int,
            desc: str,
            effects: list[Effect],
            exhaust: bool = False,
            neutral: bool = False,
            pool_count: int = 1,
            hero_class: str = "",
    ):
        self.card_id = card_id
        self.name = name
        self.card_type = card_type
        self.cost = cost
        self.desc = desc
        self.effects = effects
        self.exhaust = exhaust
        self.neutral = neutral
        self.pool_count = pool_count
        self.hero_class = hero_class

    def copy(self) -> "Card":
        return Card(
            self.card_id, self.name, self.card_type, self.cost, self.desc,
            list(self.effects), exhaust=self.exhaust, neutral=self.neutral, pool_count=self.pool_count, hero_class=self.hero_class
        )

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
                new_effects.append(DamageEffect(eff.value + 3, pierce=eff.pierce))
                desc_parts.append(f"Наносит {eff.value + 3} урона")
            elif isinstance(eff, BlockDamageEffect):
                new_effects.append(BlockDamageEffect(eff.value + 3, pierce=eff.pierce))
                desc_parts.append(f"Наносит {eff.value + 3} + ваша броня урона")
            elif isinstance(eff, BlockEffect):
                new_effects.append(BlockEffect(eff.value + 3))
                desc_parts.append(f"Даёт {eff.value + 3} защиты")
            elif isinstance(eff, HealEffect):
                new_effects.append(HealEffect(eff.value + 3))
                desc_parts.append(f"Восстанавливает {eff.value + 3} HP")
            elif isinstance(eff, StripBlockEffect):
                new_effects.append(StripBlockEffect())
                desc_parts.append("Сбрасывает всю броню врага")
            else:
                new_effects.append(eff)

        new_desc = ", ".join(desc_parts) if desc_parts else self.desc
        if self.exhaust and "Изгнание" not in new_desc:
            new_desc += ". Изгнание."
        return Card(f"{self.card_id}_plus", f"{self.name}+", self.card_type, self.cost, new_desc, new_effects,
                    exhaust=self.exhaust, neutral=self.neutral, pool_count=self.pool_count, hero_class=self.hero_class)


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
    """Загружает все карты из файлов в папке data/cards/ (neutral.json, warrior.json и др.)."""

    FILE_TO_CLASS = {
        "warrior.json": "ВОИН",
        "mage.json": "ЭЛЕМЕНТАЛИСТ",
        "paladin.json": "ПАЛАДИН",
        "assassin.json": "АССАСИН",
    }

    cards_dir = os.path.join("data", "cards")
    library: dict[str, Card] = {}

    if not os.path.exists(cards_dir):
        return library

    for filename in sorted(os.listdir(cards_dir)):
        if not filename.endswith(".json"):
            continue
        is_neutral_file = (filename == "neutral.json")
        default_class = FILE_TO_CLASS.get(filename, "")
        filepath = os.path.join(cards_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            raw = json.load(f)

        for cid, info in raw.items():
            effects = build_effects(info.get("effects", []))
            library[cid] = Card(
                cid,
                info["name"],
                info["type"],
                info["cost"],
                info["desc"],
                effects,
                exhaust=info.get("exhaust", False),
                neutral=info.get("neutral", is_neutral_file),
                pool_count=info.get("pool_count", 1),
                hero_class=info.get("hero_class", default_class),
            )

    return library




