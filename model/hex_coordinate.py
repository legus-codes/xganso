from dataclasses import dataclass
from typing import List, Self

from model.vec2 import VecI2


@dataclass(frozen=True)
class HexCoordinate:
    q: int
    r: int

    @property
    def s(self) -> int:
        return -self.q - self.r

    @property
    def vector(self) -> VecI2:
        return VecI2(self.q, self.r)

    @property
    def length(self) -> int:
        return max([abs(self.q), abs(self.r), abs(self.s)])

    @staticmethod
    def directions() -> List[VecI2]:
        return [VecI2(1, 0), VecI2(1, -1), VecI2(0, -1), VecI2(-1, 0), VecI2(-1, 1), VecI2(0, 1)]

    @property
    def neighbors(self) -> List[Self]:
        return [self + neighbor for neighbor in self.directions()]

    def __add__(self, other: Self|VecI2) -> Self:
        if isinstance(other, HexCoordinate):
            return HexCoordinate(self.q + other.q, self.r + other.r)
        elif isinstance(other, VecI2):
            return HexCoordinate(self.q + other.x, self.r + other.y)
        raise TypeError(f'Unsupported operand type(s) for +: "HexCoordinate" and "{type(other).__name__}"')

    def __sub__(self, other: Self|VecI2) -> Self:
        if isinstance(other, HexCoordinate):
            return HexCoordinate(self.q - other.q, self.r - other.r)
        elif isinstance(other, VecI2):
            return HexCoordinate(self.q - other.x, self.r - other.y)
        raise TypeError(f'Unsupported operand type(s) for -: "HexCoordinate" and "{type(other).__name__}"')

    def __mul__(self, scalar: int) -> Self:
        return HexCoordinate(self.q * scalar, self.r * scalar)

    def distance(self, other: Self|VecI2) -> int:
        return self.__sub__(other).length
