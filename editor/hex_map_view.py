import pygame

from battle.unit import Unit
from editor.hex_camera import HexCamera
from editor.hex_editor_state import HexEditorMode, UIContext
from model.hex_coordinate import HexCoordinate, VecF2
from model.hex_geometry import HexLayout
from model.hex_map import HexMap
from ui.elements import Panel


class HexMapView:

    def __init__(self, screen: pygame.Surface, layout: HexLayout, camera: HexCamera):
        self.screen = screen
        self.area = None
        self.layout = layout
        self.camera = camera
        self.hex_map = None
        self.font = pygame.font.SysFont('Arial', 20)

    def set_hex_map(self, hex_map: HexMap) -> None:
        self.hex_map = hex_map

    def set_hex_map_area(self, area: pygame.Rect) -> None:
        self.area = area
        self.camera.set_origin(VecF2(*self.area.center))

    def hex_to_world_point(self, coordinate: HexCoordinate) -> VecF2:
        return self.layout.hex_to_point(coordinate)

    def screen_point_to_hex(self, point: VecF2) -> HexCoordinate:
        world_position = self.camera.screen_to_world(point)
        return self.layout.point_to_hex(world_position)

    def draw(self) -> None:
        if self.hex_map:
            self.draw_hex_map(self.hex_map)

    def draw_hex_map(self, hex_map: HexMap) -> None:
        self.screen.set_clip(self.area)
        for cell in hex_map.sorted_cells:
            hex_center = self.hex_to_world_point(cell.coordinate)
            self.draw_hex_cell(hex_center, cell.color, cell.frame_color)
            if cell.is_occupied:
                self.draw_unit(hex_center, cell.unit)
        self.screen.set_clip(None)

    def draw_hex_cell(self, hex_center: VecF2, color: pygame.Color = None, frame_color: pygame.Color = None) -> None:
        corners = self.layout.get_hex_corners(hex_center)
        corners_tuples = [self.camera.world_to_screen(corner).as_tuple for corner in corners]
        if color:
            pygame.draw.polygon(self.screen, color, corners_tuples)
        if frame_color:
            pygame.draw.polygon(self.screen, frame_color, corners_tuples, 2)

    def draw_unit(self, hex_center: VecF2, unit: Unit) -> None:
        radius = 12 * self.camera.zoom
        screen_center = self.camera.world_to_screen(hex_center)
        pygame.draw.circle(self.screen, unit.color, screen_center.as_tuple, radius)
        self.draw_text(unit.name[0].capitalize(), pygame.Color('black'), screen_center)

    def draw_text(self, text: str, color: pygame.Color, hex_center: VecF2) -> None:
        text_surface = self.font.render(text, True, color)
        position = pygame.Vector2(hex_center.x - (text_surface.get_width() / 2), hex_center.y - (text_surface.get_height() / 2))
        self.screen.blit(text_surface, position)


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
