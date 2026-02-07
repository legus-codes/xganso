from dataclasses import dataclass

from core.primitives import Color, IVec2


@dataclass
class DrawRect:
    position: IVec2
    size: IVec2
    color: Color
    z: int = 0


@dataclass
class DrawText:
    position: IVec2
    text: str
    font_id: str
    color: Color
    z: int = 0
