from dataclasses import dataclass
from typing import Self, Tuple


@dataclass(frozen=True)
class VecF2:
    x: float
    y: float

    def __add__(self, other: Self) -> Self:
        return VecF2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Self) -> Self:
        return VecF2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: int) -> Self:
        return VecF2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float) -> Self:
        return VecF2(self.x / scalar, self.y / scalar)

    def dot(self, other: Self) -> float:
        return self.x * other.x + self.y * other.y

    @property
    def as_tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)


@dataclass(frozen=True)
class VecI2:
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return VecI2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Self) -> Self:
        return VecI2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: int) -> Self:
        return VecI2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: int) -> Self:
        return VecI2(self.x / scalar, self.y / scalar)

    def dot(self, other: Self) -> int:
        return self.x * other.x + self.y * other.y
    
    @property
    def as_tuple(self) -> Tuple[int, int]:
        return (self.x, self.y)
