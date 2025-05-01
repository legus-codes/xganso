# import unittest

# from model.hexgrid import HexCell

# class TestHexCell(unittest.TestCase):

#     def test_s_field(self):
#         hex = HexCell(2, 3)
#         self.assertEqual(-5, hex.s)
#         self.assertEqual(0, hex.q + hex.r + hex.s)

#     def test_hexcells_are_equal(self):
#         hex1 = HexCell(1, 5)
#         hex2 = HexCell(1, 5)
#         self.assertEqual(hex1, hex2)


# # class TestHexMath(unittest.TestCase):

# #     def test_add(self):
# #         hex1 = HexCell(1, 4)
# #         hex2 = HexCell(-7, -2)
# #         hex_add = HexMath.add(hex1, hex2)
# #         self.assertEqual(-6, hex_add.q)
# #         self.assertEqual(2, hex_add.r)
# #         self.assertEqual(4, hex_add.s)

# #     def test_subtract(self):
# #         hex1 = HexCell(1, 4)
# #         hex2 = HexCell(-7, -2)
# #         hex_subtract = HexMath.subtract(hex1, hex2)
# #         self.assertEqual(8, hex_subtract.q)
# #         self.assertEqual(6, hex_subtract.r)
# #         self.assertEqual(-14, hex_subtract.s)

# #     def test_multiply(self):
# #         hex = HexCell(1, 4)
# #         k = 5
# #         hex_multiply = HexMath.multiply(hex, k)
# #         self.assertEqual(5, hex_multiply.q)
# #         self.assertEqual(20, hex_multiply.r)
# #         self.assertEqual(-25, hex_multiply.s)

# #     def test_length(self):
# #         hex = HexCell(6, 2)
# #         length = HexMath.length(hex)
# #         self.assertEqual(8, length)

# #     def test_distance(self):
# #         hex1 = HexCell(6, 2)
# #         hex2 = HexCell(3, 1)
# #         distance = HexMath.distance(hex1, hex2)
# #         self.assertEqual(4, distance)

# #     def test_neighbors(self):
# #         hex = HexCell(3, -2)
# #         neigbors = HexMath.neighbors(hex)
# #         expected_neighbors = [HexCell(4, -2), HexCell(4, -3), HexCell(3, -3),
# #                               HexCell(2, -2), HexCell(2, -1), HexCell(3, -1)]
# #         self.assertEqual(expected_neighbors, neigbors)


# if __name__ == '__main__':
#     unittest.main()
