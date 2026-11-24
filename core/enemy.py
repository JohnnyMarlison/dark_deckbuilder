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


def create_enemy_for_stage(stage: int, round_idx: int, ng_level: int = 0) -> Enemy:
    action_scale = 1.0 + ng_level * 0.25
    is_boss = (round_idx >= 3)

    if stage == 3 and not is_boss:
        elite_pool = [
            {
                "name": "ЭЛИТА: Костяной Страж с Топором",
                "role": "Огр",
                "hp": 130,
                "actions": [
                    {"type": "Атака", "name": "Казнящий замах", "effects": [{"type": "damage", "value": 18}]},
                    {"type": "Защита", "name": "Тяжелый доспех стражи", "effects": [{"type": "block", "value": 15}]},
                ],
            },
            {
                "name": "ЭЛИТА: Чёрный Скелет-Маг",
                "role": "Злой Волшебник",
                "hp": 110,
                "actions": [
                    {"type": "Заклинание", "name": "Стрела Бездны", "effects": [{"type": "damage", "value": 14}]},
                    {"type": "Заклинание", "name": "Проклятие увядания", "effects": [{"type": "damage", "value": 8}, {"type": "steal_stamina", "value": 1}]},
                ],
            },
        ]
        chosen = random.choice(elite_pool)
        actions = [EnemyAction(a["type"], a["name"], build_effects(a.get("effects", [])), scale=action_scale) for a in chosen["actions"]]
        return Enemy(chosen["name"], chosen["role"], chosen["hp"], is_boss=False, actions=actions, ng_level=ng_level)

    path = os.path.join("data/enemies", "enemies.json")
    with open(path, "r", encoding="utf-8") as f:
        pool_data = json.load(f)

    if not is_boss:
        sub_pool = pool_data["regular"]
        if stage == 1:
            candidates = [e for e in sub_pool if e["role"] in ("Гоблин", "Скелет", "Слизняк", "Вор")]
        else:
            candidates = [e for e in sub_pool if e["role"] in ("Огр", "Скелет-стрелок", "Зомби", "Мумия")]
        if not candidates:
            candidates = sub_pool
        chosen = random.choice(candidates)
    else:
        if stage == 3:
            rare_list = pool_data.get("rare_bosses", [])
            chosen = rare_list[0] if rare_list else random.choice(pool_data["bosses"])
        else:
            chosen = random.choice(pool_data["bosses"])

    hp_multiplier = 1.25 if (is_boss and stage == 2) else 1.0
    final_hp = int(chosen["hp"] * hp_multiplier)

    actions = []
    for act in chosen.get("actions", []):
        act_scale = action_scale * (1.15 if (is_boss and stage == 2) else 1.0)
        actions.append(EnemyAction(act["type"], act["name"], build_effects(act.get("effects", [])), scale=act_scale))

    return Enemy(chosen["name"], chosen["role"], final_hp, is_boss=is_boss, actions=actions, ng_level=ng_level)
