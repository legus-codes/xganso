from dataclasses import dataclass
from ecs_framework.ecs import ComponentProtocol
from ui.primitives import InteractionColors


@dataclass(slots=True)
class Background(ComponentProtocol):
    color: InteractionColors


@dataclass(slots=True)
class Frame(ComponentProtocol):
    color: InteractionColors
    width: int


@dataclass(slots=True)
class TextStyle(ComponentProtocol):
    color: InteractionColors
    size: int
    font: str
