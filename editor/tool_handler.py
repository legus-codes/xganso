from typing import Optional

from editor.hex_map_commands import ChangeSpawnCommand, CreateTileCommand, EraseTileCommand, HexMapCommand, PaintTileCommand, RemoveSpawnCommand
from editor.hex_state import HexMapEditorState
from model.hex_coordinate import HexCoordinate
from model.hex_map import HexMap


class ToolHandler:

    def get_command(self, coordinate: HexCoordinate, hex_map: HexMap, state: HexMapEditorState) -> Optional[HexMapCommand]:
        raise NotImplementedError


class PaintTileHandler(ToolHandler):

    def get_command(self, coordinate: HexCoordinate, hex_map: HexMap, state: HexMapEditorState) -> Optional[HexMapCommand]:
        terrain = state.terrain.get()
        if coordinate in hex_map:
            current = hex_map.get_terrain(coordinate)
            if current != terrain:
                return PaintTileCommand(hex_map, coordinate, terrain, current)
        else:
            return CreateTileCommand(hex_map, coordinate, terrain)
        return None
    

class EraseTileHandler(ToolHandler):

    def get_command(self, coordinate: HexCoordinate, hex_map: HexMap, _: HexMapEditorState) -> Optional[HexMapCommand]:
        if coordinate in hex_map:
            return EraseTileCommand(hex_map, coordinate, hex_map.get_terrain(coordinate))
        return None


class AddSpawnHandler(ToolHandler):

    def get_command(self, coordinate: HexCoordinate, hex_map: HexMap, state: HexMapEditorState) -> Optional[HexMapCommand]:
        spawn = state.spawn.get()
        if coordinate in hex_map:
            current = hex_map.get_spawn(coordinate)
            if current != spawn:
                return ChangeSpawnCommand(hex_map, coordinate, spawn, current)
        return None
    

class RemoveSpawnHandler(ToolHandler):

    def get_command(self, coordinate: HexCoordinate, hex_map: HexMap, _: HexMapEditorState) -> Optional[HexMapCommand]:
        if coordinate in hex_map and hex_map.has_spawn(coordinate):
            return RemoveSpawnCommand(hex_map, coordinate, hex_map.get_spawn(coordinate))
        return None
