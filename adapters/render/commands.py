from dataclasses import dataclass

from core.primitives import Color, IVec2
from omniecs.types import DrawCommand


@dataclass(kw_only=True)
class DrawRectangle(DrawCommand):
    position: IVec2
    size: IVec2
    color: Color


@dataclass(kw_only=True)
class DrawFrame(DrawRectangle):
    width: int


@dataclass
class DrawText:
    position: IVec2
    text: str
    font_id: str
    color: Color
    z: int = 0
