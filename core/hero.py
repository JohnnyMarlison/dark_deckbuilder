import json
import os
import random
from core.entity import Entity
from core.card import Card, load_card_library

MAX_HAND_LIMIT = 8  # Максимальный лимит карт в руке с учетом добора пилюлями


class Hero(Entity):
    """Класс героя с раздельной механикой личной и нейтральной колод."""

    def __init__(self, name: str, max_hp: int, max_stamina: int, hero_deck: list[Card], neutral_deck: list[Card]):
        super().__init__(name, max_hp)
        self.max_stamina = max_stamina
        self.stamina = max_stamina

        # Базовый размер руки (5 карт) + модификаторы для будущих карт/реликвий
        self.base_hand_size: int = 5
        self.temp_hand_bonus: int = 0

        # Две независимые мастер-колоды на поход
        self.hero_master_deck: list[Card] = hero_deck
        self.neutral_master_deck: list[Card] = neutral_deck

        # Боевые стопки добора и сброса для каждого пула
        self.hero_draw_pile: list[Card] = []
        self.hero_discard_pile: list[Card] = []
        self.neutral_draw_pile: list[Card] = []
        self.neutral_discard_pile: list[Card] = []

        self.hand: list[Card] = []

    @property
    def master_deck(self) -> list[Card]:
        """Объединенный список всех карт похода (для глобальных баффов и наград)."""
        return self.hero_master_deck + self.neutral_master_deck

    @property
    def draw_pile(self) -> list[Card]:
        """Общий пул оставшихся карт в обеих колодах (для счетчика в UI)."""
        return self.hero_draw_pile + self.neutral_draw_pile

    @property
    def discard_pile(self) -> list[Card]:
        """Общий пул карт в сбросе (для счетчика в UI)."""
        return self.hero_discard_pile + self.neutral_discard_pile

    def prepare_for_battle(self):
        self.reset_block()
        self.temp_hand_bonus = 0
        self.hand.clear()

        self.hero_discard_pile.clear()
        self.hero_draw_pile = [c.copy() for c in self.hero_master_deck]
        random.shuffle(self.hero_draw_pile)

        self.neutral_discard_pile.clear()
        self.neutral_draw_pile = [c.copy() for c in self.neutral_master_deck]
        random.shuffle(self.neutral_draw_pile)

    def discard_card(self, card: Card):
        """Отправляет сыгранную или сброшенную карту в соответствующий сброс."""
        if card.neutral:
            self.neutral_discard_pile.append(card)
        else:
            self.hero_discard_pile.append(card)

    def _draw_from_neutral(self, count: int):
        for _ in range(count):
            if len(self.hand) >= MAX_HAND_LIMIT:
                break
            if not self.neutral_draw_pile:
                if not self.neutral_discard_pile:
                    break
                self.neutral_draw_pile = list(self.neutral_discard_pile)
                self.neutral_discard_pile.clear()
                random.shuffle(self.neutral_draw_pile)
            self.hand.append(self.neutral_draw_pile.pop())

    def _draw_from_hero(self, count: int):
        for _ in range(count):
            if len(self.hand) >= MAX_HAND_LIMIT:
                break
            if not self.hero_draw_pile:
                if not self.hero_discard_pile:
                    break
                self.hero_draw_pile = list(self.hero_discard_pile)
                self.hero_discard_pile.clear()
                random.shuffle(self.hero_draw_pile)
            self.hand.append(self.hero_draw_pile.pop())

    def draw_cards(self, count: int):
        """Добор карт эффектами (например, Пилюлями силы) с шансом 50/50 между пулами."""
        for _ in range(count):
            if len(self.hand) >= MAX_HAND_LIMIT:
                break
            if random.random() < 0.5:
                before = len(self.hand)
                self._draw_from_neutral(1)
                if len(self.hand) == before:
                    self._draw_from_hero(1)
            else:
                before = len(self.hand)
                self._draw_from_hero(1)
                if len(self.hand) == before:
                    self._draw_from_neutral(1)

    def start_turn(self):
        self.stamina = self.max_stamina

        # Целевой размер руки на этот ход (по умолчанию 5 + временные бонусы расширения руки)
        target_size = min(MAX_HAND_LIMIT, max(1, self.base_hand_size + self.temp_hand_bonus))
        self.temp_hand_bonus = 0

        # Если карт в руке уже >= целевого размера (например, после пилюль добора), ничего не добираем
        if len(self.hand) >= target_size:
            return

        # Считаем, сколько нейтральных и геройских карт уже осталось в руке с прошлого хода
        cur_neutral = sum(1 for c in self.hand if c.neutral)
        cur_hero = len(self.hand) - cur_neutral

        # 1) Добираем нейтральные карты, чтобы их было до 3 (в пределах свободного места)
        need_neutral = min(target_size - len(self.hand), max(0, 3 - cur_neutral))
        self._draw_from_neutral(need_neutral)

        # 2) Добираем карту героя, если в руке ещё нет ни одной классовой карты
        if len(self.hand) < target_size and cur_hero < 1:
            self._draw_from_hero(1)

        # 3) Все оставшиеся слоты до target_size заполняем с шансом 50/50 между пулами
        remaining_slots = max(0, target_size - len(self.hand))
        self.draw_cards(remaining_slots)

    def end_turn(self):
        # Несыгранные карты теперь НЕ сбрасываются, а остаются в руке до следующего хода!
        pass


def load_hero_templates() -> dict:
    path = os.path.join("data", "heroes.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def create_hero(hero_name: str) -> Hero:
    templates = load_hero_templates()
    library = load_card_library()
    info = templates[hero_name]

    # Личная колода выбранного героя
    hero_deck = [library[cid].copy() for cid in info["deck"] if cid in library]

    # Полная нейтральная колода из всех карт с флагом neutral=True и учетом их pool_count
    neutral_deck: list[Card] = []
    for card in library.values():
        if card.neutral:
            for _ in range(card.pool_count):
                neutral_deck.append(card.copy())

    return Hero(hero_name, info["hp"], info["stamina"], hero_deck, neutral_deck)
