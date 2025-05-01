from dataclasses import dataclass
from enum import IntEnum
from typing import List, Optional


class TerrainType(IntEnum):
    GRASS = 1
    FOREST = 2
    PATH = 3
    HILL = 4
    MOUNTAIN = 5
    WATER = 6
    SWAMP = 7
    SNOW = 8
    SAND = 9


@dataclass(frozen=True)
class Terrain:
    terrain_type: TerrainType
    color: str
    text_color: str
    walkable: bool
    move_cost: float

    @property
    def name(self) -> str:
        return self.terrain_type.name.capitalize()

    @property
    def value(self) -> int:
        return self.terrain_type.value


class TerrainLibrary:

    terrains = {
        TerrainType.GRASS: Terrain(TerrainType.GRASS, 'green', 'black', True, 1),
        TerrainType.FOREST: Terrain(TerrainType.FOREST, 'forestgreen', 'black', True, 2),
        TerrainType.PATH: Terrain(TerrainType.PATH, 'tan', 'black', True, 0.5),
        TerrainType.HILL: Terrain(TerrainType.HILL, 'tan4', 'black', True, 2),
        TerrainType.MOUNTAIN: Terrain(TerrainType.MOUNTAIN, 'saddlebrown', 'black', False, 0),
        TerrainType.WATER: Terrain(TerrainType.WATER, 'turquoise2', 'black', False, 0),
        TerrainType.SWAMP: Terrain(TerrainType.SWAMP, 'yellowgreen', 'black', True, 3),
        TerrainType.SNOW: Terrain(TerrainType.SNOW, 'snow', 'black', True, 1.5),
        TerrainType.SAND: Terrain(TerrainType.SAND, 'yellow2', 'black', True, 2),
    }

    @classmethod
    def count(cls) -> int:
        return len(cls.terrains)

    @classmethod
    def get(cls, terrain_type: str|TerrainType) -> Optional[Terrain]:
        if isinstance(terrain_type, str):
            terrain_type = TerrainType[terrain_type]
        return cls.terrains.get(terrain_type, None)

    @classmethod
    def default(cls) -> Terrain:
        return cls.terrains[TerrainType.GRASS]
    
    @classmethod
    def water(cls) -> Terrain:
        return cls.terrains[TerrainType.WATER]

    @classmethod
    def values(cls) -> List[Terrain]:
        return list(cls.terrains.values())
