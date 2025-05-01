import unittest
import random

from model.hex_coordinate import HexCoordinate
from model.vec2 import VecI2


class TestHexCoordinate(unittest.TestCase):

    directions = [VecI2(1, 0), VecI2(1, -1), VecI2(0, -1), VecI2(-1, 0), VecI2(-1, 1), VecI2(0, 1)]

    def test_s_property(self) -> None:
        for _ in range(1000):
            q = random.randint(-50, 50)
            r = random.randint(-50, 50)
            hex = HexCoordinate(q, r)
            self.assertEqual(hex.s, -q-r)

    def test_vector_property(self) -> None:
        for _ in range(1000):
            q = random.randint(-50, 50)
            r = random.randint(-50, 50)
            hex = HexCoordinate(q, r)
            self.assertIsInstance(hex.vector, VecI2)
            self.assertEqual(hex.vector.x, q)
            self.assertEqual(hex.vector.y, r)

    def test_length_property(self) -> None:
        for _ in range(1000):
            q = random.randint(-50, 50)
            r = random.randint(-50, 50)
            hex = HexCoordinate(q, r)
            length = int((abs(hex.q) + abs(hex.r) + abs(hex.s)) / 2)
            self.assertEqual(hex.length, length)

    def test_directions_property(self) -> None:
        hex = HexCoordinate(0, 0)
        self.assertListEqual(hex.directions(), self.directions)

    def test_neighbors_property(self) -> None:
        for _ in range(1000):
            q = random.randint(-50, 50)
            r = random.randint(-50, 50)
            hex = HexCoordinate(q, r)
            neighbors = []
            for direction in self.directions:
                neighbors.append(hex + direction)
            self.assertListEqual(hex.neighbors, neighbors)

    def test_add_with_hex(self) -> None:
        hex1 = HexCoordinate(2, 3)
        hex2 = HexCoordinate(-5, 4)
        hex = hex1 + hex2
        self.assertEqual(hex.q, -3)
        self.assertEqual(hex.r, 7)

    def test_add_with_tuple(self) -> None:
        hex1 = HexCoordinate(7, -2)
        vec2 = VecI2(-2, 2)
        hex = hex1 + vec2
        self.assertEqual(hex.q, 5)
        self.assertEqual(hex.r, 0)

    def test_add_with_unsupported_type(self) -> None:
        hex1 = HexCoordinate(0, 0)
        str2 = '2, 3'
        with self.assertRaises(TypeError):
            _ = hex1 + str2

    def test_sub_with_hex(self) -> None:
        hex1 = HexCoordinate(2, 3)
        hex2 = HexCoordinate(-5, 4)
        hex = hex1 - hex2
        self.assertEqual(hex.q, 7)
        self.assertEqual(hex.r, -1)

    def test_sub_with_tuple(self) -> None:
        hex1 = HexCoordinate(7, -2)
        vec2 = VecI2(-2, 2)
        hex = hex1 - vec2
        self.assertEqual(hex.q, 9)
        self.assertEqual(hex.r, -4)

    def test_sub_with_unsupported_type(self) -> None:
        hex1 = HexCoordinate(0, 0)
        str2 = '2, 3'
        with self.assertRaises(TypeError):
            _ = hex1 - str2

    def test_mul(self) -> None:
        hex1 = HexCoordinate(4, -9)
        scalar = 3
        hex = hex1 * scalar
        self.assertEqual(hex.q, 12)
        self.assertEqual(hex.r, -27)

    def test_distance_with_hex(self) -> None:
        hex1 = HexCoordinate(2, 3)
        hex2 = HexCoordinate(-5, 4)
        distance = hex1.distance(hex2)
        self.assertEqual(distance, 7)

    def test_distance_with_tuple(self) -> None:
        hex1 = HexCoordinate(7, -2)
        vec2 = VecI2(-2, 2)
        distance = hex1.distance(vec2)
        self.assertEqual(distance, 9)

    def test_distance_with_unsupported_type(self) -> None:
        hex1 = HexCoordinate(0, 0)
        str2 = '2, 3'
        with self.assertRaises(TypeError):
            _ = hex1.distance(str2)

if __name__ == '__main__':
    unittest.main()
