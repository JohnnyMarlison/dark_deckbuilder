from visuals.locations.world1 import draw_dark_forest, draw_abandoned_village, draw_bandit_camp
from visuals.locations.world2 import draw_sand_crypt, draw_ruined_castle, draw_ruined_colosseum
from visuals.locations.world3 import draw_obsidian_citadel, draw_undead_dungeon, draw_ice_crown


def draw_location_background(loc_name: str, t: float):
    name = str(loc_name).strip().lower()
    if "лес" in name:
        draw_dark_forest(t)
    elif "деревня" in name:
        draw_abandoned_village(t)
    elif "лагерь" in name:
        draw_bandit_camp(t)
    elif "склеп" in name:
        draw_sand_crypt(t)
    elif "замок" in name or "замка" in name:
        draw_ruined_castle(t)
    elif "колизей" in name:
        draw_ruined_colosseum(t)
    elif "цитадель" in name:
        draw_obsidian_citadel(t)
    elif "подземелье" in name or "мертвецов" in name:
        draw_undead_dungeon(t)
    elif "ледяная" in name or "корона" in name:
        draw_ice_crown(t)
