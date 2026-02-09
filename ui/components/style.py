from dataclasses import dataclass

from ecs_framework.primitives import ComponentProtocol
from ui.types import InteractionColors


@dataclass(slots=True)
class Background(ComponentProtocol):
    color: InteractionColors


@dataclass(slots=True)
class Frame(ComponentProtocol):
    color: InteractionColors
    width: int


@dataclass(slots=True)
class TextStyle(ComponentProtocol):
    font: str
    size: int
    color: InteractionColors
