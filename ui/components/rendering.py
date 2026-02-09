from dataclasses import dataclass

from ecs_framework.primitives import ComponentProtocol


@dataclass(slots=True)
class AlwaysRedraw(ComponentProtocol): ...


@dataclass(slots=True)
class Dirty(ComponentProtocol): ...
