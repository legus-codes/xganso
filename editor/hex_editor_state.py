from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

import pygame

from utils.observable import Observable
from editor.protocols import HexMapEditorControllerProtocol
from model.hex_coordinate import HexCoordinate
from model.hex_map import HexCell, HexMap
from model.spawn import SpawnLibrary
from model.terrain import TerrainLibrary
from pathfinding.pathfinding import PathfindingHelper


class PopupType(Enum):
    NONE = 0
    TERRAIN = 1
    SPAWN = 2


class MapType(Enum):
    HEXAGON = 1
    SQUARE = 2
    

class HexEditorMode(Enum):
    EDIT = 1
    TEST = 2


class HexEditorTool(Enum):
    PAINT_TILE = 1
    ERASE_TILE = 2
    ADD_SPAWN = 3
    REMOVE_SPAWN = 4


class HexTestTool(Enum):
    PATH = 1
    MOVE = 2
    RANGE = 3
    RING = 4


class HexMapEditorState:

    def __init__(self):
        self.hex_map = None

        self.edit_tool: Observable = Observable(HexEditorTool.PAINT_TILE)
        self.terrain: Observable = Observable(TerrainLibrary.default())
        self.spawn: Observable = Observable(SpawnLibrary.default())
        self.popup: Observable = Observable(PopupType.NONE)

        self.editor_mode: Observable = Observable(HexEditorMode.EDIT)
        self.map_type: Observable = Observable(MapType.HEXAGON)

        self.filename: Observable[str] = Observable('grid.json')
        self.radius: Observable[int] = Observable(5)
        self.width: Observable[int] = Observable(10)
        self.height: Observable[int] = Observable(10)

        self.test_tools: Dict[HexTestTool, Observable[bool]] = {
            HexTestTool.PATH: Observable(False),
            HexTestTool.MOVE: Observable(False),
            HexTestTool.RANGE: Observable(False),
            HexTestTool.RING: Observable(False)
        }

        self.distance: Observable[int] = Observable(3)
        self.move_power: Observable[int] = Observable(3)

        self.selected_cell: Observable[Optional[HexCoordinate]] = Observable(None)
        self.hovered_cell: Observable[Optional[HexCoordinate]] = Observable(None)
        self.path: Observable[List[HexCell]] = Observable([])
        self.reachable_cells: Observable[List[HexCell]] = Observable([])
        self.in_range: Observable[List[HexCell]] = Observable([])
        self.ring: Observable[List[HexCell]] = Observable([])

        self.selected_cell.bind(self.update_path)
        self.hovered_cell.bind(self.update_path)
        self.test_tools[HexTestTool.PATH].bind(self.update_path)
        self.editor_mode.bind(self.update_path)

        self.selected_cell.bind(self.update_reachable_cells)
        self.move_power.bind(self.update_reachable_cells)
        self.test_tools[HexTestTool.MOVE].bind(self.update_reachable_cells)
        self.editor_mode.bind(self.update_reachable_cells)

        self.selected_cell.bind(self.update_in_range)
        self.distance.bind(self.update_in_range)
        self.test_tools[HexTestTool.RANGE].bind(self.update_in_range)
        self.editor_mode.bind(self.update_in_range)

        self.selected_cell.bind(self.update_ring)
        self.distance.bind(self.update_ring)
        self.test_tools[HexTestTool.RING].bind(self.update_ring)
        self.editor_mode.bind(self.update_ring)

    def set_hex_map(self, hex_map: HexMap) -> None:
        self.hex_map = hex_map

    def update_path(self, _: Any) -> None:
        if self.editor_mode.get() == HexEditorMode.TEST and self.test_tools[HexTestTool.PATH].get() and self.selected_cell.get() and self.hovered_cell.get():
            self.path.set(PathfindingHelper.astar(self.hex_map, self.selected_cell.get(), self.hovered_cell.get()))
        else:
            self.path.set([])

    def update_reachable_cells(self, _: Any) -> None:
        if self.editor_mode.get() == HexEditorMode.TEST and self.test_tools[HexTestTool.MOVE].get() and self.selected_cell.get() and self.move_power.get():
            self.reachable_cells.set(PathfindingHelper.bfs(self.hex_map, self.selected_cell.get(), self.move_power.get()))
        else:
            self.reachable_cells.set([])

    def update_in_range(self, _: Any) -> None:
        if self.editor_mode.get() == HexEditorMode.TEST and self.test_tools[HexTestTool.RANGE].get() and self.selected_cell.get() and self.distance.get():
            self.in_range.set(PathfindingHelper.in_range(self.hex_map, self.selected_cell.get(), self.distance.get()))
        else:
            self.in_range.set([])

    def update_ring(self, _: Any) -> None:
        if self.editor_mode.get() == HexEditorMode.TEST and self.test_tools[HexTestTool.RING].get() and self.selected_cell.get() and self.distance.get():
            self.ring.set(PathfindingHelper.ring(self.hex_map, self.selected_cell.get(), self.distance.get()))
        else:
            self.ring.set([])


@dataclass
class UIContext:
    controller: HexMapEditorControllerProtocol
    state: HexMapEditorState
    screen: pygame.Surface
