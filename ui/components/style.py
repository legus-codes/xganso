from dataclasses import dataclass, field

from omniecs.types import Component
from core.primitives import Color, ColorStack


@dataclass(slots=True)
class Background(Component):
    colors: ColorStack

    @property
    def color(self) -> Color:
        return self.colors.color

@dataclass(slots=True)
class Frame(Component):
    colors: ColorStack
    width: int

    @property
    def color(self) -> Color:
        return self.colors.color


@dataclass(slots=True)
class TextStyle(Component):
    font: str
    size: int
    colors: ColorStack

    @property
    def color(self) -> Color:
        return self.colors.color
