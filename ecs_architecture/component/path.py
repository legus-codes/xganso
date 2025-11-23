from typing import List

from ecs_framework.ecs import ComponentProtocol
from model.hex_coordinate import HexCoordinate, VecF2
from model.hex_map import HexCell


class TargetGridPosition(ComponentProtocol):
    cell: HexCoordinate


class PreviewPath(ComponentProtocol):
    path: List[HexCoordinate]


class Path(ComponentProtocol):
    path: List[HexCell]


class MoveCommand(ComponentProtocol):
    pass


class MovementProgress(ComponentProtocol):
    origin: VecF2
    destination: VecF2
    cell: HexCoordinate
    progress: float = 0.0
