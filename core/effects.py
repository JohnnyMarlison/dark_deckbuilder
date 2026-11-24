from dataclasses import dataclass


@dataclass
class CombatEvent:
    """Событие боя, которое слой графики превращает в анимацию и частицы."""
    kind: str        # "damage", "block", "heal", "stamina", "steal_stamina", "draw"
    target: str      # "player" или "enemy"
    value: int
    blocked: int = 0
    pierce: bool = False


class Effect:
    """Базовый класс любого игрового эффекта."""
    def apply(self, source, target, context: dict) -> list[CombatEvent]:
        return []

    def describe(self, scale: float = 1.0) -> str:
        return ""


class DamageEffect(Effect):
    def __init__(self, value: int, pierce: bool = False):
        self.value = value
        self.pierce = pierce

    def apply(self, source, target, context: dict) -> list[CombatEvent]:
        scale = context.get("scale", 1.0)
        dmg = source.calculate_outgoing_damage(int(self.value * scale))
        real_dmg, blocked = target.take_damage(dmg, pierce=self.pierce)
        target_role = "enemy" if context.get("source_is_player") else "player"
        return [CombatEvent("damage", target_role, real_dmg, blocked=blocked, pierce=self.pierce)]

    def describe(self, scale: float = 1.0) -> str:
        val = int(self.value * scale)
        return f"{val} урона сквозь броню" if self.pierce else f"Наносит {val} урона"


class BlockEffect(Effect):
    def __init__(self, value: int):
        self.value = value

    def apply(self, source, target, context: dict) -> list[CombatEvent]:
        scale = context.get("scale", 1.0)
        blk = int(self.value * scale)
        source.add_block(blk)
        src_role = "player" if context.get("source_is_player") else "enemy"
        return [CombatEvent("block", src_role, blk)]

    def describe(self, scale: float = 1.0) -> str:
        return f"Дает {int(self.value * scale)} брони"


class HealEffect(Effect):
    def __init__(self, value: int):
        self.value = value

    def apply(self, source, target, context: dict) -> list[CombatEvent]:
        scale = context.get("scale", 1.0)
        healed = source.heal(int(self.value * scale))
        src_role = "player" if context.get("source_is_player") else "enemy"
        return [CombatEvent("heal", src_role, healed)]

    def describe(self, scale: float = 1.0) -> str:
        return f"Лечит {int(self.value * scale)} HP"


class DrawEffect(Effect):
    def __init__(self, value: int):
        self.value = value

    def apply(self, source, target, context: dict) -> list[CombatEvent]:
        if hasattr(source, "draw_cards"):
            source.draw_cards(self.value)
        return [CombatEvent("draw", "player", self.value)]

    def describe(self, scale: float = 1.0) -> str:
        return f"+{self.value} карта"


class StaminaEffect(Effect):
    def __init__(self, value: int):
        self.value = value

    def apply(self, source, target, context: dict) -> list[CombatEvent]:
        if hasattr(source, "stamina"):
            source.stamina = min(10, source.stamina + self.value)
        return [CombatEvent("stamina", "player", self.value)]

    def describe(self, scale: float = 1.0) -> str:
        return f"+{self.value} Стамины"


class StealStaminaEffect(Effect):
    def __init__(self, value: int):
        self.value = value

    def apply(self, source, target, context: dict) -> list[CombatEvent]:
        if hasattr(target, "pending_stamina_loss"):
            target.pending_stamina_loss += self.value
        return [CombatEvent("steal_stamina", "player", self.value)]

    def describe(self, scale: float = 1.0) -> str:
        return f"-{self.value} стамины"


def build_effects(raw_list: list[dict]) -> list[Effect]:
    """Фабрика создания объектов эффектов из JSON-описания."""
    result: list[Effect] = []
    for item in raw_list:
        etype = item.get("type")
        val = item.get("value", 0)
        if etype == "damage":
            result.append(DamageEffect(val, pierce=item.get("pierce", False)))
        elif etype == "block":
            result.append(BlockEffect(val))
        elif etype == "heal":
            result.append(HealEffect(val))
        elif etype == "draw":
            result.append(DrawEffect(val))
        elif etype == "stamina":
            result.append(StaminaEffect(val))
        elif etype == "steal_stamina":
            result.append(StealStaminaEffect(val))
    return result
