from dataclasses import dataclass

from pygame import Surface

from ecs_framework.ecs import ECS, ComponentProtocol, SystemProtocol
from editor.hex_camera import HexCamera
from editor.hex_map_view import HexMapView
from model.hex_coordinate import VecF2
from model.hex_geometry import POINTY, HexLayout
from model.hex_map import HexMap
from ui.ui_components import UIRect


@dataclass
class Map(ComponentProtocol):
    hex_map: HexMap


@dataclass
class MapDisplaySource(ComponentProtocol):
    entity: int


class MapRendererSystem(SystemProtocol):

    def __init__(self, world: ECS, screen: Surface):
        self.world = world
        self.map_view = HexMapView(screen, HexLayout(POINTY, VecF2(20, 20)), HexCamera())

    def execute(self, delta_time):
        for _, (area, map_source) in self.world.get_entities_with_components(UIRect, MapDisplaySource):
            self.map_view.set_hex_map_area(area.rectangle)
            hex_map = self.world.get_entity_component(map_source.entity, Map)
            if hex_map is None:
                continue

            self.map_view.set_hex_map(hex_map.hex_map)
            self.map_view.draw()
