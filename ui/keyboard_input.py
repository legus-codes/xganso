from dataclasses import dataclass
from enum import Enum

from ecs_framework.ecs import ComponentProtocol


class Key(Enum):
    DELETE = 8
    ENTER = 13


@dataclass
class KeyDown(ComponentProtocol):
    char: str
    key: int
