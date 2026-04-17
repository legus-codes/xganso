from dataclasses import dataclass
from typing import Self


@dataclass(slots=True)
class Color:
    r: int
    g: int
    b: int
    a: int = 255

    @property
    def tuple(self) -> tuple[int, int, int, int]:
        return (self.r, self.g, self.b, self.a)


@dataclass(slots=True)
class Vec2:
    x: float = 0
    y: float = 0

    @property
    def tuple(self) -> tuple[float, float]:
        return (self.x, self.y)

    def __add__(self, other: Self) -> Self:
        return Vec2(self.x + other.x, self.y + other.y)


@dataclass(slots=True)
class IVec2:
    x: int = 0
    y: int = 0

    @property
    def tuple(self) -> tuple[int, int]:
        return (self.x, self.y)


@dataclass(slots=True)
class Rect:
    x: float = 0
    y: float = 0
    w: float = 0
    h: float = 0

    @classmethod
    def from_transform(cls, position: Vec2 | IVec2, size: Vec2 | IVec2) -> Self:
        return cls(position.x, position.y, size.x, size.y)

    def contains(self, point: Vec2) -> bool:
        return self.x <= point.x <= self.x + self.w and self.y <= point.y <= self.y + self.h
