from dataclasses import dataclass

from ecs_framework.ecs import ComponentProtocol
from model.hex_coordinate import HexCoordinate, VecF2


@dataclass
class GridPosition(ComponentProtocol):
    cell: HexCoordinate


@dataclass
class GridPositionChanged(ComponentProtocol):
    pass


@dataclass
class WorldPosition(ComponentProtocol):
    point: VecF2


@dataclass
class ScreenPosition(ComponentProtocol):
    point: VecF2

