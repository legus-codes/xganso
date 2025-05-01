from typing import List, Protocol

from battle.unit import Unit
from model.hex_map import HexCell


class Command(Protocol):

    def execute(self) -> None:
        ...


class MoveCommand(Command):

    def __init__(self, unit: Unit, origin: HexCell, target: HexCell):
        self.unit = unit
        self.origin = origin
        self.target = target

    def execute(self) -> None:
        self.unit.move_to(self.target)

    def __repr__(self) -> str:
        return f'Move {self.unit.name} from {self.origin} to {self.target}'


class AttackCommand(Command):

    def __init__(self, unit: Unit, target: Unit):
        self.unit = unit
        self.target = target

    def execute(self) -> None:
        self.target.take_damage(self.unit.attack)

    def __repr__(self) -> str:
        return f'Attack {self.unit.name} ({self.unit.attack}) to {self.target.name} ({self.target.hp} hp)'


class CommandQueue:

    def __init__(self):
        self.queue: List[Command] = []

    def add_command(self, command: Command):
        self.queue.append(command)

    def get_command(self) -> Command:
        return self.queue.pop(0)

    def undo_command(self) -> None:
        self.queue.pop()

    def execute_all_commands(self) -> None:
        while not self.is_empty:
            command = self.get_command()
            command.execute()

    def get_move_command(self, unit: Unit) -> MoveCommand:
        for command in self.queue:
            if isinstance(command, MoveCommand):
                if command.unit == unit:
                    return command
        return None

    @property
    def is_empty(self) -> bool:
        return len(self.queue) == 0
