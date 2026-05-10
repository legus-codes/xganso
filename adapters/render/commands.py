from dataclasses import dataclass

from core.primitives import Color, IVec2
from omniecs.types import DrawCommand

from ui.components.layout import HorizontalAlignment, VerticalAlignment


@dataclass(kw_only=True)
class DrawRectangle(DrawCommand):
    position: IVec2
    size: IVec2
    color: Color


@dataclass(kw_only=True)
class DrawFrame(DrawRectangle):
    width: int


@dataclass(kw_only=True)
class DrawText(DrawRectangle):
    text: str
    font_id: str
    font_size: int
    horizontal_alignment: HorizontalAlignment
    vertical_alignment: VerticalAlignment
    spacing: IVec2


@dataclass(kw_only=True)
class DrawInput(DrawText):
    value: str
    focused: bool
