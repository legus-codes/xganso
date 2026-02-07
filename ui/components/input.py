from dataclasses import dataclass
from enum import Enum

from ecs_framework.ecs import ComponentProtocol
from core.primitives import IVec2


class Key(Enum):
    DELETE = 8
    ENTER = 13


class MouseButton(Enum):
    left = 1
    right = 3


@dataclass(slots=True)
class KeyDown(ComponentProtocol):
    char: str
    key: int


@dataclass(slots=True)
class MouseMove(ComponentProtocol):
    position: IVec2


@dataclass(slots=True)
class MouseClick(ComponentProtocol):
    button: MouseButton
    position: IVec2


@dataclass(slots=True)
class MouseRelease(ComponentProtocol):
    button: MouseButton
    position: IVec2


@dataclass(slots=True)
class MousePress(ComponentProtocol):
    button: MouseButton
    position: IVec2
