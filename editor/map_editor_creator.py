from dataclasses import dataclass
from enum import Enum
from random import randint

from ecs_framework.ecs import ECS, ComponentProtocol, SystemProtocol
from editor.map_editor_feedback import Feedback
from editor.map_editor_viewer import Map
from model.hex_map import HexMap
from model.hex_map_builder import HexMapBuilder


class MapType(Enum):
    Empty = 0
    Hexagon = 1
    Random = 2


@dataclass
class CreateMapCommand(ComponentProtocol):
    map_type: MapType
    radius: int


class MapCreater(SystemProtocol):

    def __init__(self, world: ECS):
        self.world = world
        self.hex_map_builder = HexMapBuilder()

    def execute(self, delta_time):
        for entity, create_command in self.world.get_entities_with_single_component(CreateMapCommand):
            hex_map = self.create_map(create_command.map_type, create_command.radius)

            self.world.add_component(entity, Map(hex_map))
            radius_message = ''
            if create_command.map_type != MapType.Empty:
                radius_message = f'with radius {create_command.radius} '
            self.world.add_component(entity, Feedback(f'{create_command.map_type.name} Map {radius_message}created successfully'))

            self.world.remove_component(entity, CreateMapCommand)
            
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
