from core.run_state import RunState
from core.enemy import Enemy, create_enemy_for_stage
from core.card import Card, EnemyAction
from core.effects import CombatEvent
from core.records import update_record, check_stage_achievements


class CombatEngine:
    """Чистый боевой движок: управляет ходами, правилами и переходами без привязки к графике."""

    def __init__(self, run: RunState):
        self.run = run
        self.hero = run.hero
        self.enemy: Enemy | None = None

    def setup_encounter(self) -> Enemy:
        self.hero.prepare_for_battle()
        self.enemy = create_enemy_for_stage(self.run.stage, self.run.round_idx, self.run.ng_level)
        return self.enemy

    def begin_player_turn(self) -> list[CombatEvent]:
        events = self.hero.trigger_turn_start()
        self.hero.start_turn()
        if self.enemy:
            self.enemy.choose_action()
        return events

    def can_play_card(self, card: Card) -> bool:
        return self.hero.stamina >= card.cost

    def play_player_card(self, card: Card) -> tuple[list[CombatEvent], str]:
        """Разыгрывает карту героя. Возвращает (события_боя, статус_боя: 'CONTINUE' | 'STAGE_REWARD' | 'BOSS_REWARD' | 'FINAL_VICTORY')."""
        if not self.enemy or not self.can_play_card(card):
            return [], "CONTINUE"

        self.hero.stamina -= card.cost
        if card in self.hero.hand:
            self.hero.hand.remove(card)
        # Сначала применяем эффекты (добор тянет только из старого сброса/колоды)
        events = card.play(self.hero, self.enemy)

        if not getattr(card, "exhaust", False):
            self.hero.discard_pile.append(card)


        if not self.enemy.is_alive:
            check_stage_achievements(self.hero.name, self.run.stage, self.run.ng_level, self.enemy.role)
            if self.run.round_idx < 3:
                return events, "STAGE_REWARD"
            elif self.run.stage < 3:
                return events, "BOSS_REWARD"
            else:
                update_record(self.hero.name, won=True, turns=self.run.total_turns, ng_level=self.run.ng_level)
                return events, "FINAL_VICTORY"

        return events, "CONTINUE"

    def end_player_turn(self) -> EnemyAction | None:
        self.hero.trigger_turn_end()
        self.hero.end_turn()
        return self.enemy.planned_action if self.enemy else None

    def resolve_enemy_turn(self) -> tuple[list[CombatEvent], str]:
        """Выполняет ход врага. Возвращает (события_боя, статус: 'CONTINUE' | 'GAME_OVER')."""
        if not self.enemy or not self.enemy.planned_action:
            return [], "CONTINUE"

        self.enemy.reset_block()
        events = self.enemy.trigger_turn_start()
        act = self.enemy.planned_action
        events.extend(act.execute(self.enemy, self.hero))
        events.extend(self.enemy.trigger_turn_end())

        self.enemy.last_action_text = f"[{act.action_type}] {act.name}: {act.desc}"

        if not self.hero.is_alive:
            update_record(self.hero.name, won=False, turns=self.run.total_turns, ng_level=self.run.ng_level)
            return events, "GAME_OVER"

        self.run.total_turns += 1
        return events, "CONTINUE"
