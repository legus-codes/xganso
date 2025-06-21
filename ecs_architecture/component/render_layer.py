from dataclasses import dataclass

from ecs_framework.ecs import ComponentProtocol


@dataclass
class RenderLayer(ComponentProtocol):
    z: int
