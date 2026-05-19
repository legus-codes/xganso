from typing import List

from omniecs.types import Component
from model.hex_coordinate import HexCoordinate, VecF2
from model.hex_map import HexCell


class TargetGridPosition(Component):
    cell: HexCoordinate


class PreviewPath(Component):
    path: List[HexCoordinate]


class Path(Component):
    path: List[HexCell]


class MoveCommand(Component):
    pass


class MovementProgress(Component):
    origin: VecF2
    destination: VecF2
    cell: HexCoordinate
    progress: float = 0.0
