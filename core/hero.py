import json
import os
import random
from core.entity import Entity
from core.card import Card, load_card_library

MAX_HAND_SIZE = 6
CARDS_PER_TURN = 4


class Hero(Entity):
    """Класс игрока с управлением колодой, рукой, сбросом и стаминой."""

    def __init__(self, name: str, max_hp: int, max_stamina: int, desc: str, deck: list[Card]):
        super().__init__(name, max_hp)
        self.max_stamina = max_stamina
        self.stamina = max_stamina
        self.desc = desc

        self.master_deck: list[Card] = [c.copy() for c in deck]
        self.draw_pile: list[Card] = []
        self.hand: list[Card] = []
        self.discard_pile: list[Card] = []
        self.pending_stamina_loss = 0

    def prepare_for_battle(self):
        self.reset_block()
        self.statuses.clear()
        self.pending_stamina_loss = 0
        self.draw_pile = [c.copy() for c in self.master_deck]
        random.shuffle(self.draw_pile)
        self.hand.clear()
        self.discard_pile.clear()

    def start_turn(self) -> list[Card]:
        self.reset_block()
        self.stamina = max(1, self.max_stamina - self.pending_stamina_loss)
        self.pending_stamina_loss = 0
        return self.draw_cards(CARDS_PER_TURN)

    def end_turn(self):
        self.discard_pile.extend(self.hand)
        self.hand.clear()

    def draw_cards(self, count: int) -> list[Card]:
        drawn: list[Card] = []
        for _ in range(count):
            if len(self.hand) >= MAX_HAND_SIZE:
                break
            if not self.draw_pile:
                if not self.discard_pile:
                    break
                self.draw_pile = self.discard_pile[:]
                self.discard_pile.clear()
                random.shuffle(self.draw_pile)
            card = self.draw_pile.pop()
            self.hand.append(card)
            drawn.append(card)
        return drawn


def load_hero_templates() -> dict:
    path = os.path.join("data", "heroes.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def create_hero(hero_name: str) -> Hero:
    templates = load_hero_templates()
    library = load_card_library()
    info = templates[hero_name]
    deck = [library[cid].copy() for cid in info["deck"] if cid in library]
    return Hero(hero_name, info["hp"], info["stamina"], info["desc"], deck)
