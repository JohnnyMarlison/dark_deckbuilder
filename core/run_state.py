import random
from core.hero import Hero, create_hero
from core.card import Card
from core.effects import DamageEffect, HealEffect, BlockEffect, BlockDamageEffect

WORLD_LOCATIONS = {
    1: ("Мрачный лес", "Заброшенная деревня", "Лагерь разбойников"),
    2: ("Песчаный склеп", "Разрушенный двор замка", "Разрушенный колизей"),
    3: ("Обсидиановая цитадель", "Подземелье мертвецов", "Ледяная корона"),
}


class RunState:
    """Управляет структурой кампании: 3 Мира по 3 Раунда в каждом + случайные локации."""

    def __init__(self, hero_name: str):
        self.hero: Hero = create_hero(hero_name)
        self.base_hero_hp: int = self.hero.max_hp  # Фиксируем стартовое HP для честного расчета наград
        self.stage: int = 1
        self.round_idx: int = 1
        self.ng_level: int = 0
        self.total_turns: int = 1
        self.bonuses: dict[str, int] = {"max_hp": 0, "damage": 0, "heal": 0}
        self.current_location_name: str = random.choice(WORLD_LOCATIONS.get(1, ("Мрачный лес",)))
        self.bonuses: dict[str, int] = {
            "max_hp": 0,
            "neutral_damage": 0,
            "neutral_heal": 0,
            "neutral_block": 0,
            "hero_damage": 0,
            "hero_heal": 0,
            "hero_block": 0,
        }


    @property
    def location(self) -> int:
        return self.stage

    @property
    def round_num(self) -> int:
        return self.round_idx

    @property
    def location_title(self) -> str:
        return f"МИР {self.stage}: {self.current_location_name.upper()}"

    def advance_step(self):
        if self.round_idx < 3:
            self.round_idx += 1
        else:
            self.stage += 1
            self.round_idx = 1
            pool = WORLD_LOCATIONS.get(self.stage, ("Бездна Тьмы",))
            self.current_location_name = random.choice(pool)


    def apply_full_heal(self) -> int:
        healed = self.hero.heal(self.hero.max_hp)
        self.advance_step()
        return healed

    def apply_max_hp_boost(self) -> tuple[int, int]:
        hp_gain = max(6, int(self.base_hero_hp * random.uniform(0.10, 0.12)))
        self.hero.max_hp += hp_gain
        self.bonuses["max_hp"] += hp_gain
        healed = self.hero.heal(max(5, int(self.hero.max_hp * random.uniform(0.10, 0.15))))
        self.advance_step()
        return hp_gain, healed

    def apply_deck_buff(self, scope: str, stat: str, amount: int):
        """
        scope: 'neutral' или 'hero'
        stat: 'damage' (+3), 'heal' (+3) или 'block' (+2)
        """
        bonus_key = f"{scope}_{stat}"
        if bonus_key in self.bonuses:
            self.bonuses[bonus_key] += amount

        target_deck = self.hero.neutral_master_deck if scope == "neutral" else self.hero.hero_master_deck

        for card in target_deck:
            updated = False
            for eff in card.effects:
                if stat == "damage" and isinstance(eff, (DamageEffect, BlockDamageEffect)):
                    eff.value += amount
                    updated = True
                elif stat == "heal" and isinstance(eff, HealEffect):
                    eff.value += amount
                    updated = True
                elif stat == "block" and isinstance(eff, BlockEffect):
                    eff.value += amount
                    updated = True

            if updated:
                # Пересобираем описание карты с учётом изгнания и пробивания
                parts = []
                for e in card.effects:
                    d = e.describe(1.0)
                    if d:
                        if isinstance(e, DamageEffect) and e.pierce:
                            d += " сквозь броню"
                        parts.append(d)
                new_desc = ", ".join(parts) + "."
                if getattr(card, "exhaust", False):
                    new_desc += " Изгнание."
                card.desc = new_desc

        self.advance_step()

    def generate_boss_card_choices(self, count: int = 4) -> list[Card]:
        unique_cards: dict[str, Card] = {}
        for c in self.hero.master_deck:
            base_id = c.card_id.replace("_plus", "")
            if base_id not in unique_cards:
                unique_cards[base_id] = c
        pool = list(unique_cards.values())
        chosen = random.sample(pool, min(count, len(pool)))
        return [c.create_upgraded_copy() for c in chosen]

    def add_cards_to_deck(self, cards: list[Card]):
        for c in cards:
            if c.neutral:
                self.hero.neutral_master_deck.append(c.copy())
            else:
                self.hero.hero_master_deck.append(c.copy())

    def start_new_game_plus(self):
        self.ng_level += 1
        self.stage = 1
        self.round_idx = 1
        self.hero.hp = self.hero.max_hp
        self.current_location_name = random.choice(WORLD_LOCATIONS.get(1, ("Мрачный лес",)))
