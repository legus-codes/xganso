from dataclasses import dataclass
from enum import Enum

from core.primitives import IVec2
from omniecs.types import Event


class Key(Enum):
    DELETE = 8
    ENTER = 13


class MouseButton(Enum):
    left = 1
    right = 3


@dataclass(slots=True)
class KeyDown(Event):
    key: int


@dataclass(slots=True)
class KeyUp(Event):
    key: int


@dataclass(slots=True)
class TextInput(Event):
    text: str


@dataclass(slots=True)
class MouseMove(Event):
    position: IVec2


@dataclass(slots=True)
class MouseButtonDown(Event):
    position: IVec2
    button: MouseButton


@dataclass(slots=True)
class MouseButtonUp(Event):
    position: IVec2
    button: MouseButton


@dataclass(slots=True)
class QuitRequested(Event): ...
