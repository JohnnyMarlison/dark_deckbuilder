class Modifier:
    """Базовый плагин для статус-эффектов (Яд, Слабость) и реликвий."""

    def modify_outgoing_damage(self, amount: int) -> int:
        return amount

    def modify_incoming_damage(self, amount: int) -> int:
        return amount

    def on_turn_start(self, owner: "Entity") -> list:
        return []

    def on_turn_end(self, owner: "Entity") -> list:
        return []


class Entity:
    """Базовый класс для Героя и Врага с поддержкой статусов и хуков."""

    def __init__(self, name: str, max_hp: int):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.block = 0
        self.statuses: dict[str, int] = {}
        self.modifiers: list[Modifier] = []

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def add_block(self, amount: int):
        if amount > 0:
            self.block += amount

    def heal(self, amount: int) -> int:
        if amount <= 0:
            return 0
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - old_hp

    def calculate_outgoing_damage(self, base_amount: int) -> int:
        dmg = base_amount
        for mod in self.modifiers:
            dmg = mod.modify_outgoing_damage(dmg)
        return max(0, dmg)

    def take_damage(self, amount: int, pierce: bool = False) -> tuple[int, int]:
        if amount <= 0:
            return 0, 0
        for mod in self.modifiers:
            amount = mod.modify_incoming_damage(amount)
        amount = max(0, amount)

        if pierce:
            blocked = 0
            real_dmg = amount
        else:
            blocked = min(self.block, amount)
            self.block -= blocked
            real_dmg = amount - blocked

        self.hp = max(0, self.hp - real_dmg)
        return real_dmg, blocked

    def apply_status(self, status_name: str, stacks: int):
        if stacks != 0:
            self.statuses[status_name] = self.statuses.get(status_name, 0) + stacks
            if self.statuses[status_name] <= 0:
                del self.statuses[status_name]

    def trigger_turn_start(self) -> list:
        events = []
        for mod in list(self.modifiers):
            events.extend(mod.on_turn_start(self))
        return events

    def trigger_turn_end(self) -> list:
        events = []
        for mod in list(self.modifiers):
            events.extend(mod.on_turn_end(self))
        return events

    def reset_block(self):
        self.block = 0
