from enum import Enum
import random
from typing import Dict, List

from battle.unit import Party, Unit
from command import AttackCommand, MoveCommand

from model.hex_map import HexCell, HexMap
from model.spawn import SpawnLibrary
from utils.observable import Observable


class BattlePhase(Enum):
    START_BATTLE = 1
    TURN_START = 2
    PLANNING_PHASE = 3
    EXECUTION_PHASE = 4
    TURN_END = 5


class BattleManager:

    def __init__(self, parties: List[Party], battle_map: HexMap):
        self.parties = {party.name: party for party in parties}
        self.turn_manager = TurnManager()
        self.battle_map = Observable(battle_map)
        self.state = Observable(BattlePhase.START_BATTLE)
        self.round = Observable(0)
        self.turn_order = []

    def setup(self) -> None:
        spawn_tuples = zip(self.parties.values(), random.sample(SpawnLibrary.values(), len(self.parties)))
        for party, spawn_kind in spawn_tuples:
            positions = self.battle_map.get().get_spawn_cells(spawn_kind)
            random.shuffle(positions)
            spawn_positions = zip(party.members.values(), positions)
            for unit, cell in spawn_positions:
                cell.unit = unit
                unit.move(cell.coordinate)
        
        self.turn_order = list(self.parties.values())
        random.shuffle(self.turn_order)

    def next_turn(self) -> None:
        self.state.set(BattlePhase.TURN_START)
        self.turn_manager.plan(self.turn_order[0])

    def start_planning(self) -> None:
        self.state.set(BattlePhase.PLANNING_PHASE)


class TurnManager:

    def __init__(self):
        self.party = None
        self.actions: Dict[Unit, PlannedAction] = {}

    def plan(self, party: Party) -> None:
        self.party = party
        # for unit in party.members:
        #     self.actions[unit] = PlannedAction(unit)

    def execute(self) -> None:
        for actions in self.actions.values():
            actions.execute()
        
    # def get_planned_action(self, unit: Unit) -> PlannedAction:
    #     return self.actions.get(unit, None)



class PlannedAction:

    def __init__(self, unit: Unit):
        self.unit = unit
        self.start_position = unit.position
        self.current_position = unit.position
        self.move_range = unit.movement_range
        self.attack_range = unit.attack_range
        self.attack_positions = []
        self.attack_targets = []
        self.move_command: MoveCommand = None
        self.attack_command: List[AttackCommand] = []

    def plan_movement(self, destination: HexCell) -> None:
        if destination == self.current_position:
            return
        self.move_command = MoveCommand(self.unit, self.current_position,  destination)
        self.current_position = destination

    def undo_movement(self) -> None:
        if self.move_command:
            self.current_position = self.move_command.origin
            self.move_command = None

    def plan_attack(self, target: Unit) -> None:
        if target == self.unit or target in self.attack_targets:
            return
        self.attack_command.append(AttackCommand(self.unit, target))
        self.attack_positions.append(target.position)
        self.attack_targets.append(target)

    def undo_attack(self) -> None:
        if self.attack_command:
            attack_command = self.attack_command.pop()
            self.attack_positions.pop()
            self.attack_targets.remove(attack_command.target)

    def execute(self) -> None:
        while self.move_command:
            move_command = self.move_command.pop(0)
            move_command.execute()
        while self.attack_command:
            attack_command = self.attack_command.pop(0)
            attack_command.execute()





