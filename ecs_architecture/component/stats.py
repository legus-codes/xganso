from dataclasses import dataclass

from ecs_framework.ecs import ComponentProtocol


@dataclass
class Stats(ComponentProtocol):
    attack: int
    defense: int
    hp: int
    max_hp: int
