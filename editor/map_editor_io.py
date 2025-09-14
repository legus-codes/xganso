from dataclasses import dataclass
from pathlib import Path

from ecs_framework.ecs import ECS, ComponentProtocol, SystemProtocol
from editor.map_editor_feedback import Feedback
from hexio.hex_map_io import HexMapIO


@dataclass
class FilenameInputReference(ComponentProtocol):
    entity: int
    component: ComponentProtocol
    field: str


@dataclass
class MapInputReference(ComponentProtocol):
    entity: int
    component: ComponentProtocol
    field: str


@dataclass
class LoadMapTrigger(ComponentProtocol):
    pass


class MapLoader(SystemProtocol):

    def __init__(self, world: ECS):
        self.world = world
        self.path = Path(r'C:\Users\matio\xganso')

    def execute(self, delta_time):
        for entity, (map_input, filename_input, _) in self.world.get_entities_with_components(MapInputReference, FilenameInputReference, LoadMapTrigger):
            filename = self.world.get_entity_component(filename_input.entity, filename_input.component).__getattribute__(filename_input.field)

            hex_map = HexMapIO.load(self.path / filename)
            self.world.add_component(map_input.entity, map_input.component(hex_map))
            self.world.add_component(entity, Feedback(f'Map {filename} loaded successfully'))


class CleanupLoadMap(SystemProtocol):

    def __init__(self, world: ECS):
        self.world = world

    def execute(self, delta_time):
        for entity in self.world.get_entities_with(LoadMapTrigger):
            self.world.remove_component(entity, LoadMapTrigger)


@dataclass
class SaveMapTrigger(ComponentProtocol):
    pass


class MapSaver(SystemProtocol):

    def __init__(self, world: ECS):
        self.world = world
        self.path = Path(r'C:\Users\matio\xganso')

    def execute(self, delta_time):
        for entity, (map_input, filename_input, _) in self.world.get_entities_with_components(MapInputReference, FilenameInputReference, SaveMapTrigger):
            hex_map = self.world.get_entity_component(map_input.entity, map_input.component)
            filename = self.world.get_entity_component(filename_input.entity, filename_input.component).__getattribute__(filename_input.field)

            if hex_map is not None:
                HexMapIO.save(hex_map.__getattribute__(map_input.field), self.path / filename)
                self.world.add_component(entity, Feedback(f'Map {filename} saved successfully'))


class CleanupSaveMap(SystemProtocol):

    def __init__(self, world: ECS):
        self.world = world

    def execute(self, delta_time):
        for entity in self.world.get_entities_with(SaveMapTrigger):
            self.world.remove_component(entity, SaveMapTrigger)
