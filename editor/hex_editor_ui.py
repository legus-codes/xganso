from typing import Dict
import functools
import pygame

from editor.hex_editor_canvas import HexEditorCanvas
from editor.hex_map_view import HexMapView
from editor.hex_state import HexEditorMode, HexEditorTool, HexTestTool, MapType, PopupType, UIContext
from ui.panel import Panel
from ui.widgets import Button, IntTextInput, OptionPicker, RadioButton, TextInput, Toggle
from model.spawn import SpawnLibrary
from model.terrain import TerrainLibrary


class TopMenuBar(Panel):

    def __init__(self, ui_context: UIContext, area: pygame.Rect, background: pygame.Color, frame_color: pygame.Color):
        super().__init__(ui_context.screen, area, background, frame_color)
        self.controller = ui_context.controller
        self.state = ui_context.state
        self.radius_input = None
        self.width_input = None
        self.height_input = None
        self.build_widgets()
        self.state.map_type.bind(self.on_map_type_change)
        self.on_map_type_change(self.state.map_type.get())

    def build_widgets(self) -> None:
        self.add_widget(Button(self.surface, 'Save', pygame.Rect(5, 5, 50, 30), command=self.controller.save_map))
        self.add_widget(Button(self.surface, 'Load', pygame.Rect(60, 5, 50, 30), command=self.controller.load_map))
        self.add_widget(Button(self.surface, 'New Map', pygame.Rect(400, 5, 100, 30), command=self.controller.new_map))
        self.add_widget(Button(self.surface, 'Random Map', pygame.Rect(1000, 5, 100, 30), command=self.controller.random_map))
        self.add_widget(RadioButton(self.surface, 'Hexagon', MapType.HEXAGON, self.state.map_type, pygame.Rect(505, 5, 120, 30)))
        self.add_widget(RadioButton(self.surface, 'Square', MapType.SQUARE, self.state.map_type, pygame.Rect(630, 5, 120, 30)))
        self.add_widget(RadioButton(self.surface, 'Edit', HexEditorMode.EDIT, self.state.editor_mode, pygame.Rect(1200, 5, 75, 30)))
        self.add_widget(RadioButton(self.surface, 'Test', HexEditorMode.TEST, self.state.editor_mode, pygame.Rect(1280, 5, 75, 30)))
        self.add_widget(TextInput(self.surface, 'Filename: ', self.state.filename, pygame.Rect(115, 5, 175, 30), pygame.Color('blue')))

        self.radius_input = IntTextInput(self.surface, 'Radius: ', self.state.radius, pygame.Rect(780, 5, 100, 30), pygame.Color('blue'))
        self.width_input = IntTextInput(self.surface, 'Width: ', self.state.width, pygame.Rect(780, 5, 100, 30), pygame.Color('blue'))
        self.height_input = IntTextInput(self.surface, 'Height: ', self.state.height, pygame.Rect(890, 5, 100, 30), pygame.Color('blue'))
        self.add_widget(self.radius_input)
        self.add_widget(self.width_input)
        self.add_widget(self.height_input)

    def on_map_type_change(self, map_type: MapType) -> None:
        is_hex_map = map_type == MapType.HEXAGON
        self.radius_input.enabled = is_hex_map
        self.width_input.enabled = not is_hex_map
        self.height_input.enabled = not is_hex_map


class EditToolMenu(Panel):

    def __init__(self, ui_context: UIContext, area: pygame.Rect, background: pygame.Color, frame_color: pygame.Color):
        super().__init__(ui_context.screen, area, background, frame_color)
        self.controller = ui_context.controller
        self.state = ui_context.state
        self.build_widgets()

    def build_widgets(self) -> None:
        self.add_widget(RadioButton(self.surface, 'Paint Tile', HexEditorTool.PAINT_TILE, self.state.edit_tool, pygame.Rect(5, 10, 140, 30)))
        self.add_widget(RadioButton(self.surface, 'Erase Tile', HexEditorTool.ERASE_TILE, self.state.edit_tool, pygame.Rect(5, 45, 140, 30)))
        self.add_widget(RadioButton(self.surface, 'Add Spawn', HexEditorTool.ADD_SPAWN, self.state.edit_tool, pygame.Rect(5, 80, 140, 30)))
        self.add_widget(RadioButton(self.surface, 'Remove Spawn', HexEditorTool.REMOVE_SPAWN, self.state.edit_tool, pygame.Rect(5, 115, 140, 30)))
        self.add_widget(OptionPicker(self.surface, self.state.terrain, PopupType.TERRAIN, self.state.popup, pygame.Rect(5, 185, 140, 30)))
        self.add_widget(OptionPicker(self.surface, self.state.spawn, PopupType.SPAWN, self.state.popup, pygame.Rect(5, 220, 140, 30)))


class TestToolMenu(Panel):

    def __init__(self, ui_context: UIContext, area: pygame.Rect, background: pygame.Color, frame_color: pygame.Color):
        super().__init__(ui_context.screen, area, background, frame_color)
        self.controller = ui_context.controller
        self.state = ui_context.state
        self.build_widgets()

    def build_widgets(self) -> None: 
        self.add_widget(Toggle(self.surface, 'Path', self.state.test_tools[HexTestTool.PATH], pygame.Rect(5, 10, 140, 30)))
        self.add_widget(Toggle(self.surface, 'Move', self.state.test_tools[HexTestTool.MOVE], pygame.Rect(5, 45, 140, 30)))
        self.add_widget(Toggle(self.surface, 'Range', self.state.test_tools[HexTestTool.RANGE], pygame.Rect(5, 80, 140, 30)))
        self.add_widget(Toggle(self.surface, 'Ring', self.state.test_tools[HexTestTool.RING], pygame.Rect(5, 115, 140, 30)))
        self.add_widget(IntTextInput(self.surface, 'Move Power: ', self.state.move_power, pygame.Rect(5, 180, 140, 30), pygame.Color('blue')))
        self.add_widget(IntTextInput(self.surface, 'Distance: ', self.state.distance, pygame.Rect(5, 215, 140, 30), pygame.Color('blue')))


class TerrainPalettePopup(Panel):
    
    def __init__(self, ui_context: UIContext, area: pygame.Rect, background: pygame.Color, frame_color: pygame.Color):
        super().__init__(ui_context.screen, area, background, frame_color)
        self.state = ui_context.state
        self.build_widgets()

    def build_widgets(self) -> None: 
        for index, terrain in enumerate(TerrainLibrary.values()):
            y = 5 + 35 * index
            callback = functools.partial(self.state.terrain.set, terrain)
            self.add_widget(Button(self.surface, terrain.name, pygame.Rect(5, y, 90, 30), callback, terrain.text_color, terrain.color))

    def handle_event(self, event) -> None:
        super().handle_event(event)
        if event.type == pygame.MOUSEBUTTONUP and self.area.collidepoint(event.pos):
            self.state.popup.set(PopupType.NONE)
        elif event.type == pygame.MOUSEBUTTONDOWN and not self.area.collidepoint(event.pos):
            self.state.popup.set(PopupType.NONE)


class SpawnPalettePopUp(Panel):

    def __init__(self, ui_context: UIContext, area: pygame.Rect, background: pygame.Color, frame_color: pygame.Color):
        super().__init__(ui_context.screen, area, background, frame_color)
        self.state = ui_context.state
        self.build_widgets()

    def build_widgets(self) -> None: 
        for index, spawn in enumerate(SpawnLibrary.values()):
            y = 5 + 35 * index
            callback = functools.partial(self.state.spawn.set, spawn)
            self.add_widget(Button(self.surface, spawn.name, pygame.Rect(5, y, 140, 30), callback, spawn.text_color, spawn.color))

    def handle_event(self, event) -> None:
        super().handle_event(event)
        if event.type == pygame.MOUSEBUTTONUP and self.area.collidepoint(event.pos):
            self.state.popup.set(PopupType.NONE)
        elif event.type == pygame.MOUSEBUTTONDOWN and not self.area.collidepoint(event.pos):
            self.state.popup.set(PopupType.NONE)


class UIManager:

    def __init__(self, ui_context: UIContext, hex_map_view: HexMapView) -> None:
        self.state = ui_context.state
        self.top_menu = TopMenuBar(ui_context, pygame.Rect(0, 0, 1440, 40), pygame.Color(30, 30, 30), pygame.Color(225, 225, 225))
        self.tool_menus: Dict[HexEditorMode, Panel] = {
            HexEditorMode.EDIT: EditToolMenu(ui_context, pygame.Rect(0, 40, 150, 695), pygame.Color(30, 30, 30), pygame.Color(225, 225, 225)),
            HexEditorMode.TEST: TestToolMenu(ui_context, pygame.Rect(0, 40, 150, 695), pygame.Color(30, 30, 30), pygame.Color(225, 225, 225))
        }
        self.editor_canvas = HexEditorCanvas(ui_context, hex_map_view, pygame.Rect(150, 40, 1290, 695), pygame.Color(30, 30, 30), pygame.Color(225, 225, 225))
        terrain_height = TerrainLibrary.count() * 35 + 5
        spawn_height = (SpawnLibrary.count()-1) * 35 + 5
        self.palette_popups: Dict[PopupType, Panel] = {
            PopupType.TERRAIN: TerrainPalettePopup(ui_context, pygame.Rect(150, 225, 100, terrain_height), pygame.Color(230, 100, 230), pygame.Color('turquoise')),
            PopupType.SPAWN: SpawnPalettePopUp(ui_context, pygame.Rect(150, 260, 150, spawn_height), pygame.Color(230, 230, 100), pygame.Color('gold'))
        }

        self.active_tool_menu = None
        self.state.editor_mode.bind(self.update_tool_menu)
        self.update_tool_menu(self.state.editor_mode.get())
        self.active_popup = None
        self.state.popup.bind(self.update_popup_type)
        self.update_popup_type(self.state.popup.get())

    def update_tool_menu(self, editor_mode: HexEditorMode) -> None:
        self.active_tool_menu = self.tool_menus[editor_mode]

    def update_popup_type(self, popup_type: PopupType) -> None:
        self.active_popup = self.palette_popups.get(popup_type, None)

    def handle_event(self, event: pygame.event.Event) -> None:
        if self.active_popup is not None:
            self.active_popup.handle_event(event)
        else:
            self.top_menu.handle_event(event)
            self.editor_canvas.handle_event(event)
        self.active_tool_menu.handle_event(event)

    def draw(self) -> None:
        self.top_menu.draw()
        self.active_tool_menu.draw()
        self.editor_canvas.draw()

        if self.active_popup is not None:
            self.active_popup.draw()
