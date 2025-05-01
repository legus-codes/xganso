from enum import Enum, auto
import random
from typing import List

from battle.unit import Character, Party
from map import BattleMap
from battle.battle import TurnManager


class Phase(Enum):
    Planning = auto()
    Execution = auto()


class GameManager:

    def __init__(self, player_team: Party, enemy_team: Party, battle_map: BattleMap):
        self.player_team = player_team
        self.enemy_team = enemy_team
        self.battle_map = battle_map
        self.phase = None
        self.turn_manager = TurnManager()

    @property
    def characters(self) -> List[Character]:
        return self.player_team.members + self.enemy_team.members

    def setup_battle(self) -> None:
        self.assign_starting_positions()
        self.decide_starting_team()

    def assign_starting_positions(self) -> None:
        starting_positions = self.battle_map.get_starting_positions(self.player_team.count, self.enemy_team.count)
        for character, position in zip(self.player_team.members, starting_positions[0]):
            character.set_position(position)
        for character, position in zip(self.enemy_team.members, starting_positions[1]):
            character.set_position(position)

    def decide_starting_team(self) -> None:
        starting_team = self.player_team if random.choice([True, False]) else self.enemy_team
        self.phase = Phase.Planning
        self.turn_manager.plan(starting_team)

    def change_phase(self, phase: Phase) -> None:
        self.phase = phase
