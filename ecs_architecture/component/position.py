from omniecs.types import Component
from model.hex_coordinate import HexCoordinate, VecF2


class GridPosition(Component):
    cell: HexCoordinate


class GridPositionChanged(Component):
    pass


class WorldPosition(Component):
    point: VecF2


class ScreenPosition(Component):
    point: VecF2

