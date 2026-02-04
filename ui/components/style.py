from ecs_framework.ecs import ComponentProtocol
from ui.primitives import InteractionColors


class Background(ComponentProtocol):
    color: InteractionColors


class Frame(ComponentProtocol):
    thickness: int
    color: InteractionColors


class TextStyle(ComponentProtocol):
    color: InteractionColors
    size: int
    font: str
