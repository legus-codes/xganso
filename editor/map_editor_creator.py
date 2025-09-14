from dataclasses import dataclass
from enum import Enum
from random import randint

from ecs_framework.ecs import ECS, ComponentProtocol, SystemProtocol
from editor.map_editor_feedback import Feedback
from editor.map_editor_io import MapInputReference
from model.hex_map import HexMap
from model.hex_map_builder import HexMapBuilder


class MapType(Enum):
    Empty = 0
    Hexagon = 1
    Random = 2


@dataclass
class CreateMapTrigger(ComponentProtocol):
    pass


@dataclass
class MapConfiguration(ComponentProtocol):
    map_type: MapType


@dataclass
class RadiusInputReference(ComponentProtocol):
    entity: int
    component: ComponentProtocol
    field: str


class MapCreator(SystemProtocol):

    def __init__(self, world: ECS):
        self.world = world
        self.hex_map_builder = HexMapBuilder()

    def execute(self, delta_time):
        for entity, (map_configuration, radius_input, map_input, _) in self.world.get_entities_with_components(MapConfiguration, RadiusInputReference, MapInputReference, CreateMapTrigger):
            map_type = map_configuration.map_type
            radius = int(self.world.get_entity_component(radius_input.entity, radius_input.component).__getattribute__(radius_input.field))
            hex_map = self.create_map(map_type, radius)

            self.world.add_component(map_input.entity, map_input.component(hex_map))
            radius_message = ''
            if map_type != MapType.Empty:
                radius_message = f'with radius {radius} '
            self.world.add_component(entity, Feedback(f'{map_type.name} Map {radius_message}created successfully'))
            
    def create_map(self, map_type: MapType, radius: int) -> HexMap:
        match map_type:
            case MapType.Empty:
                return self.hex_map_builder.empty_map().build()

            case MapType.Hexagon:
                return self.hex_map_builder.hexagon_map(radius).build()
            
            case MapType.Random:
                lake_size = randint(6, 30)
                return self.hex_map_builder.hexagon_map(radius).add_lake(lake_size).build()
                
        return self.hex_map_builder.empty_map().build()


class CleanupCreateMap(SystemProtocol):

    def __init__(self, world: ECS):
        self.world = world

    def execute(self, delta_time):
        for entity in self.world.get_entities_with(CreateMapTrigger):
            self.world.remove_component(entity, CreateMapTrigger)
