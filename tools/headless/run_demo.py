#!/usr/bin/env python3
"""Headless-демонстрация исправной работы игры в песочнице без OpenGL.

Что делает:
  1. Логический smoke-тест чистого боя (core/ без графики).
  2. Прогоняет НАСТОЯЩИЕ view проекта (меню → выбор героя → бой → награда →
     босс → награда босса → следующий мир) через заглушку arcade
     (tools/headless/arcade) и рисует кадры в PNG.

Запуск:  python3 tools/headless/run_demo.py   (из корня репозитория)
Выход:   tools/headless/out/*.png
"""

from __future__ import annotations

import os
import random
import shutil
import sys
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

# Порядок важен: сначала корень проекта, потом стаб arcade (перетирает site-packages)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)
os.chdir(ROOT)

import arcade  # заглушка (tools/headless/arcade) — НЕ настоящий arcade
import headless_render as renderer
from config import SCREEN_WIDTH, SCREEN_HEIGHT

OUT_DIR = os.path.join(HERE, "out")
RECORDS = os.path.join(ROOT, "records.json")
RECORDS_BACKUP = os.path.join(HERE, "records.backup.json")

MOUSE_LEFT = arcade.MOUSE_BUTTON_LEFT


# ---------------------------------------------------------------- helpers

def snap(win, name: str) -> None:
    arcade.begin_frame()
    win.on_draw()
    ops = arcade.get_frame_ops()
    path = os.path.join(OUT_DIR, f"{name}.png")
    renderer.render(ops, SCREEN_WIDTH, SCREEN_HEIGHT, arcade.get_background_color(), path)
    print(f"  [snap] {name}.png  ({len(ops)} draw-операций)")


def pump(win, seconds: float, dt: float = 1 / 30) -> None:
    for _ in range(max(1, int(round(seconds / dt)))):
        win.on_update(dt)


def press(view, x: float, y: float) -> None:
    view.on_mouse_press(x, y, MOUSE_LEFT, 0)


def motion(view, x: float, y: float) -> None:
    view.on_mouse_motion(x, y, 0, 0)


def logic_smoke_test() -> None:
    """Проверка чистого боевого движка (core) без графики."""
    print("[1] Логический smoke-тест боя (core)...")
    from core.run_state import RunState
    from core.combat import CombatEngine

    run = RunState("Воин")
    eng = CombatEngine(run)
    enemy = eng.setup_encounter()
    eng.begin_player_turn()
    status = "CONTINUE"
    turns = 0
    for _ in range(80):
        if not enemy.is_alive:
            break
        affordable = [c for c in run.hero.hand if run.hero.stamina >= c.cost]
        if affordable:
            dmg = next((c for c in affordable if c.has_damage), affordable[0])
            _events, status = eng.play_player_card(dmg)
            if status != "CONTINUE":
                break
        else:
            eng.end_player_turn()
            _events, status = eng.resolve_enemy_turn()
            if status == "GAME_OVER":
                break
            eng.begin_player_turn()
            turns += 1
    print(f"      враг «{enemy.name}»: {enemy.hp}/{enemy.max_hp} HP, "
          f"герой: {run.hero.hp}/{run.hero.max_hp} HP, ходов: {turns}, статус: {status}")
    if enemy.is_alive and status != "GAME_OVER":
        raise AssertionError("бой не завершился за 80 итераций")


def choose_card(view, affordable):
    hero = view.hero
    ratio = hero.hp / max(1, hero.max_hp)

    def prio(widget):
        t = getattr(widget.data, "card_type", "")
        if t == "Исцеление":
            return 0 if ratio < 0.75 else 6
        if t == "Защита":
            return 1 if ratio < 0.6 else 5
        if t == "Атака":
            return 2
        if t == "Заклинание":
            return 3
        return 4

    return min(affordable, key=prio)


def fight_current_battle(win, snaps: dict[str, str], max_iters: int = 400):
    """Играет текущий BattleView до перехода на другой экран.

    Возвращает ("stage_reward"|"boss"|"defeat"|"switched", view).
    """
    from views.battle.battle_view import BattleView
    from views.rewards.stage_reward_view import StageRewardView

    for _ in range(max_iters):
        v = win._view
        if not isinstance(v, BattleView):
            if isinstance(v, StageRewardView):
                return ("stage_reward", v)
            return ("switched", v)
        if v.substate == "GAME_OVER":
            return ("defeat", v)
        if v.substate == "BOSS_VICTORY":
            return ("boss", v)

        if v.playing_widget:
            name = snaps.pop("action", None)
            if name:
                pump(win, 0.12)
                snap(win, name)
                pump(win, 0.5)
            else:
                pump(win, 0.5)
            continue

        if v.enemy_attack_pending:
            name = snaps.pop("enemy", None)
            if name:
                pump(win, 0.30)
                snap(win, name)
                pump(win, 1.0)
            else:
                pump(win, 1.1)
            continue

        # ждём, пока карты доедут до целевых позиций (contains_point меряет x/y)
        if any(abs(w.x - w.target_x) > 4 or abs(w.y - w.target_y) > 4 for w in v.hand_widgets):
            pump(win, 0.2)
            continue

        affordable = [w for w in v.hand_widgets if v.hero.stamina >= w.cost]
        if affordable:
            w = choose_card(v, affordable)
            press(v, w.x, w.y)  # кликаем по видимой позиции карты
            if not v.playing_widget:
                pump(win, 0.1)  # промах — повторим после кадра анимации
            continue

        press(v, v.end_turn_btn[0], v.end_turn_btn[1])
        if not v.enemy_attack_pending:
            pump(win, 0.1)
    raise RuntimeError("бой не завершился за max_iters итераций")


def take_stage_reward(win) -> None:
    from views.rewards.stage_reward_view import StageRewardView
    v = win._view
    assert isinstance(v, StageRewardView), f"ожидался StageRewardView, получен {type(v).__name__}"
    x, y = v.options[0]["x"], 530  # «Источник жизни» — полное лечение
    motion(v, x, y)
    pump(win, 0.1)
    press(v, x, y)


def run_once(seed: int) -> None:
    random.seed(seed)
    os.makedirs(OUT_DIR, exist_ok=True)

    print(f"[2] Запуск окна игры (GameWindow), seed={seed}...")
    from main import GameWindow
    from views.menu.menu_view import MenuView
    from views.menu.hero_select_view import HeroSelectView
    from views.battle.battle_view import BattleView

    win = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, "headless")
    win.show_view(MenuView())
    pump(win, 1.35)  # ждём первую анимацию «каста» в витрине меню
    snap(win, "01_menu")

    print("[3] Клик «ИГРАТЬ» → выбор героя...")
    press(win._view, SCREEN_WIDTH / 2, 715)
    assert isinstance(win._view, HeroSelectView), type(win._view)
    hs = win._view
    hx, hy = hs.hero_cards[0]["x"], hs.hero_cards[0]["y"]
    motion(hs, hx, hy)
    pump(win, 0.4)
    snap(win, "02_hero_select")

    print(f"[4] Выбран герой «{hs.hero_cards[0]['name']}» → бой, раунд 1...")
    press(hs, hx, hy)
    assert isinstance(win._view, BattleView), type(win._view)
    pump(win, 1.0)
    snap(win, "03_battle_round1")

    result, v = fight_current_battle(win, {
        "action": "04_battle_card_play",
        "enemy": "05_battle_enemy_turn",
    })
    assert result == "stage_reward", f"раунд 1: ожидалась награда, получено {result}"
    pump(win, 0.2)
    snap(win, "06_stage_reward")
    print("[5] Награда за раунд 1 → лечение, раунд 2...")
    take_stage_reward(win)

    result, v = fight_current_battle(win, {})
    assert result == "stage_reward", f"раунд 2: ожидалась награда, получено {result}"
    take_stage_reward(win)

    print("[6] Раунд 3 — босс мира 1...")
    assert isinstance(win._view, BattleView)
    pump(win, 0.8)
    snap(win, "07_boss_round")

    result, v = fight_current_battle(win, {})
    assert result == "boss", f"ожидалась победа над боссом, получено {result}"
    snap(win, "08_boss_victory")

    print("[7] Выбор 2 карт в награду за босса...")
    rw = v.modals.reward_widgets
    press(v, rw[0].x, rw[0].y)
    press(v, rw[1].x, rw[1].y)
    bx, by = v.modals.boss_next_btn[:2]
    press(v, bx, by)

    assert isinstance(win._view, BattleView) and win._view.run.stage == 2, (
        f"не перешли во 2 мир: {type(win._view).__name__}, "
        f"stage={win._view.run.stage if isinstance(win._view, BattleView) else None}"
    )
    pump(win, 1.0)
    snap(win, "09_world2_battle")


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    had_records = os.path.exists(RECORDS)
    if had_records:
        shutil.copy2(RECORDS, RECORDS_BACKUP)

    try:
        logic_smoke_test()

        seeds = (42, 7, 3, 100, 2025, 555, 8, 31337, 12, 99)
        last_err = None
        for seed in seeds:
            print(f"\n=== попытка seed={seed} ===")
            try:
                run_once(seed)
                print(f"\nГОТОВО (seed={seed}): меню → выбор героя → 3 раунда → "
                      f"победа над боссом → 2-й мир. Скриншоты в tools/headless/out/.")
                return
            except AssertionError as e:
                print(f"[!] seed={seed} не прошёл: {e}")
                last_err = e
                continue
        raise RuntimeError(f"ни один seed не прошёл проверку: {last_err}")
    finally:
        if had_records and os.path.exists(RECORDS_BACKUP):
            shutil.copy2(RECORDS_BACKUP, RECORDS)
            os.remove(RECORDS_BACKUP)
            print("[i] records.json восстановлен из бэкапа.")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
