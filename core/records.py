import json
import os

RECORDS_FILE = "records.json"
DEFAULT_HEROES = ("Воин", "Элементалист", "Паладин", "Ассасин")

ACHIEVEMENTS_CATALOG = (
    {"id": "warrior_1", "title": "Воин: Шаг в бездну", "desc": "Пройдите 1-й уровень за Воина", "icon": "Защита"},
    {"id": "warrior_2", "title": "Воин: Закаленный в боях", "desc": "Пройдите 2-й уровень за Воина", "icon": "Защита"},
    {"id": "warrior_3", "title": "Воин: Покоритель тьмы", "desc": "Пройдите все 3 уровня за Воина", "icon": "Атака"},

    {"id": "mage_1", "title": "Элементалист: Первая искра", "desc": "Пройдите 1-й уровень за Пироманта", "icon": "Заклинание"},
    {"id": "mage_2", "title": "Элементалист: Неугасимое пламя", "desc": "Пройдите 2-й уровень за Пироманта", "icon": "Заклинание"},
    {"id": "mage_3", "title": "Элементалист: Повелитель пепла", "desc": "Пройдите все 3 уровня за Пироманта", "icon": "Заклинание"},

    {"id": "paladin_1", "title": "Паладин: Луч надежды", "desc": "Пройдите 1-й уровень за Паладина", "icon": "Исцеление"},
    {"id": "paladin_2", "title": "Паладин: Щит рассвета", "desc": "Пройдите 2-й уровень за Паладина", "icon": "Исцеление"},
    {"id": "paladin_3", "title": "Паладин: Небесный триумф", "desc": "Пройдите все 3 уровня за Паладина", "icon": "Исцеление"},

    {"id": "assassin_1", "title": "Ассасин: Тень клинка", "desc": "Пройдите 1-й уровень за Ассасина", "icon": "Атака"},
    {"id": "assassin_2", "title": "Ассасин: Смертельный танец", "desc": "Пройдите 2-й уровень за Ассасина", "icon": "Атака"},
    {"id": "assassin_3", "title": "Ассасин: Призрак бездны", "desc": "Пройдите все 3 уровня за Ассасина", "icon": "Атака"},

    {"id": "ng_plus_win", "title": "Испытание кошмаром", "desc": "Пройдите игру в усложненном режиме (НГ+)", "icon": "Заклинание"},
    {"id": "slay_dark_knight", "title": "Падение Тёмного Властелина", "desc": "Одолейте редкого Тёмного Магического Рыцаря", "icon": "Атака"},
)

HERO_PREFIX = {"Воин": "warrior", "Элементалист": "mage", "Паладин": "paladin", "Ассасин": "assassin"}

# Глобальная очередь новых полученных достижений для всплывающих уведомлений
PENDING_ACHIEVEMENT_POPUPS: list[dict] = []


def load_records() -> dict:
    data = {
        "heroes": {
            hero: {"wins": 0, "games": 0, "best_turns": None, "max_ng": 0}
            for hero in DEFAULT_HEROES
        },
        "achievements": [],
        "seen_enemies": [],
        "seen_cards": [],
    }
    if os.path.exists(RECORDS_FILE):
        try:
            with open(RECORDS_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                if "heroes" in saved:
                    for h in DEFAULT_HEROES:
                        if h in saved["heroes"]:
                            data["heroes"][h].update(saved["heroes"][h])
                    data["achievements"] = list(saved.get("achievements", []))
                    data["seen_enemies"] = list(saved.get("seen_enemies", []))
                    data["seen_cards"] = list(saved.get("seen_cards", []))
                else:
                    for h in DEFAULT_HEROES:
                        if h in saved:
                            data["heroes"][h].update(saved[h])
        except (OSError, json.JSONDecodeError):
            pass
    return data



def _save_records(data: dict):
    with open(RECORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def unlock_achievement(ach_id: str):
    data = load_records()
    if ach_id not in data["achievements"]:
        data["achievements"].append(ach_id)
        _save_records(data)
        for item in ACHIEVEMENTS_CATALOG:
            if item["id"] == ach_id:
                PENDING_ACHIEVEMENT_POPUPS.append(item)
                break


def check_stage_achievements(hero_name: str, cleared_stage: int, ng_level: int, enemy_role: str):
    """Вызывается после победы над каждым врагом."""
    prefix = HERO_PREFIX.get(hero_name)
    if prefix and 1 <= cleared_stage <= 3:
        unlock_achievement(f"{prefix}_{cleared_stage}")

    if cleared_stage >= 3 and ng_level >= 1:
        unlock_achievement("ng_plus_win")

    if enemy_role == "Тёмный Рыцарь":
        unlock_achievement("slay_dark_knight")


def update_record(hero_name: str, won: bool, turns: int, ng_level: int = 0):
    data = load_records()
    heroes = data["heroes"]
    if hero_name not in heroes:
        heroes[hero_name] = {"wins": 0, "games": 0, "best_turns": None, "max_ng": 0}

    heroes[hero_name]["games"] += 1
    if won:
        heroes[hero_name]["wins"] += 1
        if ng_level > heroes[hero_name].get("max_ng", 0):
            heroes[hero_name]["max_ng"] = ng_level
        current_best = heroes[hero_name]["best_turns"]
        if current_best is None or turns < current_best:
            heroes[hero_name]["best_turns"] = turns

    _save_records(data)

def mark_enemy_seen(enemy_name: str):
    """Открывает врага или босса в Энциклопедии при первой встрече в бою."""
    if not enemy_name:
        return
    data = load_records()
    if enemy_name not in data["seen_enemies"]:
        data["seen_enemies"].append(enemy_name)
        _save_records(data)


def mark_cards_seen(card_ids: list[str]):
    """Открывает карты в Каталоге при их первом появлении в руке."""
    if not card_ids:
        return
    data = load_records()
    changed = False
    for cid in card_ids:
        base_id = cid.replace("_plus", "")
        if base_id not in data["seen_cards"]:
            data["seen_cards"].append(base_id)
            changed = True
    if changed:
        _save_records(data)
