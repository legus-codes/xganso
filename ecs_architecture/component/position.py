from ecs_framework.ecs import ComponentProtocol
from model.hex_coordinate import HexCoordinate, VecF2


class GridPosition(ComponentProtocol):
    cell: HexCoordinate


class GridPositionChanged(ComponentProtocol):
    pass


class WorldPosition(ComponentProtocol):
    point: VecF2


class ScreenPosition(ComponentProtocol):
    point: VecF2

