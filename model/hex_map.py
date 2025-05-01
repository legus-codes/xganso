from collections.abc import Iterable
from dataclasses import dataclass
from typing import Dict, List, Optional

from battle.unit import Unit
from model.hex_coordinate import HexCoordinate
from model.terrain import Terrain
from model.spawn import Spawn, SpawnLibrary


@dataclass
class HexCell:
    coordinate: HexCoordinate
    terrain: Terrain
    spawn: Spawn
    unit: Optional[Unit]

    @property
    def color(self) -> str:
        return self.terrain.color

    @property
    def frame_color(self) -> str:
        return self.spawn.color

    @property
    def is_occupied(self) -> bool:
        return self.unit is not None

    @property
    def is_traversable(self) -> bool:
        return self.terrain.walkable and not self.is_occupied


class HexMap:
    
    def __init__(self, cells: Dict[HexCoordinate, HexCell]):
        self.cells = cells

    def __getitem__(self, coordinate: HexCoordinate) -> Optional[HexCell]:
        return self.cells[coordinate]
    
    def __contains__(self, coordinate: HexCoordinate) -> bool:
        return coordinate in self.cells

    def __iter__(self) -> Iterable[HexCell]:
        return iter(self.cells.values())

    @property
    def coordinates(self) -> List[HexCoordinate]:
        return list(self.cells.keys())

    @property
    def sorted_cells(self) -> List[HexCell]:
        return sorted(self.cells.values(), key=lambda cell: cell.spawn.spawn_type)

    def add_cell(self, coordinate: HexCoordinate, terrain: Terrain) -> None:
        self.cells[coordinate] = HexCell(coordinate, terrain, SpawnLibrary.none(), None)

    def delete_cell(self, coordinate: HexCoordinate) -> None:
        self.cells.pop(coordinate)
    
    def change_terrain(self, coordinate: HexCoordinate, terrain: Terrain) -> None:
        self.cells[coordinate].terrain = terrain

    def change_spawn(self, coordinate: HexCoordinate, spawn: Spawn) -> None:
        self.cells[coordinate].spawn = spawn

    def remove_spawn(self, coordinate: HexCoordinate) -> None:
        self.change_spawn(coordinate, SpawnLibrary.none())

    def get_terrain(self, coordinate: HexCoordinate) -> Terrain:
        return self.cells[coordinate].terrain    

    def get_spawn(self, coordinate: HexCoordinate) -> Spawn:
        return self.cells[coordinate].spawn

    def has_spawn(self, coordinate: HexCoordinate) -> bool:
        return self.get_spawn(coordinate) != SpawnLibrary.none()
    
    def get_spawn_cells(self, spawn: Spawn) -> List[HexCell]:
        return [cell for coordinate, cell in self.cells.items() if self.get_spawn(coordinate) == spawn]
