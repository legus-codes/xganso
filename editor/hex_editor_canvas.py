import pygame

from editor.hex_map_view import HexMapView
from editor.hex_state import HexEditorMode, UIContext
from ui.panel import Panel
from model.hex_map import HexMap
from model.vec2 import VecF2


class HexEditorCanvas(Panel):

    def __init__(self, ui_context: UIContext, hex_map_view: HexMapView, area: pygame.Rect, background: pygame.Color, frame_color: pygame.Color):
        super().__init__(ui_context.screen, area, background, frame_color)
        self.controller = ui_context.controller
        self.state = ui_context.state
        self.hex_map_view = hex_map_view
        self.hex_map_view.set_hex_map_area(self.area)

    def set_hex_map(self, hex_map: HexMap) -> None:
        self.hex_map_view.set_hex_map(hex_map)

    def handle_event(self, event) -> None:
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button not in (4, 5)) or (event.type == pygame.MOUSEMOTION and event.buttons == (1, 0, 0)):
            if not self.area.collidepoint(event.pos):
                return
            coordinate = self.hex_map_view.screen_point_to_hex(VecF2(*event.pos))
            self.controller.handle_click(coordinate)

        if event.type == pygame.MOUSEMOTION:
            if not self.area.collidepoint(event.pos):
                self.controller.handle_hover(None)
                return
            coordinate = self.hex_map_view.screen_point_to_hex(VecF2(*event.pos))
            self.controller.handle_hover(coordinate)

        if event.type == pygame.KEYDOWN:
            self.controller.handle_key_down(event.key)
        
    def draw(self) -> None:
        self.hex_map_view.draw()
        self.screen.set_clip(self.area)
        if self.state.editor_mode.get() == HexEditorMode.TEST:
            for cell in self.state.in_range.get():
                hex_center = self.hex_map_view.hex_to_world_point(cell.coordinate)
                self.hex_map_view.draw_hex_cell(hex_center, pygame.Color('aqua'), pygame.Color('forestgreen'))
            for cell in self.state.ring.get():
                hex_center = self.hex_map_view.hex_to_world_point(cell.coordinate)
                self.hex_map_view.draw_hex_cell(hex_center, pygame.Color('chocolate'), pygame.Color('forestgreen'))
            for cell in self.state.reachable_cells.get():
                hex_center = self.hex_map_view.hex_to_world_point(cell.coordinate)
                self.hex_map_view.draw_hex_cell(hex_center, pygame.Color('snow'), pygame.Color('forestgreen'))
            for cell in self.state.path.get():
                hex_center = self.hex_map_view.hex_to_world_point(cell.coordinate)
                self.hex_map_view.draw_hex_cell(hex_center, pygame.Color('blue'), pygame.Color('white'))
            if self.state.selected_cell.get():
                hex_center = self.hex_map_view.hex_to_world_point(self.state.selected_cell.get())
                self.hex_map_view.draw_hex_cell(hex_center, pygame.Color('gold'), None)
        if self.state.hovered_cell.get():
            hex_center = self.hex_map_view.hex_to_world_point(self.state.hovered_cell.get())
            self.hex_map_view.draw_hex_cell(hex_center, None, pygame.Color('red'))
        self.screen.set_clip(None)
