from dataclasses import dataclass
from typing import List
import math

from editor.hex_camera import HexCamera
from model.hex_coordinate import HexCoordinate
from model.vec2 import VecF2, VecI2


@dataclass(frozen=True)
class HexOrientation:
    forward_x: VecF2
    forward_y: VecF2
    backward_x: VecF2
    backward_y: VecF2
    angle: float


POINTY = HexOrientation(
    forward_x=VecF2(math.sqrt(3), math.sqrt(3)/2),
    forward_y=VecF2(0, 3/2),
    backward_x=VecF2(math.sqrt(3)/3, -1/3),
    backward_y=VecF2(0, 2/3),
    angle=30
)


FLAT = HexOrientation(
    forward_x=VecF2(3/2, 0),
    forward_y=VecF2(math.sqrt(3)/2, math.sqrt(3)),
    backward_x=VecF2(2/3, 0),
    backward_y=VecF2(-1/3, math.sqrt(3)/3),
    angle=0
)


@dataclass
class HexLayout:
    orientation: HexOrientation
    size: VecI2

    def hex_to_point(self, coordinate: HexCoordinate) -> VecF2:
        x = self.orientation.forward_x.dot(coordinate.vector) * self.size.x
        y = self.orientation.forward_y.dot(coordinate.vector) * self.size.y
        return VecF2(x, y)

    def point_to_hex(self, point: VecF2) -> HexCoordinate:
        x = point.x / self.size.x
        y = point.y / self.size.y
        transformed_point = VecF2(x, y)
        q = self.orientation.backward_x.dot(transformed_point)
        r = self.orientation.backward_y.dot(transformed_point)
        return self.round_coordinate(HexCoordinate(q, r))

    def round_coordinate(self, coordinate: HexCoordinate) -> HexCoordinate:
        q = round(coordinate.q)
        r = round(coordinate.r)
        s = round(coordinate.s)

        q_diff = abs(q - coordinate.q)
        r_diff = abs(r - coordinate.r)
        s_diff = abs(s - coordinate.s)

        if q_diff > r_diff and q_diff > s_diff:
            q = -r-s
        elif r_diff > s_diff:
            r = -q-s

        return HexCoordinate(q, r)

    def get_hex_corners(self, center: VecF2) -> List[VecF2]:
        corners = []
        for i in range(6):
            angle = math.radians(60 * i + self.orientation.angle)
            x = center.x + self.size.x * math.cos(angle)
            y = center.y + self.size.y * math.sin(angle)
            corners.append(VecF2(x, y))
        return corners
