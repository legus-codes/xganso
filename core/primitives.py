from dataclasses import dataclass


@dataclass(slots=True)
class Color:
    r: int
    g: int
    b: int
    a: int = 255


@dataclass(slots=True)
class Vec2:
    x: float = 0
    y: float = 0


@dataclass(slots=True)
class IVec2:
    x: int = 0
    y: int = 0
