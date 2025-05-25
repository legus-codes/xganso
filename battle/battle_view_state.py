from typing import Optional
from model.hex_coordinate import HexCoordinate
from model.hex_map import HexMap
from utils.observable import Observable


class BattleViewState:

    def __init__(self):
        self.hovered_cell: Observable[Optional[HexCoordinate]] = Observable(None)
        self.hex_map = None
        
    def set_hex_map(self, hex_map: HexMap) -> None:
        self.hex_map = hex_map
