from enum import Enum

from ecs_framework.ecs import ComponentProtocol
from ui.primitives import IVec2


class Key(Enum):
    DELETE = 8
    ENTER = 13


class MouseButton(Enum):
    left = 1
    right = 3


class KeyDown(ComponentProtocol):
    char: str
    key: int


class MouseMove(ComponentProtocol):
    position: IVec2


class MouseClick(ComponentProtocol):
    button: MouseButton
    position: IVec2


class MouseRelease(ComponentProtocol):
    button: MouseButton
    position: IVec2


class MousePress(ComponentProtocol):
    button: MouseButton
    position: IVec2
