from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from ecs_framework.ecs import ComponentProtocol


class Key(Enum):
    DELETE = 8
    ENTER = 13


class MouseButton(Enum):
    left = 1
    right = 3


@dataclass
class KeyDown(ComponentProtocol):
    char: str
    key: int


@dataclass
class MousePosition(ComponentProtocol):
    position: Tuple[int, int]


@dataclass
class MouseClicked(ComponentProtocol):
    button: MouseButton
    position: Tuple[int, int]


@dataclass
class MouseReleased(ComponentProtocol):
    button: MouseButton
    position: Tuple[int, int]


@dataclass
class MousePressed(ComponentProtocol):
    button: MouseButton
