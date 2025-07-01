from dataclasses import dataclass
from typing import List

from ecs_framework.ecs import ComponentProtocol
from model.hex_coordinate import HexCoordinate, VecF2
from model.hex_map import HexCell


@dataclass
class TargetGridPosition(ComponentProtocol):
    cell: HexCoordinate


@dataclass
class PreviewPath(ComponentProtocol):
    path: List[HexCoordinate]


@dataclass
class Path(ComponentProtocol):
    path: List[HexCell]


@dataclass
class MoveCommand(ComponentProtocol):
    pass


@dataclass
class MovementProgress(ComponentProtocol):
    origin: VecF2
    destination: VecF2
    cell: HexCoordinate
    progress: float = 0.0
