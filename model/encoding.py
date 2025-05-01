import json
from typing import Any

from model.hex_coordinate import HexCoordinate
from model.hex_map import HexCell, HexMap
from model.spawn import SpawnLibrary
from model.terrain import TerrainLibrary


class HexMapDecoder(json.JSONDecoder):
    
    def __init__(self, **kwargs):
        super().__init__(object_hook=self.object_hook, **kwargs)

    def object_hook(self, object: Any) -> Any:
        if 'type' in object:
            if object['type'] == 'HexCell':
                q = object['q']
                r = object['r']
                terrain = TerrainLibrary.get(object['terrain'])
                spawn = SpawnLibrary.get(object['spawn'])
                return HexCell(HexCoordinate(q, r), terrain, spawn, None)
            if object['type'] == 'HexMap':
                cells = {cell.coordinate: cell for cell in object['cells']}
                return HexMap(cells)

        return object


class HexMapEncoder(json.JSONEncoder):
    
    def default(self, object: Any) -> Any:
        if isinstance(object, HexCell):
            return {
                'type': 'HexCell',
                'q': object.coordinate.q,
                'r': object.coordinate.r,
                'terrain': object.terrain.value,
                'spawn': object.spawn.value,
            }
        elif isinstance(object, HexMap):
            return {
                'type': 'HexMap',
                'cells': [cell for cell in object]
            }

        return super().default(object)
