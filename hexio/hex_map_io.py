import json

from hexio.encoding import HexMapDecoder, HexMapEncoder
from model.hex_map import HexMap


class HexMapIO:

    @staticmethod
    def save(hex_map: HexMap, filename: str) -> None:
        with open(filename, 'w') as json_file:
            json.dump(hex_map, json_file, cls=HexMapEncoder, indent=4)

    @staticmethod
    def load(filename: str) -> HexMap:
        with open(filename) as json_file:
            return json.load(json_file, cls=HexMapDecoder)
