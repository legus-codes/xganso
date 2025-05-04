from typing import Protocol

from model.hex_coordinate import HexCoordinate


class HexMapEditorControllerProtocol(Protocol):

    def new_map(self) -> None:
        ...

    def save_map(self) -> None:
        ...

    def load_map(self) -> None:
        ...

    def random_map(self) -> None:
        ...
        
    def handle_click(self, coordinate: HexCoordinate) -> None:
        ...
    
    def handle_hover(self, coordinate: HexCoordinate) -> None:
        ...

    def handle_key_down(self, character: str) -> None:
        ...
