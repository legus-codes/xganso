from dataclasses import dataclass
from pathlib import Path

from ecs_framework.ecs import ECS, ComponentProtocol, SystemProtocol
from editor.map_editor_feedback import Feedback
from editor.map_editor_viewer import Map
from hexio.hex_map_io import HexMapIO


@dataclass
class LoadMapCommand(ComponentProtocol):
    filename: str


class MapLoader(SystemProtocol):

    def __init__(self, world: ECS):
        self.world = world
        self.path = Path(r'C:\Users\matio\xganso')

    def execute(self, delta_time):
        for entity, load_command in self.world.get_entities_with_single_component(LoadMapCommand):
            hex_map = HexMapIO.load(self.path / load_command.filename)
            self.world.add_component(entity, Map(hex_map))
            self.world.add_component(entity, Feedback(f'Map {load_command.filename} loaded successfully'))
            self.world.remove_component(entity, LoadMapCommand)


@dataclass
class SaveMapCommand(ComponentProtocol):
    filename: str


class MapSaver(SystemProtocol):

    def __init__(self, world: ECS):
        self.world = world
        self.path = Path(r'C:\Users\matio\xganso')

    def execute(self, delta_time):
        for entity, save_command in self.world.get_entities_with_single_component(SaveMapCommand):
            hex_map = self.world.get_entity_component(entity, Map)

            if hex_map is not None:
                HexMapIO.save(hex_map.hex_map, self.path / save_command.filename)
                self.world.add_component(entity, Feedback(f'Map {save_command.filename} saved successfully'))

            self.world.remove_component(entity, SaveMapCommand)
