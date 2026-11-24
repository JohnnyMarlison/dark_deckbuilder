import random
from core.hero import Hero, create_hero
from core.card import Card
from core.effects import DamageEffect, HealEffect

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
        healed = self.hero.heal(max(4, int(self.hero.max_hp * random.uniform(0.06, 0.10))))
        self.advance_step()
        return hp_gain, healed

    def apply_deck_buff(self, buff_type: str, amount: int):
        if buff_type in self.bonuses:
            self.bonuses[buff_type] += amount
        for card in self.hero.master_deck:
            updated = False
            for eff in card.effects:
                if buff_type == "damage" and isinstance(eff, DamageEffect):
                    eff.value += amount
                    updated = True
                elif buff_type == "heal" and isinstance(eff, HealEffect):
                    eff.value += amount
                    updated = True
            if updated:
                card.desc = ", ".join(e.describe(1.0) for e in card.effects if e.describe(1.0))
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
            self.hero.master_deck.append(c.copy())

    def start_new_game_plus(self):
        self.ng_level += 1
        self.stage = 1
        self.round_idx = 1
        self.hero.hp = self.hero.max_hp
        self.current_location_name = random.choice(WORLD_LOCATIONS.get(1, ("Мрачный лес",)))
