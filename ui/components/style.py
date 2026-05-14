from dataclasses import dataclass

from omniecs.types import Component
from core.primitives import Color


@dataclass(slots=True)
class Background(Component):
    color: Color


@dataclass(slots=True)
class Frame(Component):
    color: Color
    width: int


@dataclass(slots=True)
class TextStyle(Component):
    font: str
    size: int
    color: Color
