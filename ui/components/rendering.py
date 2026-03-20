from dataclasses import dataclass

from omniecs.types import Component


@dataclass(slots=True)
class AlwaysRedraw(Component): ...


@dataclass(slots=True)
class Dirty(Component): ...
