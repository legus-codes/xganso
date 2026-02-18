from dataclasses import dataclass

from ecs_framework.types import Component


@dataclass(slots=True)
class AlwaysRedraw(Component): ...


@dataclass(slots=True)
class Dirty(Component): ...
