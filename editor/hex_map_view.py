import pygame

from battle.unit import Unit
from editor.hex_camera import HexCamera
from model.hex_coordinate import HexCoordinate
from model.hex_geometry import HexLayout
from model.hex_map import HexMap
from model.vec2 import VecF2


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
        pygame.draw.circle(self.screen, unit.color, hex_center, radius)
        self.draw_text(unit.name[0].capitalize(), pygame.Color('black'), hex_center)

    def draw_text(self, text: str, color: pygame.Color, hex_center: VecF2) -> None:
        text_surface = self.font.render(text, True, color)
        position = pygame.Vector2(hex_center.x - (text_surface.get_width() / 2), hex_center.y - (text_surface.get_height() / 2))
        self.screen.blit(text_surface, position)
