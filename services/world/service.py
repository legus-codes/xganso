from typing import Dict
from ecs_architecture.component.builder import ComponentBuilder, ComponentBuilderProtocol
from ecs_architecture.component.registry import ComponentRegistry
from ecs_framework.ecs import ECS
from services.data.models import DataDescription
from services.world.core import WorldServiceConfig


class WorldService:
    
    def __init__(self, builder: ComponentBuilderProtocol):
        self.builder = builder
        self.worlds: Dict[str, ECS] = {}

    def build_world(self, name: str) -> None:
        if not self.has_world(name):
            self.worlds[name] = ECS()

    def destroy_world(self, name: str) -> None:
        self.worlds.pop(name, None)

    def has_world(self, name: str) -> bool:
        return name in self.worlds

    def get_world(self, name: str) -> ECS | None:
        return self.worlds.get(name, None)

    def build_entity(self, world_name: str, data: DataDescription) -> int | None:
        world = self.get_world(world_name)
        if world is None:
            return None
        
        components = self.builder.build(data.model_dump())
        entity = world.create_entity()
        for component in components:
            world.add_component(entity, component)

        return entity

    def destroy_entity(self, world_name: str, entity_id: int) -> None:
        world = self.get_world(world_name)
        if world is None:
            return

        world.delete_entity(entity_id)


class WorldServiceFactory:
    
    @staticmethod
    def build(world_service_config: WorldServiceConfig) -> WorldService:
        registry = ComponentRegistry()
        registry.load_all(world_service_config.components)
        builder = ComponentBuilder(registry)
        return WorldService(builder)
