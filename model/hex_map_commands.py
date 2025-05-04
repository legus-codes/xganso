from typing import Protocol

from model.hex_coordinate import HexCoordinate
from model.hex_map import HexMap
from model.terrain import Terrain
from model.spawn import Spawn


class HexMapCommand(Protocol):

    def execute(self) -> None:
        ...

    def undo(self) -> None:
        ...


class CreateTileCommand(HexMapCommand):

    def __init__(self, hex_map: HexMap, coordinate: HexCoordinate, terrain: Terrain):
        self.hex_map = hex_map
        self.coordinate = coordinate
        self.terrain = terrain

    def execute(self) -> None:
        self.hex_map.add_cell(self.coordinate, self.terrain)

    def undo(self) -> None:
        self.hex_map.delete_cell(self.coordinate)
    

class PaintTileCommand(HexMapCommand):

    def __init__(self, hex_map: HexMap, coordinate: HexCoordinate, terrain: Terrain, old_terrain: Terrain):
        self.hex_map = hex_map
        self.coordinate = coordinate
        self.terrain = terrain
        self.old_terrain = old_terrain

    def execute(self) -> None:
        self.hex_map.change_terrain(self.coordinate, self.terrain)

    def undo(self) -> None:
        self.hex_map.change_terrain(self.coordinate, self.old_terrain)


class EraseTileCommand(HexMapCommand):

    def __init__(self, hex_map: HexMap, coordinate: HexCoordinate, old_terrain: Terrain):
        self.hex_map = hex_map
        self.coordinate = coordinate
        self.old_terrain = old_terrain

    def execute(self) -> None:
        self.hex_map.delete_cell(self.coordinate)

    def undo(self) -> None:
        self.hex_map.add_cell(self.coordinate, self.old_terrain)


class ChangeSpawnCommand(HexMapCommand):

    def __init__(self, hex_map: HexMap, coordinate: HexCoordinate, spawn: Spawn, old_spawn: Spawn):
        self.hex_map = hex_map
        self.coordinate = coordinate
        self.spawn = spawn
        self.old_spawn = old_spawn

    def execute(self) -> None:
        self.hex_map.change_spawn(self.coordinate, self.spawn)

    def undo(self) -> None:
        self.hex_map.change_spawn(self.coordinate, self.old_spawn)


class RemoveSpawnCommand(HexMapCommand):

    def __init__(self, hex_map: HexMap, coordinate: HexCoordinate, old_spawn: Spawn):
        self.hex_map = hex_map
        self.coordinate = coordinate
        self.old_spawn = old_spawn

    def execute(self) -> None:
        self.hex_map.remove_spawn(self.coordinate)

    def undo(self) -> None:
        self.hex_map.change_spawn(self.coordinate, self.old_spawn)
