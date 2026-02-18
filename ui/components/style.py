from dataclasses import dataclass

from ecs_framework.types import Component
from ui.types import InteractionColors


@dataclass(slots=True)
class Background(Component):
    color: InteractionColors


@dataclass(slots=True)
class Frame(Component):
    color: InteractionColors
    width: int


@dataclass(slots=True)
class TextStyle(Component):
    font: str
    size: int
    color: InteractionColors
