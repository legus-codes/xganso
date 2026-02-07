from dataclasses import dataclass
from enum import Enum

from ecs_framework.ecs import EventProtocol
from core.primitives import IVec2


class Key(Enum):
    DELETE = 8
    ENTER = 13


class MouseButton(Enum):
    left = 1
    right = 3


@dataclass(slots=True)
class KeyDown(EventProtocol):
    char: str
    key: int


@dataclass(slots=True)
class MouseMove(EventProtocol):
    position: IVec2


@dataclass(slots=True)
class MouseButtonDown(EventProtocol):
    position: IVec2
    button: MouseButton


@dataclass(slots=True)
class MouseButtonUp(EventProtocol):
    position: IVec2
    button: MouseButton


@dataclass(slots=True)
class QuitRequested(EventProtocol): ...
