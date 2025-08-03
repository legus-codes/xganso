from dataclasses import dataclass

from ecs_framework.ecs import ComponentProtocol


@dataclass
class Attack(ComponentProtocol):
    base: int
    growth: int


@dataclass
class Defense(ComponentProtocol):
    base: int
    growth: int


@dataclass
class HP(ComponentProtocol):
    current: int
    max_value: int
    regeneration: int
    growth: int
