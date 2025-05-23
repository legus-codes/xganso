from typing import List

from model.hex_map_commands import HexMapCommand
from model.hex_map import HexMap
from utils.observable import Observable


class HexMapModel:
    
    def __init__(self, hex_map: HexMap):
        self.hex_map = Observable(hex_map)
        self.history: List[HexMapCommand] = []

    def set_hex_map(self, hex_map: HexMap) -> None:
        self.hex_map.set(hex_map)
        self.history = []

    def apply_command(self, command: HexMapCommand) -> None:
        command.execute()
        self.history.append(command)

    def undo(self) -> None:
        if self.history:
            command = self.history.pop()
            command.undo()
