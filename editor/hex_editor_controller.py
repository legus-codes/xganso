from typing import Dict, Optional
import random
import pygame

from editor.hex_camera import HexCamera
from editor.hex_editor_ui import UIContext, UIManager
from editor.hex_map_model import HexMapModel
from editor.hex_map_view import HexMapView
from editor.hex_state import HexEditorMode, HexEditorTool, HexMapEditorState, MapType
from editor.tool_handler import AddSpawnHandler, EraseTileHandler, PaintTileHandler, RemoveSpawnHandler, ToolHandler
from model.hex_coordinate import HexCoordinate
from model.hex_geometry import POINTY, HexLayout
from model.hex_map import HexMap
from model.hex_map_builder import HexMapBuilder
from model.io import HexMapIO
from model.vec2 import VecF2


class MapManager:

    def __init__(self, hex_map_builder: HexMapBuilder, hex_map_model: HexMapModel):
        self.hex_map_builder = hex_map_builder
        self.hex_map_model = hex_map_model

    def create_hexagon_map(self, radius: int) -> None:
        if radius:
            hex_map = self.hex_map_builder.hexagon_map(radius).build()
            self.hex_map_model.set_hex_map(hex_map)

    def create_square_map(self, width: int, height: int) -> HexMap:
        if width and height:
            hex_map =  self.hex_map_builder.square_map(width, height).build()
            self.hex_map_model.set_hex_map(hex_map)

    def save_map(self, filename: str) -> None:
        HexMapIO.save(self.hex_map_model.hex_map.get(), filename)

    def load_map(self, filename: str) -> None:
        hex_map = HexMapIO.load(filename)
        self.hex_map_model.set_hex_map(hex_map)

    def random_map(self) -> None:
        radius = random.randint(8, 12)
        lake_size = random.randint(6, 30)
        hex_map = self.hex_map_builder.hexagon_map(radius).add_lake(lake_size).build()
        self.hex_map_model.set_hex_map(hex_map)


class InputHandler:

    def __init__(self, state: HexMapEditorState, ui_manager: UIManager, hex_map_model: HexMapModel, camera: HexCamera, tool_handlers: Dict[HexEditorTool, ToolHandler]):
        self.state = state
        self.ui_manager = ui_manager
        self.hex_map_model = hex_map_model
        self.camera = camera
        self.tool_handlers = tool_handlers

    def handle_click(self, coordinate: HexCoordinate) -> None:
        if self.state.editor_mode.get() == HexEditorMode.EDIT:
            handler = self.tool_handlers[self.state.edit_tool.get()]
            command = handler.get_command(coordinate, self.hex_map_model.hex_map.get(), self.state)
            if command:
                self.hex_map_model.apply_command(command)
        elif self.state.editor_mode.get() == HexEditorMode.TEST:
            if coordinate in self.hex_map_model.hex_map.get():
                if self.state.selected_cell.get() == coordinate:
                    self.state.selected_cell.set(None)
                else:
                    self.state.selected_cell.set(coordinate)
            else:
                self.state.selected_cell.set(None)

    def handle_hover(self, coordinate: Optional[HexCoordinate]) -> None:
        self.state.hovered_cell.set(coordinate)

    def handle_key_down(self, key: int) -> None:
        if self.state.editor_mode.get() == HexEditorMode.EDIT:
            if key == pygame.K_u:
                self.hex_map_model.undo() 

    def handle_event(self, event) -> None:
        self.ui_manager.handle_event(event)
        self.camera.handle_event(event)

    def handle_key_pressed(self, keys: pygame.key.ScancodeWrapper) -> None:
        self.camera.handle_key_pressed(keys)


class HexEditorController:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.hex_map_model = HexMapModel(HexMap({}))
        self.map_manager = MapManager(HexMapBuilder(), self.hex_map_model)

        self.layout = HexLayout(POINTY, VecF2(20, 20))
        self.camera = HexCamera()
        self.state = HexMapEditorState()
        self.hex_map_view = HexMapView(self.screen, self.layout, self.camera)
        self.hex_map_model.hex_map.bind(self.state.set_hex_map)
        self.hex_map_model.hex_map.bind(self.hex_map_view.set_hex_map)
        self.hex_map_model.hex_map.set(HexMap({}))

        self.ui_context = UIContext(self, self.state, self.screen)
        self.ui_manager = UIManager(self.ui_context, self.hex_map_view)

        self.tool_handlers: Dict[HexEditorTool, ToolHandler] = {
            HexEditorTool.PAINT_TILE: PaintTileHandler(),
            HexEditorTool.ERASE_TILE: EraseTileHandler(),
            HexEditorTool.ADD_SPAWN: AddSpawnHandler(),
            HexEditorTool.REMOVE_SPAWN: RemoveSpawnHandler(),
        }

        self.input_handler = InputHandler(self.state, self.ui_manager, self.hex_map_model, self.camera, self.tool_handlers)

    def new_map(self) -> None:
        map_type = self.state.map_type.get()
        radius = self.state.radius.get()
        width = self.state.width.get()
        height = self.state.height.get()

        if map_type == MapType.HEXAGON:
            self.map_manager.create_hexagon_map(radius)
        elif map_type == MapType.SQUARE:
            self.map_manager.create_square_map(width, height)

    def save_map(self) -> None:
        self.map_manager.save_map(self.state.filename.get())

    def load_map(self) -> None:
        self.map_manager.load_map(self.state.filename.get())

    def random_map(self) -> None:
        self.map_manager.random_map()

    def handle_click(self, coordinate: HexCoordinate) -> None:
        self.input_handler.handle_click(coordinate)

    def handle_hover(self, coordinate: Optional[HexCoordinate]) -> None:
        self.input_handler.handle_hover(coordinate)

    def handle_key_down(self, key: int) -> None:
        self.input_handler.handle_key_down(key)

    def handle_event(self, event) -> None:
        self.input_handler.handle_event(event)

    def handle_key_pressed(self, keys: pygame.key.ScancodeWrapper) -> None:
        self.input_handler.handle_key_pressed(keys)

    def draw(self) -> None:
        self.ui_manager.draw()
