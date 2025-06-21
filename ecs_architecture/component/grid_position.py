from dataclasses import dataclass

from ecs_framework.ecs import ComponentProtocol


@dataclass
class GridPosition(ComponentProtocol):
    q: int
    r: int
