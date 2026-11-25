import json
import os
import random
from core.entity import Entity
from core.card import EnemyAction
from core.effects import build_effects


class Enemy(Entity):
    def __init__(self, name: str, role: str, base_hp: int, is_boss: bool, actions: list[EnemyAction], ng_level: int = 0):
        hp_scale = 1.0 + ng_level * 0.35
        super().__init__(name, int(base_hp * hp_scale))
        self.role = role
        self.is_boss = is_boss
        self.ng_level = ng_level
        self.actions = actions

        self.planned_action: EnemyAction | None = None
        self.last_action_text: str = "Первый ход (действий еще не было)"

    def choose_action(self) -> EnemyAction:
        self.planned_action = random.choice(self.actions)
        return self.planned_action


def load_enemy_pools() -> dict:
    """Загружает все пулы противников из папки data/enemies/."""
    from config import resource_path
    base_dir = resource_path(os.path.join("data", "enemies"))

    with open(os.path.join(base_dir, "regular.json"), "r", encoding="utf-8") as f:
        regular = json.load(f)
    with open(os.path.join(base_dir, "elite.json"), "r", encoding="utf-8") as f:
        elite = json.load(f)
    with open(os.path.join(base_dir, "bosses.json"), "r", encoding="utf-8") as f:
        bosses_data = json.load(f)

    return {
        "regular": regular,
        "elite": elite,
        "act_bosses": bosses_data.get("act_bosses", []),
        "final_bosses": bosses_data.get("final_bosses", []),
    }


def create_enemy_for_stage(stage: int, round_idx: int, ng_level: int = 0) -> Enemy:
    pools = load_enemy_pools()
    action_scale = 1.0 + ng_level * 0.25
    is_boss = (round_idx >= 3)

    if not is_boss:
        if stage == 3:
            chosen = random.choice(pools["elite"])
        elif stage == 1:
            candidates = [e for e in pools["regular"] if e["role"] in ("Гоблин", "Скелет", "Слизняк", "Вор")]
            chosen = random.choice(candidates or pools["regular"])
        else:
            candidates = [e for e in pools["regular"] if e["role"] in ("Огр", "Скелет-стрелок", "Зомби", "Мумия")]
            chosen = random.choice(candidates or pools["regular"])
    else:
        if stage == 3:
            chosen = random.choice(pools["final_bosses"])
        else:
            chosen = random.choice(pools["act_bosses"])

    hp_multiplier = 1.25 if (is_boss and stage == 2) else 1.0
    final_hp = int(chosen["hp"] * hp_multiplier)

    actions = []
    for act in chosen.get("actions", []):
        act_scale = action_scale * (1.15 if (is_boss and stage == 2) else 1.0)
        actions.append(EnemyAction(act["type"], act["name"], build_effects(act.get("effects", [])), scale=act_scale))

    return Enemy(chosen["name"], chosen["role"], final_hp, is_boss=is_boss, actions=actions, ng_level=ng_level)
