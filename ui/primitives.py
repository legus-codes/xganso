from dataclasses import dataclass


@dataclass(slots=True)
class Color:
    r: int
    g: int
    b: int
    a: int = 255


@dataclass(slots=True, frozen=True)
class InteractionColors:
    normal: Color
    hovered: Color
    pressed: Color
    focused: Color
    selected: Color
    disabled: Color


@dataclass(slots=True)
class Vec2:
    x: float
    y: float


@dataclass(slots=True)
class IVec2:
    x: int
    y: int
