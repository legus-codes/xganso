import random
from typing import Self

from model.hex_coordinate import HexCoordinate
from model.hex_map import HexMap
from model.pathfinding import PathfindingHelper
from model.terrain import TerrainLibrary


class HexMapTemplate:

    @staticmethod
    def hexagon_map(radius: int) -> HexMap:
        hex_map = HexMap({})
        for q in range(-radius, radius+1):
            for r in range(max(-radius, -q-radius), min(radius+1, -q+radius+1)):
                hex_map.add_cell(HexCoordinate(q, r), TerrainLibrary.default())
        return hex_map

    @staticmethod
    def square_map(width: int, height: int) -> HexMap:
        top_q = int(-width/2)
        top_r = int(-height/2)
        start = [HexCoordinate(top_q, top_r)]
        for index in range(height-1):
            current = start[-1]
            if index % 2 == 0:
                q = current.q-1
                r = current.r+1
            else:
                q = current.q
                r = current.r+1
            start.append(HexCoordinate(q, r))

        hex_map = HexMap({})
        for index, cell in enumerate(start):
            columns = width if index % 2 == 0 else width+1
            for column in range(columns):
                q = cell.q + column
                hex_map.add_cell(HexCoordinate(q, cell.r), TerrainLibrary.default())
        return hex_map


class HexMapBuilder:

    def __init__(self):
        self.hex_map = HexMap({})

    def hexagon_map(self, radius: int) -> Self:
        self.hex_map = HexMapTemplate.hexagon_map(radius)
        return self

    def square_map(self, width: int, height: int) -> Self:
        self.hex_map = HexMapTemplate.square_map(width, height)
        return self

    def add_lake(self, size: int) -> Self:
        lake_cells = set()
        start = random.choice(self.hex_map.coordinates)
        frontier = [start]

        while len(lake_cells) < size and frontier:
            cell = frontier.pop(0)
            if cell not in lake_cells:
                lake_cells.add(cell)
                for neighbor in PathfindingHelper.neighbors(self.hex_map, cell):
                    if random.random() < 0.6:
                        frontier.append(neighbor.coordinate)

        for cell in lake_cells:
            self.hex_map.change_terrain(cell, TerrainLibrary.water())
        
        return self

    def add_river(self) -> Self:
        return self

    def add_path(self) -> Self:
        return self

    def build(self) -> HexMap:
        return self.hex_map
